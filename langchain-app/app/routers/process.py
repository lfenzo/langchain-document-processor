import json
from tempfile import NamedTemporaryFile

import magic
from fastapi import APIRouter, File, UploadFile, Response

from app.models import FeedbackForm
from app.services.base import BaseService
from app.factories import StoreManagerFactory
from app.builders.document_processor import DocumentProcessorBuilder
from app.builders.services.summarization.simple import SimpleSummarizerBuilder


router = APIRouter()


@router.post("/summarize")
async def process_summarization(file: UploadFile = File(...)):
    summarization_service = (
        SimpleSummarizerBuilder()
        .set_chatmodel(service='ollama', model='llama3.1')
        .build()
    )
    return await invoke_set_of_services(file=file, services=[summarization_service])


async def invoke_set_of_services(services: list[BaseService], file: UploadFile = File(...)):
    contents = await file.read()

    with NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(contents)
        tmp_file.flush()
        tmp_file.seek(0)  # Ensure the file pointer is at the start

        processor = (
            DocumentProcessorBuilder()
            .set_loader(file_type=magic.from_buffer(contents, mime=True), file_path=tmp_file.name)
            .set_services(services)
            .build()
        )

    service_responses = json.dumps(await processor.execute_all_services())
    return Response(content=service_responses, media_type='application/json')
