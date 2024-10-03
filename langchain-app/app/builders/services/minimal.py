from langchain_core.language_models.chat_models import BaseChatModel

from app.builders.services.base import BaseServiceBuilder
from app.services.minimal import MinimalService
from app.services.summarization.minimal import Summarizer
from app.services.description.minimal import Descriptor


class MinimalServiceBuilder(BaseServiceBuilder):
    DEFAULT_CHATMODEL_SERVICE = 'ollama'
    DEFAULT_CHATMODEL_KWARGS = {
        'model': 'llama3.1',
        'base_url': 'http://ollama-server:11434',
    }

    MINIMAL_SERVICES = {
        'summarization': Summarizer,
        'description': Descriptor,
    }

    def __init__(self, service: str) -> None:
        super().__init__()
        self.service = service
        self.chatmodel = self._create_default_chatmodel()
        self.has_system_msg_support = False

    def build(self) -> MinimalService:
        return self.MINIMAL_SERVICES[self.service](**self.get_init_params())

    def get_init_params(self) -> dict:
        return {
            "chatmodel": self.chatmodel,
            "has_system_msg_support": self.has_system_msg_support,
        }

    def set_chatmodel(self, service: str, chatmodel: BaseChatModel = None, **kwargs):
        combined_kwargs = {**self.DEFAULT_CHATMODEL_KWARGS, **kwargs}
        self.chatmodel = self._create_chatmodel(
            service=service, chatmodel=chatmodel, **combined_kwargs
        )
        return self

    def set_system_msg_support(self, has_system_msg_support: bool):
        self.has_system_msg_support = has_system_msg_support
        return self

    def _create_default_chatmodel(self) -> BaseChatModel:
        return self._create_chatmodel(
            service=self.DEFAULT_CHATMODEL_SERVICE, **self.DEFAULT_CHATMODEL_KWARGS
        )
