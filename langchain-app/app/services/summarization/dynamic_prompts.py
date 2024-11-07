from typing import Any, AsyncIterator

from langchain_core.documents.base import Document
from langchain_core.messages.ai import AIMessageChunk, AIMessage
from langchain.chat_models.base import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate

from app.models import DocumentInfo
from app.services.base import BaseService


class DynamicPromptSummarizer(BaseService):
    """
    A service for dynamically generating summaries and extracting structured information 
    from text using customizable prompt templates and language models.

    This class leverages a dual-model setup:
    - One model for extraction tasks.
    - Another model for summarization tasks.
    """

    def __init__(
        self,
        chatmodel: BaseChatModel,
        extraction_chatmodel: BaseChatModel,
        **kwargs,
    ) -> None:
        """
        Initializes the `DynamicPromptSummarizer` with specified language models.

        Parameters
        ----------
        chatmodel : BaseChatModel
            The language model used for summarization tasks.
        extraction_chatmodel : BaseChatModel
            The language model used for structured data extraction tasks.
        **kwargs
            Additional keyword arguments passed to the parent `BaseService` class.
        """
        super().__init__(**kwargs)
        self.chatmodel = chatmodel
        self.extraction_chatmodel = extraction_chatmodel

    @property
    def extraction_prompt(self) -> ChatPromptTemplate:
        """
        Defines the prompt template for extracting structured information.

        Returns
        -------
        ChatPromptTemplate
            The prompt template for the extraction task.
        """
        return ChatPromptTemplate.from_messages([
            (
                "human",
                """
                You are an expert extraction algorithm, specialized in extracting structured
                information. Your task is to accurately identify and extract relevant attributes
                from the provided text. For each attribute, if the value cannot be determined from
                the text, return 'null' as the attribute's value. Ensure the extracted information
                is concise, relevant, and structured according to the required format.
                """
            ),
            ("human", "{text}"),
        ])

    @property
    def summarization_prompt(self) -> ChatPromptTemplate:
        """
        Defines the prompt template for generating summaries.

        Returns
        -------
        ChatPromptTemplate
            The prompt template for the summarization task.
        """
        return ChatPromptTemplate.from_messages([
            (
                "human",
                """
                You are an advanced AI specializing in identifying and summarizing the most
                important and relevant information from complex documents. Your task is to create
                a detailed summary by focusing on the key ideas, core arguments, and supporting
                details.
                """
            ),
            (
                "human",
                """
                Ensure the summary is approximately 30% of the original length. Prioritize the
                following:
                - Major themes and critical points
                - Important supporting details that enhance the key points
                - Exclude redundant or trivial information
                """
            ),
            (
                "human",
                """
                Follow these guidelines when generating the summary:
                - Text Type: {text_type} (e.g., report, presentation, article)
                - Media Type: {media_type} (e.g., PDF, PPT, DOC)
                - Domain: {document_domain} (e.g., finance, medical, legal)
                - Audience: {audience} (e.g., general, experts)
                - Audience Expertise: {audience_expertise} (e.g., beginner, intermediate, advanced)
                - Focus on Document Key Points: {key_points}
                """
            ),
            (
                "human",
                """
                The summary must be written in the same language as the input document, maintaining
                the document’s formal tone and style. Avoid introductory phrases and external
                knowledge. Simply focus on what is present in the document itself.
                """
            ),
            ("human", "{text}"),
        ])

    @property
    def extraction_chain(self):
        """
        Combines the extraction prompt and the extraction model to form an execution chain.

        Returns
        -------
        Any
            A chain object combining the prompt and the model with structured output.
        """
        return (
            self.extraction_prompt
            | self.extraction_chatmodel.with_structured_output(schema=DocumentInfo)
        )

    @property
    def summarization_chain(self):
        """
        Combines the summarization prompt and the summarization model to form an execution chain.

        Returns
        -------
        Any
            A chain object combining the prompt and the summarization model.
        """
        return self.summarization_prompt | self.chatmodel

    def summarize(self, content: list[Document]) -> AsyncIterator[AIMessageChunk] | AIMessage:
        """
        Summarizes the given content using both extraction and summarization chains.

        Parameters
        ----------
        content : list[Document]
            A list of `Document` objects to be summarized.

        Returns
        -------
        AsyncIterator[AIMessageChunk] or AIMessage
            The generated summary, either as an asynchronous stream or a single message.
        """
        text = self._get_text_from_content(content=content)
        structured_information = self.extraction_chain.invoke({"text": text})
        return self.summarization_chain.ainvoke({"text": text, **structured_information.dict()})

    def get_metadata(self, file: str, generation_metadata: dict) -> dict[str, Any]:
        """
        Retrieves metadata for the summarization task, including model and prompt details.

        Parameters
        ----------
        file : str
            The name of the file being processed.
        generation_metadata : dict
            Additional metadata about the generation process.

        Returns
        -------
        dict[str, Any]
            A dictionary containing the combined metadata.
        """
        metadata = self._get_base_metadata(file=file, generation_metadata=generation_metadata)
        metadata.update({
            'chatmodel': repr(self.chatmodel),
            "summarization_prompt": repr(self.summarization_prompt),
            'extraction_chatmodel': repr(self.extraction_chatmodel),
            "extraction_prompt": repr(self.extraction_prompt),
            "structured_straction_schema": DocumentInfo.__class__.__name__,
        })
        return metadata
