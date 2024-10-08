from abc import ABC, abstractmethod
from typing import Any, Dict

from langchain_core.documents.base import Document
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages.ai import AIMessage
from langchain_core.runnables.base import Runnable

from app.services.base import BaseService


class MinimalService(BaseService, ABC):

    def __init__(self, chatmodel: BaseChatModel, has_system_msg_support: bool = False):
        self.chatmodel = chatmodel
        self.has_system_msg_support = has_system_msg_support

    @property
    @abstractmethod
    def prompt(self):
        ...

    @property
    @abstractmethod
    def service_type(self) -> str:
        ...

    @property
    def message_type(self):
        return "system" if self.has_system_msg_support else "human"

    @property
    def runnable(self, **kwargs) -> Runnable:
        return self.prompt | self.chatmodel

    def run(self, content: list[Document]) -> AIMessage:
        return self.runnable.ainvoke({"text": self._get_text_from_content(content=content)})

    def get_metadata(self, file: str, gen_metadata: Dict) -> Dict[str, Any]:
        metadata = self._get_base_metadata(file=file, gen_metadata=gen_metadata)
        metadata.update({
            'service_type': self.service_type,
            'chatmodel': repr(self.chatmodel),
            'prompt': repr(self.prompt),
            'has_system_msg_support': self.has_system_msg_support,
        })
        return metadata
