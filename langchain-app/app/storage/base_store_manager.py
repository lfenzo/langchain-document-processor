from typing import Any
from abc import ABC, abstractmethod

from app.models import FeedbackForm


class BaseStoreManager(ABC):

    @abstractmethod
    def get_document_by_id(self, _id: str, **kwargs) -> Any:
        pass

    @abstractmethod
    def store_service_output(self, artefact: str, data: dict, **kwargs) -> str:
        pass

    @abstractmethod
    def store_service_output_feedback(self, form: FeedbackForm) -> None:
        pass
