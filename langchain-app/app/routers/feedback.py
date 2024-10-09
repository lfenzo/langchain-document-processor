import os


from fastapi import APIRouter, Query

from app.factories import StoreManagerFactory
from app.models import FeedbackForm


router = APIRouter()


@router.post("/feedback")
async def process_feedback(
    form: FeedbackForm,
    _id: str = Query(..., description="Document ID."),
    service_type: str = Query(..., description='Service type for which the feedback is stored.'),
):
    storage_manager = StoreManagerFactory().create(
        store_manager='mongodb',
        port='27017',
        password=os.environ['MONGO_INITDB_ROOT_PASSWORD'],
        user=os.environ['MONGO_INITDB_ROOT_USERNAME'],
    )

    return await storage_manager.store_service_output_feedback(
        _id=_id,
        service_type=service_type,
        form=form
    )
