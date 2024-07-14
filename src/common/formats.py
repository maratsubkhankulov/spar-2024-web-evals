from typing import List, Iterator

from langchain_community.document_loaders.base import BaseLoader
from langchain.document_loaders import CSVLoader, EverNoteLoader, TextLoader, PyPDFLoader
from langchain.document_loaders import (
    UnstructuredEPubLoader,
    UnstructuredHTMLLoader,
    UnstructuredMarkdownLoader,
    UnstructuredODTLoader,
    UnstructuredPowerPointLoader,
    UnstructuredWordDocumentLoader,
    UnstructuredURLLoader,
)
from langchain_core.documents import Document
import ocrmypdf

from src.common.handlers import dump_file


class PDFLoaderOCR(PyPDFLoader):
    def __init__(self, *args, dumping_def: callable = dump_file, language: List[str] = None, **kwargs):
        if language is None:
            language = ['rus', 'eng']

        self.language = language
        self.ocr = ocrmypdf.ocr
        self.dumping_def = dumping_def
        super().__init__(*args, **kwargs)

    def load(self) -> List[Document]:
        """Load given path as pages."""
        stream = self.lazy_load()
        recognized_docs = self.check_stream(stream)
        if not recognized_docs:
            new_path = self.dumping_def(self.file_path)
            self.ocr(new_path, self.file_path, language=self.language)
            recognized_docs = list(self.lazy_load())
        return recognized_docs

    def check_stream(self, stream: Iterator[Document], limit: int = 30, threshold: float = 0.3) -> List[Document]:
        """
        Check a given stream for recognized pages
        :param stream: stream of documents
        :param limit: limit of pages
        :param threshold: threshold of percentage unrecognized pages vs recognized pages
        :return: list of documents or empty list in case of the unrecognized pages more than the limit
        """
        out_list = list()
        counter = 0
        for doc in stream:
            out_list.append(doc)
            counter += 1 if not doc.page_content else 0
            if counter > limit:
                out_list = list()
                break

        if counter / (len(out_list) + 1e-6) > threshold:
            out_list = list()

        return out_list


LOADER_MAPPING = {  # noqa: WPS407
    'csv': (CSVLoader, {}),
    'doc': (UnstructuredWordDocumentLoader, {'mode': 'elements'}),
    'docx': (UnstructuredWordDocumentLoader, {'mode': 'elements'}),
    'enex': (EverNoteLoader, {}),
    'epub': (UnstructuredEPubLoader, {}),
    'html': (UnstructuredHTMLLoader, {}),
    'md': (UnstructuredMarkdownLoader, {}),
    'odt': (UnstructuredODTLoader, {}),
    'pdf': (PDFLoaderOCR, {}),
    'ppt': (UnstructuredPowerPointLoader, {'mode': 'elements'}),
    'pptx': (UnstructuredPowerPointLoader, {'mode': 'elements'}),
    'txt': (TextLoader, {'encoding': 'utf8'}),
}


def get_loader(source: str) -> BaseLoader | None:
    """
    Get loader related to a source format
    :param source: source for recognition
    :return: loader
    """
    if source.lower().startswith('https://'):
        return UnstructuredURLLoader(urls=[source])

    mark = source.lower().split('.')[-1]
    if mark in LOADER_MAPPING:
        loader_cls, kwargs = LOADER_MAPPING[mark]  # noqa: WPS529
        return loader_cls(source, **kwargs)
