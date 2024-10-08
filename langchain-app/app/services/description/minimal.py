from langchain.prompts import ChatPromptTemplate

from app.services import MinimalService, ServiceTypes


class Descriptor(MinimalService):

    @property
    def service_type(self) -> str:
        return ServiceTypes.DESCRIPTION

    @property
    def prompt(self):
        return ChatPromptTemplate.from_messages([
            (
                self.message_type,
                """
                Generate only a 2 to 3 sentence description of this document in the same language
                as the original document. Make sure to outline the main purpose of the document
                in your description.
                """
            ),
            (self.message_type, "Your output should contain at most 150 tokens."),
            (self.message_type, "Do not use introduction phrases, just output the description."),
            ("human", "{text}")
        ])
