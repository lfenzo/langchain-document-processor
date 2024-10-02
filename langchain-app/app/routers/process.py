from tempfile import NamedTemporaryFile

import magic
from fastapi import APIRouter, File, UploadFile

from app.models import FeedbackForm
from app.factories import StoreManagerFactory
from app.builders.document_processor import DocumentProcessorBuilder
from app.builders.services.summarization.simple import SimpleSummarizerBuilder


router = APIRouter()


@router.post("/summarize")
async def invoke_summarize(file: UploadFile = File(...)):
    contents = await file.read()

    with NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(contents)
        tmp_file.flush()
        tmp_file.seek(0)  # Ensure the file pointer is at the start

        summarization_service = (
            SimpleSummarizerBuilder()
            .set_chatmodel(service='ollama', model='llama3.1')
            .build()
        )

        processor = (
            DocumentProcessorBuilder()
            .set_loader(file_type=magic.from_buffer(contents, mime=True), file_path=tmp_file.name)
            .set_services([summarization_service])
            .build()
        )

    return await processor.execute_all_services()
