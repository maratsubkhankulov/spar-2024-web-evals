import asyncio
from typing import List, Tuple, Union

from langchain_community.llms import OpenAI
from langchain_core.messages import BaseMessage

from src.common.handlers import jsonize


class AsyncLLMGenerator:
    llm: OpenAI

    async def async_generate(self, filled_prompt: Union[str, BaseMessage]) -> str:
        """
        Async version of generate
        :param filled_prompt: target prompt (not raw) for the generation
        :return: generated text from the llm
        """
        out = await self.llm.ainvoke(filled_prompt)
        return out.content

    async def concurrently_generate(self, filled_prompts: List[str]) -> Tuple[str]:
        """
        Async version of generate for batch generation concurrently
        :param filled_prompts: target prompts (not raw) for the generation
        :return: generated outputs from the llm
        """
        tasks = [self.async_generate(pr) for pr in filled_prompts]
        return await asyncio.gather(*tasks)


class LLMGenerator:
    llm: OpenAI

    def generate(self, filled_prompt: Union[str, BaseMessage]) -> str:
        """
        Ordinary version of generate
        :param filled_prompt: target prompt (not raw) for the generation
        :return: generated text from the llm
        """
        out = self.llm.invoke(filled_prompt)
        return out.content


class Agent(AsyncLLMGenerator):
    """
    Controller for mechanics (raw version)
    """

    def __init__(self, llm: OpenAI):
        self.llm = llm

    @jsonize
    async def __call__(self, question: Union[str, List[BaseMessage]]) -> str:
        """
        Asynchronously generates series of the stages for Problem building
        :param question: question for asking llm
        :return: answer
        """
        return await self.async_generate(question)
