from langchain.prompts import ChatPromptTemplate

from app.services import MinimalService, ServiceTypes


class Summarizer(MinimalService):

    def __init__(self, text_percentage: int = 30, **kwargs):
        super().__init__(**kwargs)
        self.text_percentage = text_percentage

    @property
    def service_type(self) -> str:
        return ServiceTypes.SUMMARIZATION

    @property
    def prompt(self):
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
