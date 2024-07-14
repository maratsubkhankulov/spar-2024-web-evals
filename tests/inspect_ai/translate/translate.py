import re
from typing import Any

from langchain_core.language_models import BaseChatModel

from inspect_ai._eval.registry import task
from inspect_ai._eval.task import Task
from inspect_ai.dataset import json_dataset
from inspect_ai.model import Model, get_model
from inspect_ai.scorer import scorer, accuracy, bootstrap_std, Scorer, Target, Score
from inspect_ai.scorer._model import DEFAULT_MODEL_GRADED_QA_TEMPLATE
from inspect_ai.solver import TaskState, Solver, solver

from src.agents import make_tool_agent_executor
from src.common.tools import ask, extract_grade
from src.inspect_langchain import langchain_solver
from src.templates.instructions import (
    creation_prompt, scorers_header_task, scorers_instruction_task
)


@scorer(metrics=[accuracy(), bootstrap_std()])
def model_graded_qa(
        template: str = DEFAULT_MODEL_GRADED_QA_TEMPLATE, *args, model: str | Model | None = None, **kwargs
) -> Scorer:
    # resolve model
    grader_model = get_model(model)

    async def score(state: TaskState, target: Target) -> Score:
        # format the model grading template
        header = await ask(
            grader_model, creation_prompt,
            {'description': state.input_text, 'task': scorers_header_task}
        )

        hints = await ask(
            grader_model,
            creation_prompt,
            {'description': state.input_text, "task": scorers_instruction_task}
        )

        score_prompt = template.format(
            header=header.message.content,
            question=state.input_text,
            answer=state.output.completion,
            criterion=target.text,
            instructions=hints.message.content,
        )

        # query the model for the score
        result = await grader_model.generate(score_prompt)

        return extract_grade(result, metadata={'score_prompt': score_prompt})

    return score



@solver
def agent(
        max_iterations: int | None = 15, max_execution_time: float | None = None
) -> Solver:
    # agent function
    async def agent(llm: BaseChatModel, input: dict[str, Any]):

        agent_executor = await make_tool_agent_executor(
            llm, input, max_iterations=max_iterations, max_execution_time=max_execution_time
        )
        # execute the agent and return output
        result = await agent_executor.ainvoke(input)
        return result["output"]

    # return agent function as inspect solver
    return langchain_solver(agent)


@task
def translate() -> Task:
    return Task(
        dataset=json_dataset("translate.jsonl"),
        plan=agent(),
        scorer=model_graded_qa(),
    )