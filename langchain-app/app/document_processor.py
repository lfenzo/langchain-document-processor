from langchain_core.document_loaders import BaseLoader
from langchain_core.documents.base import Document
from langchain_core.messages.ai import AIMessage


from app.storage.base_store_manager import BaseStoreManager
from app.services.base import BaseService


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

    @property
    def file_path(self) -> str:
        has_blob_perser = hasattr(self.loader, 'blob_parser')
        return self.loader.blob_loader.path if has_blob_perser else self.loader.file_path

    @property
    def file_as_bytes(self) -> bytes:
        with open(self.file_path, 'rb') as file:
            return file.read()

    async def execute_all_services(self) -> None:
        content = self.loader.load()
        for service in self.services:
            await self._execute_service(service=service, content=content)

    async def _execute_service(self, service: BaseService, content: list[Document]):
        generated: AIMessage = await service.run(content=content)

        artefact_data = {
            '_id': generated.id,
            'metadata': service.get_metadata(file=self.file_path, gen_metadata=generated),
            'content': generated.content,
            'feedback': None,
        }

        await self.store_manager.store_artefact(
            artefact=service.service_type, data=artefact_data, document=self.file_as_bytes,
        )
