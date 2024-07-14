from dependency_injector import containers, providers

from src.common.handlers import load_created_object
from src.controller.llm import Agent


class LLMContainer(containers.DeclarativeContainer):
    config = providers.Configuration()

    embeddings = providers.Singleton(
        load_created_object,
        config.embeddings.object,
        config.embeddings.kwargs,
    )

    llm = providers.Singleton(
        load_created_object,
        config.llm.object,
        config.llm.kwargs,
    )

    agent = providers.Singleton(
        Agent,
        llm=llm
    )
