from abc import ABC, abstractmethod

from langchain_core.language_models.chat_models import BaseChatModel

from app.factories import ChatModelFactory


class BaseServiceBuilder(ABC):

    @abstractmethod
    def build(self):
        pass

    @abstractmethod
    def get_init_params(self):
        pass

    def _create_chatmodel(self, service: str, chatmodel: BaseChatModel = None, **kwargs):
        return (
            chatmodel if isinstance(chatmodel, BaseChatModel)
            else ChatModelFactory().create(chatmodel=service, **kwargs)
        )
