from typing import Any, AsyncIterator

from langchain_core.documents.base import Document
from langchain_core.messages.ai import AIMessageChunk, AIMessage
from langchain.chat_models.base import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate

from app.models import DocumentInfo
from app.services.base import BaseService


class DynamicPromptSummarizer(BaseService):

    def __init__(
        self,
        chatmodel: BaseChatModel,
        extraction_chatmodel: BaseChatModel,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self.chatmodel = chatmodel
        self.extraction_chatmodel = extraction_chatmodel

    @property
    def extraction_prompt(self) -> ChatPromptTemplate:
        return ChatPromptTemplate.from_messages([
            (
                "human",
                """
                You are an expert extraction algorithm, specialized in extracting structured
                information. Your task is to accurately identify and extract relevant attributes
                from the provided text. For each attribute, if the value cannot be determined from
                the text, return 'null' as the attribute's value. Ensure the extracted information
                is concise, relevant, and structured according to the required format."
                """
            ),
            ("human", "{text}"),
        ])

    @property
    def summarization_prompt(self) -> ChatPromptTemplate:
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
        return (
            self.extraction_prompt
            | self.extraction_chatmodel.with_structured_output(schema=DocumentInfo)
        )

    @property
    def summarization_chain(self):
        return self.summarization_prompt | self.chatmodel

    def summarize(self, content: list[Document]) -> AsyncIterator[AIMessageChunk] | AIMessage:
        text = self._get_text_from_content(content=content)
        structured_information = self.extraction_chain.invoke({"text": text})
        return self.summarization_chain.ainvoke({"text": text, **structured_information.dict()})

    def get_metadata(self, file: str, generation_metadata: dict) -> dict[str, Any]:
        metadata = self._get_base_metadata(file=file, generation_metadata=generation_metadata)
        metadata.update({
            'chatmodel': repr(self.chatmodel),
            "summarization_prompt": repr(self.summarization_prompt),
            'extraction_chatmodel': repr(self.extraction_chatmodel),
            "extraction_prompt": repr(self.extraction_prompt),
            "structured_straction_schema": DocumentInfo.__class__.__name__,
        })
        return metadata
