from abc import ABC, abstractmethod

from langchain_core.caches import BaseCache
from langchain_core.language_models.chat_models import BaseChatModel

from app.factories import CacheFactory, ChatModelFactory


class BaseServiceBuilder(ABC):
    DEFAULT_CACHE_SERVICE = 'redis'
    DEFAULT_CACHE_HOST = 'redis'
    DEFAULT_CACHE_PORT = 6379

    def __init__(self):
        self.cache = self._create_default_cache()

    @abstractmethod
    def build(self):
        pass

    @abstractmethod
    def get_init_params(self):
        pass

    def set_cache(self, cache: str | BaseCache, **kwargs):
        self.cache = (
            cache if isinstance(cache, BaseCache)
            else CacheFactory().create(cache=cache, **kwargs)
        )
        return self

    def _create_chatmodel(self, service: str, chatmodel: BaseChatModel = None, **kwargs):
        return (
            chatmodel if isinstance(chatmodel, BaseChatModel)
            else ChatModelFactory().create(chatmodel=service, cache=self.cache, **kwargs)
        )

    def _create_default_cache(self) -> BaseCache:
        return CacheFactory().create(
            cache=self.DEFAULT_CACHE_SERVICE,
            host=self.DEFAULT_CACHE_HOST,
            port=self.DEFAULT_CACHE_PORT
        )
