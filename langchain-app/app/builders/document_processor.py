from langchain_core.document_loaders import BaseLoader

from app.factories import LoaderFactory, StoreManagerFactory
from app.storage import BaseStoreManager
from app.document_processor import DocumentProcessor


class DocumentProcessorBuilder:
    DEFAULT_STORE_MANAGER_USER = 'root'
    DEFAULT_STORE_MANAGER_PORT = '27017'
    DEFAULT_STORE_MANAGER_PASSWORD = 'password'
    DEFAULT_STORE_MANAGER_SERVICE = 'mongodb'

    def __init__(self) -> None:
        self.loader = None
        self.services = []
        self.store_manager = self._create_default_store_manager()

    def build(self):
        if not self.loader:
            raise ValueError("Cannot instantiate DocumentProcessor object without a Loader.")
        if not self.services:
            raise ValueError("Cannot instantiate DocumentProcessor object without services.")
        return DocumentProcessor(**self.get_init_params())

    def get_init_params(self):
        return {
            'loader': self.loader,
            'store_manager': self.store_manager,
            'services': self.services,
        }

    def set_services(self, services):
        self.services = services
        return self

    def set_loader(self, file_type: str = None, file_path: str = None, loader: BaseLoader = None):
        self.loader = (
            loader if loader is not None
            else LoaderFactory().create(file_type=file_type, file_path=file_path)
        )
        return self

    def set_store_manager(self, store_manager: str | BaseStoreManager, **kwargs):
        self.store_manager = (
            store_manager if isinstance(store_manager, BaseStoreManager)
            else StoreManagerFactory().create(store_manager=store_manager, **kwargs)
        )
        return self

    def _create_default_store_manager(self) -> BaseStoreManager:
        return StoreManagerFactory().create(
            store_manager=self.DEFAULT_STORE_MANAGER_SERVICE,
            user=self.DEFAULT_STORE_MANAGER_USER,
            password=self.DEFAULT_STORE_MANAGER_PASSWORD,
            port=self.DEFAULT_STORE_MANAGER_PORT,
        )
