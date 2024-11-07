from langchain.prompts import ChatPromptTemplate

from app.services import MinimalService, ServiceTypes


class Translator(MinimalService):
    """
    A minimal service for translating text into a specified target language.

    The `Translator` ensures accurate translations while preserving the meaning,
    context, style, and structure of the original document.
    """

    def __init__(self, target_language: str, **kwargs):
        """
        Initializes the `Translator` with a specified target language.

        Parameters
        ----------
        target_language : str
            The language to which the text will be translated.
        **kwargs
            Additional keyword arguments passed to the parent `MinimalService` class.
        """
        super().__init__(**kwargs)
        self.target_language = target_language

    @property
    def service_type(self) -> str:
        """
        The type of service, defined as `ServiceTypes.TRANSLATION`.

        Returns
        -------
        str
            The string constant representing the service type.
        """
        return ServiceTypes.TRANSLATION

    @property
    def prompt(self) -> ChatPromptTemplate:
        """
        Defines the prompt template for the translation task.

        Returns
        -------
        ChatPromptTemplate
            The prompt template for translating text into the target language.
        """
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

    def get_logging_information(self) -> dict:
        """
        Retrieves logging information specific to the `Translator` service.

        Returns
        -------
        dict
            A dictionary containing the `target_language` value used in the translation task.
        """
        return {"target_language": self.target_language}
