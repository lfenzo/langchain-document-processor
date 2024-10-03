from langchain_core.document_loaders import BaseLoader
from langchain_core.documents.base import Document
from langchain_core.messages.ai import AIMessage

from app.services.base import BaseService
from app.storage.base_store_manager import BaseStoreManager
from app.storage.file_hasher import FileHasher


class DocumentProcessor:

    def __init__(
        self,
        loader: BaseLoader,
        store_manager: BaseStoreManager,
        services: list[BaseService] = None,
    ) -> None:
        self.loader = loader
        self.store_manager = store_manager
        self.services = services
        self.hasher = FileHasher()

    @property
    def file_path(self) -> str:
        has_blob_perser = hasattr(self.loader, 'blob_parser')
        return self.loader.blob_loader.path if has_blob_perser else self.loader.file_path

    @property
    def file_hash(self) -> str:
        return self.hasher.hash(file_bytes=self.file_as_bytes)

    @property
    def file_as_bytes(self) -> bytes:
        with open(self.file_path, 'rb') as file:
            return file.read()

    @property
    def file_content(self):
        return self.loader.load()

    async def execute_all_services(self) -> dict:
        for service in self.services:
            await self._execute_service_on_content(service=service, content=self.file_content)
        return self.store_manager.get_document_by_id(_id=self.file_hash)

    async def _execute_service_on_content(self, service: BaseService, content: list[Document]):
        generated: AIMessage = await service.run(content=content)

        artefact_data = {
            '_id': generated.id,
            'metadata': service.get_metadata(file=self.file_path, gen_metadata=generated),
            'content': generated.content,
            'feedback': None,
        }

        await self.store_manager.store_service_output(
            _id=self.file_hash,
            artefact=service.service_type,
            data=artefact_data,
            document=self.file_as_bytes,
            overwrite_existing=True,
        )
