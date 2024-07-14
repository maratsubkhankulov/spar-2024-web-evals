from typing import Any, cast

from langchain.agents import (
    AgentExecutor,
    BaseMultiActionAgent,
    create_openai_functions_agent,
)
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain_core.language_models import BaseChatModel

from inspect_ai._eval.registry import task
from inspect_ai._eval.task import Task
from inspect_ai.dataset import json_dataset
from inspect_ai.scorer import model_graded_fact
from inspect_ai.solver import Solver, solver
from src.inspect_langchain import langchain_solver
from src.templates.instructions import prompt
from src.common.tools import tools


@solver
def wikipedia_search(
    max_iterations: int | None = 15, max_execution_time: float | None = None
) -> Solver:
    # standard prompt for functions agent
    # prompt = hub.pull("hwchase17/openai-tools-agent")

    # tavily and wikipedia tools
    # tavily_api = TavilySearchAPIWrapper()  # type: ignore
    # tools = load_tools(["wikipedia"])

    # agent function
    async def agent(llm: BaseChatModel, input: dict[str, Any]):
        # create agent -- cast needed due to:
        # https://github.com/langchain-ai/langchain/issues/13075
        tools_agent = create_openai_functions_agent(llm, tools + load_tools(["wikipedia"]), prompt)
        agent_executor = AgentExecutor.from_agent_and_tools(
            agent=cast(BaseMultiActionAgent, tools_agent),
            tools=tools,
            name="wikipedia_search",
            max_iterations=max_iterations,
            max_execution_time=max_execution_time,
        )

        # execute the agent and return output
        result = await agent_executor.ainvoke(input)
        return result["output"]

    # return agent function as inspect solver
    return langchain_solver(agent)


@task
def wikipedia() -> Task:
    return Task(
        dataset=json_dataset("wikipedia.jsonl"),
        plan=wikipedia_search(),
        scorer=model_graded_fact(),
    )