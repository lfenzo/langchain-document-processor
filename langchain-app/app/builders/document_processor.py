from langchain_core.document_loaders import BaseLoader

from app.factories import LoaderFactory, StoreManagerFactory
from app.storage import BaseStoreManager
from app.document_processor import DocumentProcessor


class DocumentProcessorBuilder:
    """
    A builder class for constructing a `DocumentProcessor` instance with customizable components.

    This class provides methods to configure a `Loader`, `StoreManager`, and a list of `services`.
    It ensures that all required components are set before building the `DocumentProcessor`.
    """

    DEFAULT_STORE_MANAGER_USER = 'root'
    DEFAULT_STORE_MANAGER_PORT = '27017'
    DEFAULT_STORE_MANAGER_PASSWORD = 'password'
    DEFAULT_STORE_MANAGER_SERVICE = 'mongodb'

    def __init__(self) -> None:
        """
        Initializes a new `DocumentProcessorBuilder` with default configurations.

        Attributes
        ----------
        loader : BaseLoader or None
            The loader instance or None if not set.
        services : list
            A list of service configurations to be used by the `DocumentProcessor`.
        store_manager : BaseStoreManager
            The store manager instance, initialized with default settings.
        """
        self.loader = None
        self.services = []
        self.store_manager = self._create_default_store_manager()

    def build(self):
        """
        Constructs and returns a `DocumentProcessor` instance.

        Returns
        -------
        DocumentProcessor
            An instance of `DocumentProcessor` initialized with the configured parameters.

        Raises
        ------
        ValueError
            If `loader` or `services` are not set.
        """
        if not self.loader:
            raise ValueError("Cannot instantiate DocumentProcessor object without a Loader.")
        if not self.services:
            raise ValueError("Cannot instantiate DocumentProcessor object without 'services'.")
        return DocumentProcessor(**self.get_init_params())

    def get_init_params(self):
        """
        Retrieves the initialization parameters for the `DocumentProcessor`.

        Returns
        -------
        dict
            A dictionary containing the loader, store manager, and services.
        """
        return {
            'loader': self.loader,
            'store_manager': self.store_manager,
            'services': self.services,
        }

    def set_services(self, services):
        """
        Configures the services for the `DocumentProcessor`.

        Parameters
        ----------
        services : list
            A list of service configurations.

        Returns
        -------
        DocumentProcessorBuilder
            The current builder instance for method chaining.
        """
        self.services = services
        return self

    def set_loader(self, file_type: str = None, file_path: str = None, loader: 'BaseLoader' = None):
        """
        Sets the loader instance or creates one using the `LoaderFactory`.

        Parameters
        ----------
        file_type : str, optional
            The type of the file to be processed.
        file_path : str, optional
            The path to the file to be processed.
        loader : BaseLoader, optional
            A pre-existing loader instance. If provided, it overrides the factory-based creation.

        Returns
        -------
        DocumentProcessorBuilder
            The current builder instance for method chaining.
        """
        self.loader = (
            loader if loader is not None
            else LoaderFactory().create(file_type=file_type, file_path=file_path)
        )
        return self

    def set_store_manager(self, store_manager: str | BaseStoreManager, **kwargs):
        """
        Sets the store manager instance or creates one using the `StoreManagerFactory`.

        Parameters
        ----------
        store_manager : str or BaseStoreManager
            A pre-existing store manager instance or the type of store manager to be created.
        **kwargs
            Additional parameters to pass to the `StoreManagerFactory` when creating the store manager.

        Returns
        -------
        DocumentProcessorBuilder
            The current builder instance for method chaining.
        """
        self.store_manager = (
            store_manager if isinstance(store_manager, BaseStoreManager)
            else StoreManagerFactory().create(store_manager=store_manager, **kwargs)
        )
        return self

    def _create_default_store_manager(self) -> BaseStoreManager:
        """
        Creates a default `BaseStoreManager` instance with predefined configurations.

        Returns
        -------
        BaseStoreManager
            The default store manager instance.
        """
        return StoreManagerFactory().create(
            store_manager=self.DEFAULT_STORE_MANAGER_SERVICE,
            user=self.DEFAULT_STORE_MANAGER_USER,
            password=self.DEFAULT_STORE_MANAGER_PASSWORD,
            port=self.DEFAULT_STORE_MANAGER_PORT,
        )
