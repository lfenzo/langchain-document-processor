from langchain.prompts import ChatPromptTemplate

from app.services.minimal import MinimalService


class Descriptor(MinimalService):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service_type = 'description'

    @property
    def prompt(self):
        msg_type = "system" if self.has_system_msg_support else "human"
        return ChatPromptTemplate.from_messages([
            (
                msg_type,
                """
                Generate only a 2 to 3 sentence description of this document in the same language
                as the original document. Make sure to outline the main purpose of the document
                in your description.
                """
            ),
            (
                msg_type,
                """
                Keep the description short regardless of the length of the document.
                """
            ),
            (
                msg_type,
                """
                Do not use introduction phrases, just output the description.
                """
            ),
            ("human", "{text}")
        ])
