from langchain.prompts import ChatPromptTemplate

from app.services import MinimalService, ServiceTypes


class Tagger(MinimalService):

    @property
    def service_type(self):
        return ServiceTypes.TAGGING

    @property
    def prompt(self):
        return ChatPromptTemplate.from_messages([
            (
                self.message_type,
                """
                You are an AI specialized in extracting key topics, tags, and keywords from text.
                Your task is to generate a concise list of relevant tags that capture the core
                subjects and themes of the provided document.
                """
            ),
            (
                self.message_type,
                """
                Follow these guidelines when generating the tags:
                - Ensure the tags are in the same language as the document
                - Use lowercase words only and avoid punctuation
                - Include between 1 to 4 tags that cover the main subjects of the document
                - Avoid generic words like "document," "content," or "information"
                - Do not repeat tags or include any that are redundant
                """
            ),
            (
                self.message_type,
                """
                You can assume that the generated tags will be used in some sort of search system.
                """
            ),
            (
                self.message_type,
                """
                Output the tags in a comma-separated format, like so:
                tag1, tag2, tag3, ...
                """
            ),
            ("human", "{text}")
        ])
