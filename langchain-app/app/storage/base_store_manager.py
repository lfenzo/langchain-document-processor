from typing import Any
from abc import ABC, abstractmethod

from app.models import FeedbackForm


class BaseStoreManager(ABC):

    @abstractmethod
    def get_document_by_id(self, _id: str, **kwargs) -> Any:
        pass

    @abstractmethod
    def get_logging_information(self) -> dict:
        pass

    @abstractmethod
    def store_service_output(self, _id: str, **kwargs) -> str:
        pass

    @abstractmethod
    def store_service_output_feedback(self, _id: str, form: FeedbackForm, **kwargs) -> None:
        pass
