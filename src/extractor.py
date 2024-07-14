import os
import re
from typing import List, Tuple, Dict

from langchain_community.llms.openai import OpenAI
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings

from src.controller.llm import LLMGenerator
from src.core.errors import NotFoundInSource
from src.prompter.search_agent import content_table_question, context_prompt, topic_borders_question
from src.retriever import Vectorizer


class VectorHandler(LLMGenerator):  # noqa: WPS230 TODO: this raw configuation has to be changed
    """
    Context extractor with auxiliary methods for vector search
    """
    def __init__(  # noqa: WPS211 TODO: this raw configuation has to be changed
        self,
        embeddings: Embeddings,
        llm: OpenAI,
        document_store_path: str = '/app/data/document_store',
        context_prompt: str = context_prompt,
        content_table_question: str = content_table_question,
        topic_borders_question: str = topic_borders_question,
        vectorizer_kwargs: dict = {'splitter': None},
    ):
        self.embeddings = embeddings
        self.llm = llm
        self.structure = {}
        self.document_store_path = document_store_path
        self.context_prompt = context_prompt
        self.content_table_question = content_table_question
        self.topic_borders_question = topic_borders_question
        self.vectorizer_kwargs = vectorizer_kwargs

    def __call__(self, title: str, sources: List[str]) -> str:
        """
        Generate context paragraph from the list of sources with vector search (RAG system)
        :param title: title of the paragraph
        :param sources: list of sources
        :return: context paragraph
        """
        contexts = []
        for source in sources:
            vectorizer = Vectorizer(self.embeddings, self.document_store_path, **self.vectorizer_kwargs)
            source_path = os.path.join(self.document_store_path, source)
            content, docs = self.get_content_table(source_path, vectorizer)
            contexts.append(self.extract_context(title, content, docs))
        return ''.join(contexts)

    @staticmethod
    def parse_doc_list(docs: List[Document], sep: str = '\n') -> str:
        """
        Parse list of documents to string
        :param docs: list of documents
        :param sep: separator for concatenation
        :return: concatenated string
        """
        return sep.join(part.page_content for part in docs)

    def ask(self, question: str, context: str) -> str:
        """
        Ask question to LLM
        :param question: question
        :param context: context
        :return: answer
        """
        prompt = self.context_prompt.format(question=question, context=context)
        return self.generate(prompt)

    @staticmethod
    def get_pages(line_with_pages: str) -> List[int]:
        print(line_with_pages)  # noqa: WPS421 it's for raw log you can remove it or replace with logger
        pages = re.findall(r'\d+', line_with_pages)
        if len(pages) < 2:
            raise NotFoundInSource(line_with_pages)
        return list(map(int, pages[-2:]))

    def get_content_table(
        self,
        source: str,
        vectorizer: Vectorizer,
        context_trigger: str = "Введение, ...........§ 1, § 20, Глава 3",
    ) -> Tuple[str, Dict[str, Document]]:
        """
        Context table extractor
        :param source: path to the source
        :param vectorizer: system for vector search
        :param context_trigger: context trigger for vector search
        :return: context table and structure with docs from faiss docstore
        """
        vectorizer([source])
        parts = vectorizer.index.similarity_search(context_trigger)

        raw_content = '\n'.join(part.page_content for part in parts)
        content = self.ask(self.content_table_question, raw_content)
        return content, vectorizer.index.docstore._dict  # noqa: WPS437

    @staticmethod
    def get_target_docs(  # noqa: WPS602
        docs: Dict[str, Document], pages: List[int], additive_pages: List = None
    ) -> List[Document]:
        """
        Extractor target docs with context from raw source (book or everything else)
        :param docs: docstore
        :param pages: target pages for extraction
        :param additive_pages: additional pages for extraction (boundaries)
        :return: target docs with target information
        """
        target_docs = []
        additive_pages = additive_pages if additive_pages else pages
        add_pages = (additive_pages[1] - additive_pages[0]) // 2
        for doc in docs.values():
            right_boundary = pages[1] + add_pages
            left_boundary = pages[0] - add_pages
            if left_boundary < doc.metadata['page'] < right_boundary:
                target_docs.append(doc)
        return target_docs

    def extract_context(self, title: str, content: str, docs: Dict[str, Document]) -> str:
        """
        Extract context from the content.
        First of all, it extracts the name of the target or relevant part of the content table.
        Secondly, from the extracted target part, it extracts the pages and cuts the content with the boundaries.
        :param title: title of the paragraph
        :param content: content table
        :param docs: docstore
        :return: extracted context by the title borders or relevant paragraph of the content table
        """
        extracted_target_part = self.ask(self.topic_borders_question.format(title=title), content)
        target_pages = self.get_pages(extracted_target_part)
        return self.parse_doc_list(self.get_target_docs(docs, target_pages))
