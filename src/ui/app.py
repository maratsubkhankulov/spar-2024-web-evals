from typing import List

import anyio
from dependency_injector.wiring import inject, Provide

from src.common.handlers import make_dummy_task
from src.containers import LLMContainer
from src.controller.pipe import pipe
from src.core.problem import Lesson, Strategy, Problem
from src.core.tasks import Task
from src.extractor import VectorHandler


def run_async(fn):
    async def wrapper(*args, **kwargs):
        return await anyio.to_thread.run_sync(
            fn, *args, **kwargs
        )

    return wrapper


@run_async
@inject
def generate_context(
        title: str, sources: List[str], llm=Provide[LLMContainer.llm], embeddings=Provide[LLMContainer.embeddings]
):
    handler = VectorHandler(embeddings, llm)
    context = handler(title, sources)
    return handler, context


async def generate_lesson(title: str, sources: List[str], config_path: str) -> Lesson:
    if sources:
        handler, context = await generate_context(title, sources)
    else:
        context = ''
    struct = dict(context=context, title=title)
    strategy = Strategy.from_yaml(config_path)

    tasks = strategy.lesson if isinstance(strategy.lesson, Task) else make_dummy_task(strategy.lesson)
    out = await pipe(tasks, struct)
    lines = []
    for line in out:
        if "_lines" in line:
            lines.append(line[:-len("_lines")])

    problems = []

    for item in lines:
        line_key, vim_key = item + "_lines", item + "_vim"  # noqa: WPS336
        if vim_key in out:
            problem = Problem(lines=out[line_key], vim_lines=out[vim_key])
        else:
            problem = Problem(lines=out[line_key])
        problems.append(problem)

    return Lesson(plan='' if 'plan' not in out else out['plan'], problems=problems)
