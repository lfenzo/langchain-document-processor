from abc import ABC, abstractmethod

from app.models.feedback import FeedbackForm


class BaseStoreManager(ABC):

    @abstractmethod
    def get_artefact(self, _id: str):
        pass

    @abstractmethod
    def store_artefact(self, artefact: str, data: dict) -> str:
        pass

    @abstractmethod
    def store_artefact_feedback(self, form: FeedbackForm):
        pass
