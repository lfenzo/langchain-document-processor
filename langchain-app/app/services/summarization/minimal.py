from langchain.prompts import ChatPromptTemplate

from app.services import MinimalService, ServiceTypes


class Summarizer(MinimalService):
    """
    A minimal service for generating concise summaries of text.

    The `Summarizer` focuses on producing multi-language summaries that retain key points,
    central themes, and significant details, while adhering to a percentage-based length
    constraint.
    """

    def __init__(self, text_percentage: int = 30, **kwargs):
        """
        Initializes the `Summarizer` with a text percentage limit for the output.

        Parameters
        ----------
        text_percentage : int, optional
            The percentage of the original text length to target for the summary (default is 30).
        **kwargs
            Additional keyword arguments passed to the parent `MinimalService` class.
        """
        super().__init__(**kwargs)
        self.text_percentage = text_percentage

    @property
    def service_type(self) -> str:
        """
        The type of service, defined as `ServiceTypes.SUMMARIZATION`.

        Returns
        -------
        str
            The string constant representing the service type.
        """
        return ServiceTypes.SUMMARIZATION

    @property
    def prompt(self) -> ChatPromptTemplate:
        """
        Defines the prompt template for the summarization task.

        Returns
        -------
        ChatPromptTemplate
            The prompt template for generating summaries based on key points, themes, and details.
        """
        return ChatPromptTemplate.from_messages([
            (
                self.message_type,
                """
                You are an AI specialized in multi-language summaries. Your task is to summarize
                the provided text by focusing on the key points, central themes, and significant
                details.
                """
            ),
            (
                self.message_type,
                f"""
                Ensure the summary is approximately {self.text_percentage}% of the original text
                length. Avoid superficial details or unnecessary information.
                """
            ),
            (
                self.message_type,
                """
                Follow these additional guidelines to generate the summary:
                - Produce the summary in the same language as the input text
                - Assume the document’s intended audience
                - Keep the tone and style consistent with the original
                - Do not add introductions, conclusions, or external knowledge
                - Do not use verbs in the first person
                """
            ),
            ("human", "{text}")
        ])

    def get_logging_information(self) -> dict:
        """
        Retrieves logging information specific to the `Summarizer` service.

        Returns
        -------
        dict
            A dictionary containing the `text_percentage` value used in the summarization task.
        """
        return {"text_percentage": self.text_percentage}
