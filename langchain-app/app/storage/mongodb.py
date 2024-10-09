from datetime import datetime
from typing import Any
from bson.binary import Binary
from pymongo import MongoClient

from app.models import FeedbackForm
from app.storage import BaseStoreManager


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
    database : Database
        The MongoDB database instance.
    """

    def __init__(
        self,
        user: str,
        password: str,
        port: str = '27017',
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
        self.database = self.client[self.database_name]

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

    @property
    def collection(self):
        return self.database[self.collection_name]

    def get_document_by_id(self, _id: str, exclude_byte_fields: bool = True) -> dict[str, Any]:
        document = self.collection.find_one({"_id": _id})
        if exclude_byte_fields:
            del document['original_document_as_bytes']
        return document

    async def store_service_output(
        self,
        _id: str,
        artefact: str,
        data: dict,
        document: bytes,
        overwrite_existing: bool = False,
    ) -> str:
        document_to_store = Binary(document) if self.document_can_be_stored(document) else None
        existing_document = self.collection.find_one({"_id": _id})

        if not existing_document:
            base_document = {"_id": _id, "original_document_as_bytes": document_to_store}
            self.collection.insert_one(document=base_document)
            existing_document = base_document

        if artefact not in existing_document or overwrite_existing:
            self.collection.update_one({"_id": _id}, {"$set": {artefact: data}})

        return _id

    async def store_service_output_feedback(
        self,
        _id: str,
        service_type: str,
        form: FeedbackForm,
    ) -> int:
        feedback_as_dict = self._set_creation_date(feedback=form.dict())
        insertion_result = self.collection.update_one(
            {"_id": _id},
            {"$push": {f"{service_type}.feedback": feedback_as_dict}}
        )

        if insertion_result.matched_count == 0:
            raise ValueError(f"Failed to insert feedback with {_id=} on {service_type=}")

        return _id

    def _set_creation_date(self, feedback: dict) -> dict:
        if not feedback['created_at']:
            feedback['created_at'] = datetime.now().isoformat()
        return feedback
