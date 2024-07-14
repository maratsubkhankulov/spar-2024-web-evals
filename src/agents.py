from typing import Any, cast

from langchain.agents import create_openai_functions_agent, AgentExecutor, BaseMultiActionAgent
from langchain_core.language_models import BaseChatModel

from src.common.tools import tools
from src.templates.instructions import base_prompt, solvers_alignment_task


async def make_tool_agent_executor(llm: BaseChatModel, input: dict[str, Any], **kwargs):
    # create agent -- cast needed due to:
    # https://github.com/langchain-ai/langchain/issues/13075
    refined_instructions = await llm.ainvoke(
        solvers_alignment_task.format(input=input)
    )
    tools_agent = create_openai_functions_agent(
        llm, tools, base_prompt.partial(instructions=refined_instructions.content)
    )

    return AgentExecutor.from_agent_and_tools(
        agent=cast(BaseMultiActionAgent, tools_agent),
        tools=tools,
        name="translator",
        **kwargs
    )