import asyncio
import re
from typing import Union

from dependency_injector.wiring import inject, Provide
from langchain_core.messages import HumanMessage

from src.common.tool import extract_parts
from src.containers import LLMContainer
from src.controller.llm import Agent
from src.core.tasks import Task

template_border = f"\n\n{'#' * 40}\n\n"  # noqa: WPS432  this template is convenient for reading


async def parse_output(question, kwargs, key, line=template_border, re_str=r'\n#+\n*'):
    parsed = re.split(re_str, kwargs[key])
    tasks = []
    for ind, item in enumerate(parsed):
        kws = kwargs.copy()
        kws.update({key: item})
        tasks.append(
            Task(
                name=str(ind),
                question=question,
                kwargs=kws
            )
        )
    out_dict = {}
    output = await asyncio.gather(*[pipe(task) for task in tasks])
    for out in output:
        out_dict.update(out)
    return line.join(out_dict[str(index)] for index in range(len(parsed)))  # noqa: WPS221


@inject
def make_message(task: Task, bodies: dict = Provide[LLMContainer.config.bodies]) -> Union[str, HumanMessage]:
    parts = extract_parts(task.question, bodies)
    if len(parts) == 1:
        return task.question
    return HumanMessage(content=parts)


@inject
async def pipe(task: Task, default_kwargs={}, agent: Agent = Provide[LLMContainer.agent]) -> dict:  # noqa: WPS231
    """
    Pipeline constructor for fractalized tasks
    :param task: a current fractalized task
    :param default_kwargs: default arguments for the current task
    :param agent: llm for the asynchronous generation
    :return: updated kwargs - dict with returned values
    """
    default_kwargs.update(task.kwargs)

    if isinstance(task.steps, list):  # go to the leafs or through the branch breadthwise
        paralleled = []

        for step in task.steps:
            default_kwargs_step = default_kwargs.copy()
            default_kwargs_step.update(step.kwargs)
            paralleled.append(pipe(step, default_kwargs_step))
        outputs = await asyncio.gather(*paralleled)
        for out in outputs:
            default_kwargs.update(out)

    if isinstance(task.steps, Task):  # go to the leaf or through the branch longwise
        output = await pipe(task.steps, default_kwargs)
        default_kwargs.update(output)

    task.steps = None

    agent = agent if not task.priority_model else Agent(llm=agent.llm.__class__(llm=task.priority_model))  # noqa:WPS221

    if (task.parse is None and default_kwargs.get('parse')) or task.parse:
        task.parse = default_kwargs.get('parse') if task.parse is None else task.parse
        output = await parse_output(task.question, default_kwargs, task.parse)
        default_kwargs['parse'] = None
    else:
        task.question = task.question.format(**default_kwargs)
        output = await agent([make_message(task)])

    output = {task.name: output}
    default_kwargs.update(output)
    return default_kwargs
