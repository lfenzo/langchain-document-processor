from typing import Any
from bson import ObjectId
from bson.binary import Binary
from pymongo import MongoClient

from app.models import FeedbackForm
from app.storage import BaseStoreManager, FileHasher


# currently mongodb can only store document of up to 16MB in size
MAX_DOCUMENT_SIZE_IN_BYTES = 16_793_598  # obtained from pymongo error message (~16MB)


class MongoDBStoreManager(BaseStoreManager):
    """
    MongoDB-based implementation of the BaseStoreManager for storing summaries and feedback.

    This class manages the storage of summary documents and metadata in a MongoDB collection.

    Attributes
    ----------
    database_name : str
        The name of the MongoDB database used for storing summaries.
    collection_name : str
        The name of the MongoDB collection used for storing summaries.
    client : MongoClient
        The MongoDB client used to connect to the database.
    db : Database
        The MongoDB database instance.
    """

    def __init__(
        self,
        user: str,
        password: str,
        port: str,
        database_name: str = 'document_processor',
        collection_name: str = 'documents',
    ) -> None:
        """
        Initializes the MongoDBStoreManager with database and collection settings.

        Parameters
        ----------
        user : str, optional
            The username for connecting to MongoDB (default is 'root').
        password : str, optional
            The password for connecting to MongoDB (default is 'password').
        port : str, optional
            The port for connecting to MongoDB (default is '27017').
        database_name : str, optional
            The name of the MongoDB database to use (default is 'summary_database').
        collection_name : str, optional
            The name of the MongoDB collection to use (default is 'summaries').
        """
        connection_string = self.get_connection_string(user=user, password=password, port=port)
        self.database_name = database_name
        self.collection_name = collection_name
        self.client = MongoClient(connection_string)
        self.db = self.client[self.database_name]

    def get_connection_string(self, user: str, password: str, port: str) -> str:
        """
        Constructs the MongoDB connection string.

        Parameters
        ----------
        user : str
            The username for connecting to MongoDB.
        password : str
            The password for connecting to MongoDB.
        port : str
            The port for connecting to MongoDB.

        Returns
        -------
        str
            The MongoDB connection string.
        """
        return f"mongodb://{user}:{password}@mongodb:{port}/"

    def document_can_be_stored(self, document: bytes) -> bool:
        """
        Checks if the document can be stored based on its size.

        MongoDB has a size limit of 16MB for documents.

        Parameters
        ----------
        document : bytes
            The document to check.

        Returns
        -------
        bool
            True if the document size is within the limit, otherwise False.
        """
        return len(document) <= MAX_DOCUMENT_SIZE_IN_BYTES

    def _get_summary_document_by_id(self, document_id: str) -> dict[str, Any]:
        collection = self.db[self.collection_name]
        document = collection.find_one({"_id": ObjectId(document_id)})
        return document

    def get_artefact(self, **kwargs):
        return self._get_summary_document_by_id(**kwargs)

    async def store_artefact(self, artefact: str, data: dict, document: bytes) -> str:
        document_hash = FileHasher().generate_file_hash(file_bytes=document)
        document_to_store = Binary(document) if self.document_can_be_stored(document) else None
        collection = self.db[self.collection_name]

        existing_document = collection.find_one({"_id": document_hash})

        if not existing_document:
            base_document = {"_id": document_hash, "original_document_as_bytes": document_to_store}
            collection.insert_one(document=base_document)

        if artefact not in existing_document:
            collection.update_one({"_id": document_hash}, {"$set": {artefact: data}})

        return document_hash

    async def store_artefact_feedback(self, form: FeedbackForm) -> None:
        collection = self.db[self.collection_name]

        feedback_dict = {
            key: value
            for key, value in form.dict().items() if key != 'document_id'
        }

        update_result = collection.update_one(
            {"_id": form.document_id},
            {"$set": {"feedback": feedback_dict}}
        )

        if update_result.matched_count == 0:
            raise ValueError(f"Failed to update document with ObjectId '{form.document_id}'")
