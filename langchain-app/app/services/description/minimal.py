from langchain.prompts import ChatPromptTemplate

from app.services import MinimalService, ServiceTypes


class Descriptor(MinimalService):
    """
    A service for generating concise descriptions of documents.

    The `Descriptor` generates short sentence summaries that outline the main
    purpose of a document, ensuring the output is in the same language as the
    original document. The output is constrained by a maximum token limit.
    """

    def __init__(self, max_tokens: int, **kwargs) -> None:
        super().__init__(**kwargs)
        self.max_tokens = max_tokens

    @property
    def service_type(self) -> str:
        return ServiceTypes.DESCRIPTION

    @property
    def prompt(self) -> ChatPromptTemplate:
        """
        Generates the prompt template for the description task.

        The prompt instructs the model to create a concise document description,
        adhering to the token limit and maintaining the document's original language.

        Returns
        -------
        ChatPromptTemplate
            The chat prompt template with instructions for the description task.
        """
        return ChatPromptTemplate.from_messages([
            (
                self.message_type,
                """
                Generate only a 2 to 3 sentence description of this document in the same language
                as the original document. Make sure to outline the main purpose of the document
                in your description.
                """
            ),
            (self.message_type, f"Your output should contain at most {self.max_tokens} tokens."),
            (self.message_type, "Do not use introduction phrases, just output the description."),
            ("human", "{text}")
        ])

    def get_logging_information(self) -> dict:
        """
        Retrieves logging information specific to the `Descriptor` service.

        Returns
        -------
        dict
            A dictionary containing the `max_tokens` value used in the service.
        """
        return {"max_tokens": self.max_tokens}
