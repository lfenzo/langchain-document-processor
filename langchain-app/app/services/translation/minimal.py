from langchain.prompts import ChatPromptTemplate

from app.services import MinimalService, ServiceTypes


class Translator(MinimalService):

    def __init__(self, target_language: str, **kwargs):
        super().__init__(**kwargs)
        self.target_language = target_language

    @property
    def service_type(self):
        return ServiceTypes.TRANSLATION

    @property
    def prompt(self):
        return ChatPromptTemplate.from_messages([
            (
                self.message_type,
                """
                You are an AI specialized in translating text between multiple languages.
                Your task is to translate the provided document into the target language
                accurately, while preserving the meaning, context, and style of the original
                text.
                """
            ),
            (
                self.message_type,
                """
                Follow these guidelines when translating:
                - Use vocabulary, syntax, and tone appropriate for the target language
                - Ensure the translation maintains the original context and intent
                - Do not add introductions, explanations, or footnotes
                - Avoid word-for-word translation; prioritize fluidity and coherence
                - Retain any formatting like lists or bullet points from the original document
                """
            ),
            (
                self.message_type,
                """
                Output the translation in the exact structure of the original document, preserving
                any line breaks, headings, or sections.
                """
            ),
            (self.message_type, f"Translate the text to {self.target_language}"),
            ("human", "{text}")
        ])
