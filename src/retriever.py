import os
from typing import List

import faiss
from langchain.text_splitter import NLTKTextSplitter
from langchain_community.docstore import InMemoryDocstore
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain.vectorstores.faiss import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_core.vectorstores import VectorStore

from src.common.faiss_additives import concatenate_indexes
from src.common.formats import get_loader
from src.common.handlers import write_file


class Vectorizer:
    """
    Implementation of the vectorization methods.
    """
    document_store = 'data/document_store'

    def __init__(
        self,
        embeddings: Embeddings,
        document_store: str = 'data/document_store',
        splitter=NLTKTextSplitter(separator=' ', chunk_size=1000, chunk_overlap=100)  # noqa: WPS404 B008
    ):
        """
        Initialization of the vectorizer with predefined prompt template
        :param embeddings: embeddings model
        :param document_store: path to document store
        """

        self.index = None
        self.document_store = document_store  # noqa: WPS601
        self.embeddings = embeddings
        self.splitter = splitter

    def __call__(self, sources: List[str]) -> None:  # noqa: WPS231
        """
        Create vectorization files
        :param sources: list of files
        """

        for source in sources:
            real_source = os.path.join(self.document_store, source)
            vectorbase = real_source + '.index'  # noqa: WPS336
            if not os.path.exists(vectorbase):
                doc = get_loader(real_source)
                if not doc:
                    continue
                chunks = doc.load()
                chunks = chunks if not self.splitter else self.split_chunks(chunks)
                self.create_index(chunks).save_local(vectorbase)
            index = concatenate_indexes(self.index, self.embeddings, vectorbase)
            self.index = index if index else self.index

    def create_index(self, chunks: List[Document]) -> FAISS:
        """
        Create vectorization files (semantic search database)
        :param chunks: list of documents with piece of information
        :return: database of vectorized documents
        """
        texts = [doc.page_content for doc in chunks]
        metadatas = [doc.metadata for doc in chunks]
        return FAISS.from_texts(texts, self.embeddings, metadatas=metadatas)

    def similar_data(self, question: str, template: str) -> PromptTemplate:
        """
        Search similar data
        :param template: prompt template with predefined format with 'context' and 'question' fields
        :param question: string with target question
        :return: prompt with additional information related to question and 'question' field
        """
        context = additive_information(self.index.similarity_search(question))
        return PromptTemplate(template=template, input_variables=['context', 'question']).partial(context=context)

    def split_chunks(self, sources: List[Document]) -> List[Document]:
        """
        Split documents into chunks
        :param sources: list of sources
        :return: list of chunks
        """
        return self.splitter.split_documents(sources)

    def load_local(self, index_path: str, embeddings) -> None:
        """
        Load vectorized files
        :param index_path: path to index file
        :param embeddings: embeddings model
        """
        self.index = FAISS.load_local(index_path, embeddings)

    @staticmethod
    def pure_faiss_index(embeddings: Embeddings) -> VectorStore:  # noqa: WPS602
        dim = 768  # embeddings.client.encode('some').size == 768
        return FAISS(embeddings, faiss.IndexFlatL2(dim), InMemoryDocstore({}), {})

    @classmethod
    def write_file(cls, path: str, content: bytes) -> None:
        """
        Write any file in predefined place
        """
        if not os.path.exists(cls.document_store):
            os.makedirs(cls.document_store, exist_ok=True)
        write_file(str(os.path.join(cls.document_store, path)), content)


def additive_information(docs: List[Document]) -> str:
    return '\n'.join([doc.page_content for doc in docs])
