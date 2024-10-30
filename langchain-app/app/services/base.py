from typing import Any
from abc import ABC, abstractmethod

from langchain_core.documents.base import Document
from langchain_core.messages.ai import AIMessage, AIMessageChunk


class BaseService(ABC):

    @abstractmethod
    def run(self, content: list[Document]) -> AIMessage:
        pass

    @abstractmethod
    def get_metadata(self, file: str, gen_metadata: dict) -> dict[str, Any]:
        pass

    def get_logging_information(self) -> dict:
        return {}

    def set_logger(self, logger) -> None:
        self.logger = logger

    def _get_text_from_content(self, content: list[Document]) -> str:
        return "".join([page.page_content + "\n" for page in content])

    def _get_content_from_chunks(self, chunks: list[AIMessageChunk]) -> str:
        return "".join([c.content for c in chunks])

    def _get_base_metadata(self, file: str, gen_metadata: dict) -> dict[str, Any]:
        return {
            'input_file': file,
            **gen_metadata.response_metadata,
            **gen_metadata.usage_metadata,
        }
