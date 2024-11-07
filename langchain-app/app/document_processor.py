from langchain_core.document_loaders import BaseLoader
from langchain_core.documents.base import Document
from langchain_core.messages.ai import AIMessage

from app.logger import global_logger
from app.services.base import BaseService
from app.storage.base_store_manager import BaseStoreManager
from app.storage.file_hasher import FileHasher


class DocumentProcessor:
    """
    A class for processing documents through a sequence of services.

    The `DocumentProcessor` manages the loading, hashing, and execution of services
    on a document. It also handles storage of the generated outputs and metadata.

    Attributes
    ----------
    loader : BaseLoader
        The loader used to extract content from the document.
    store_manager : BaseStoreManager
        The storage manager for saving and retrieving document-related data.
    services : list[BaseService]
        A list of services to apply to the document.
    hasher : FileHasher
        Utility for generating a hash to uniquely identify the document.
    logger : Any
        A logger instance for tracking the processing and service execution.
    """

    def __init__(
        self,
        loader: BaseLoader,
        store_manager: BaseStoreManager,
        services: list[BaseService] = None,
    ) -> None:
        """
        Initializes the `DocumentProcessor` with its loader, store manager, and services.

        Parameters
        ----------
        loader : BaseLoader
            The loader instance to extract document content.
        store_manager : BaseStoreManager
            The storage manager for managing document data.
        services : list[BaseService], optional
            A list of services to apply to the document (default is None).
        """
        self.loader = loader
        self.store_manager = store_manager
        self.services = services or []
        self.hasher = FileHasher()
        self.logger = global_logger.bind(_id=self.file_hash, number_of_services=len(self.services))

    @property
    def file_path(self) -> str:
        """
        Retrieves the file path of the document.

        Returns
        -------
        str
            The file path of the document.
        """
        has_blob_parser = hasattr(self.loader, 'blob_parser')
        return self.loader.blob_loader.path if has_blob_parser else self.loader.file_path

    @property
    def file_hash(self) -> str:
        """
        Generates a hash for the document based on its content.

        Returns
        -------
        str
            A SHA-256 hash representing the document's content.
        """
        return self.hasher.hash(file_bytes=self.file_as_bytes)

    @property
    def file_as_bytes(self) -> bytes:
        """
        Reads the document content as bytes.

        Returns
        -------
        bytes
            The binary content of the document.
        """
        with open(self.file_path, 'rb') as file:
            return file.read()

    @property
    def file_content(self) -> list[Document]:
        """
        Loads the document content using the configured loader.

        Returns
        -------
        list[Document]
            A list of `Document` objects extracted from the file.
        """
        return self.loader.load()

    async def execute_services(self) -> dict:
        """
        Executes all configured services on the document and stores their outputs.

        Returns
        -------
        dict
            A dictionary representing the document's metadata and stored artefacts.

        Notes
        -----
        This method logs the progress of each service execution and stores
        the generated data in the storage manager.
        """
        self.logger.info("Starting sequence of services on document")
        self.logger.info("Loading content from file", file_path=self.file_path)
        file_content = self.file_content

        for i, service in enumerate(self.services):
            service_logger = self.logger.bind(
                service_type=service.service_type,
                service_number=i + 1,
            )

            service.set_logger(service_logger)
            await self._execute_service_on_content(service=service, content=file_content)

        return self.store_manager.get_document_by_id(_id=self.file_hash)

    async def _execute_service_on_content(self, service: BaseService, content: list[Document]):
        """
        Executes a single service on the document content.

        Parameters
        ----------
        service : BaseService
            The service to execute.
        content : list[Document]
            A list of `Document` objects to process.

        Notes
        -----
        This method logs the execution progress and stores the generated outputs
        in the storage manager.
        """
        service.logger.info(
            "Starting service execution over the loaded content",
            **service.get_logging_information()
        )

        generated: AIMessage = await service.run(content=content)
        service.logger.info(
            "Finished service LLM generation",
            generated_id=generated.id,
            **service.get_logging_information()
        )

        artefact_data = {
            '_id': generated.id,
            'metadata': service.get_metadata(file=self.file_path, gen_metadata=generated),
            'content': generated.content,
            'feedback': [],
        }

        service.logger.info(
            "Storing artefacts to database",
            **self.store_manager.get_logging_information()
        )
        await self.store_manager.store_service_output(
            _id=self.file_hash,
            artefact=service.service_type,
            data=artefact_data,
            document=self.file_as_bytes,
            overwrite_existing=True,
        )
