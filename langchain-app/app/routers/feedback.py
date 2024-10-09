import os


from fastapi import APIRouter

from app.factories import StoreManagerFactory
from app.models import FeedbackForm


router = APIRouter()


@router.post("/feedback")
async def process_feedback(form: FeedbackForm):
    storage_manager = StoreManagerFactory().create(
        store_manager='mongodb',
        port='27017',
        password=os.environ['MONGO_INITDB_ROOT_PASSWORD'],
        user=os.environ['MONGO_INITDB_ROOT_USERNAME'],
    )
    await storage_manager.store_service_output_feedback(form=form)
    return {'user': form.user, 'id': form.id}
