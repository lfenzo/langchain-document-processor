from typing import Any
from abc import ABC, abstractmethod

from app.models import FeedbackForm


class BaseStoreManager(ABC):
    """
    Abstract base class for implementing storage managers.

    This class defines the required interface for storing and retrieving documents,
    service outputs, and user feedback. Subclasses must implement all abstract methods.
    """

    @abstractmethod
    def get_document_by_id(self, _id: str, **kwargs) -> Any:
        """
        Retrieves a document from the storage system by its unique identifier.

        Parameters
        ----------
        _id : str
            The unique identifier of the document to retrieve.
        **kwargs
            Additional optional parameters for filtering or customization.

        Returns
        -------
        Any
            The retrieved document or metadata.
        """
        pass

    @abstractmethod
    def get_logging_information(self) -> dict:
        """
        Retrieves logging-related metadata for structured logging purposes.

        Returns
        -------
        dict
            A dictionary containing logging metadata such as configuration or state information.
        """
        pass

    @abstractmethod
    def store_service_output(self, _id: str, **kwargs) -> str:
        """
        Stores the output of a service into the storage system.

        Parameters
        ----------
        _id : str
            The unique identifier for the document or artefact to store.
        **kwargs
            Additional data to be stored, such as metadata or service-specific artefacts.

        Returns
        -------
        str
            The ID of the stored item.
        """
        pass

    @abstractmethod
    def store_service_output_feedback(self, _id: str, form: FeedbackForm, **kwargs) -> None:
        """
        Stores user feedback for a specific service output.

        Parameters
        ----------
        _id : str
            The unique identifier of the document associated with the feedback.
        form : FeedbackForm
            A feedback form containing user-provided feedback.
        **kwargs
            Additional data to be stored alongside the feedback.

        Returns
        -------
        None
        """
        pass
