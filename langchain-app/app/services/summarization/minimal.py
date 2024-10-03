from langchain.prompts import ChatPromptTemplate

from app.services.minimal import MinimalService


class Summarizer(MinimalService):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service_type = 'summary'

    @property
    def prompt(self):
        msg_type = "system" if self.has_system_msg_support else "human"
        return ChatPromptTemplate.from_messages([
            (
                msg_type,
                """
                You are an AI specialized in multi-language summaries. Your task is to summarize
                the provided text by focusing on the key points, central themes, and significant
                details.
                """
            ),
            (
                msg_type,
                """
                Ensure the summary is approximately 30% of the original text length. Avoid
                superficial details or unnecessary information.
                """
            ),
            (
                msg_type,
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
