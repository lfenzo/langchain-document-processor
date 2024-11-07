from typing import Any
from abc import ABC, abstractmethod

from langchain_core.documents.base import Document
from langchain_core.messages.ai import AIMessage, AIMessageChunk


class BaseService(ABC):
    """
    Abstract base class for defining services that process documents.

    The `BaseService` provides a structure for implementing services with methods
    for running tasks, retrieving metadata, and handling logging. It includes
    utility methods for processing document content and managing metadata.
    """

    @abstractmethod
    def run(self, content: list[Document]) -> AIMessage:
        """
        Executes the service's main functionality on the provided documents.

        Parameters
        ----------
        content : list[Document]
            A list of `Document` objects to process.

        Returns
        -------
        AIMessage
            The output of the service as an AI-generated message.
        """
        pass

    @abstractmethod
    def get_metadata(self, file: str, gen_metadata: dict) -> dict[str, Any]:
        """
        Retrieves metadata about the service execution.

        Parameters
        ----------
        file : str
            The name of the file being processed.
        gen_metadata : dict
            Metadata about the generation process.

        Returns
        -------
        dict[str, Any]
            A dictionary containing the metadata for the service.
        """
        pass

    def get_logging_information(self) -> dict:
        """
        Retrieves logging-specific information for the service.

        Returns
        -------
        dict
            A dictionary containing logging-related information (default is empty).
        """
        return {}

    def set_logger(self, logger) -> None:
        """
        Sets the logger for the service.

        Parameters
        ----------
        logger : Any
            The logger instance to use for logging service activity.
        """
        self.logger = logger

    def _get_text_from_content(self, content: list[Document]) -> str:
        """
        Extracts the text content from a list of `Document` objects.

        Parameters
        ----------
        content : list[Document]
            A list of `Document` objects to extract text from.

        Returns
        -------
        str
            The combined text content from all documents, separated by newlines.
        """
        return "".join([page.page_content + "\n" for page in content])

    def _get_content_from_chunks(self, chunks: list[AIMessageChunk]) -> str:
        """
        Combines the content from a list of AI message chunks.

        Parameters
        ----------
        chunks : list[AIMessageChunk]
            A list of `AIMessageChunk` objects to extract content from.

        Returns
        -------
        str
            The combined content from all chunks.
        """
        return "".join([c.content for c in chunks])

    def _get_base_metadata(self, file: str, gen_metadata: dict) -> dict[str, Any]:
        """
        Constructs base metadata for the service execution.

        Parameters
        ----------
        file : str
            The name of the file being processed.
        gen_metadata : dict
            Metadata about the generation process, including response and usage metadata.

        Returns
        -------
        dict[str, Any]
            A dictionary containing the base metadata, including input file, response metadata,
            and usage metadata.
        """
        return {
            'input_file': file,
            **gen_metadata.response_metadata,
            **gen_metadata.usage_metadata,
        }
