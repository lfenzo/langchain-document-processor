import json
from tempfile import NamedTemporaryFile

import magic
from fastapi import APIRouter, File, UploadFile, Response

from app.services.base import BaseService
from app.builders.document_processor import DocumentProcessorBuilder
from app.builders.services.minimal import MinimalServiceBuilder
from app.factories.cache_factory import CacheFactory


router = APIRouter()


@router.post("/summarization")
async def process_summarization(file: UploadFile = File(...)):
    return await invoke_standalone_service(file=file, service='summarization')


@router.post('/description')
async def process_description(file: UploadFile = File(...)):
    return await invoke_standalone_service(file=file, service='description')


async def invoke_standalone_service(file: UploadFile, service: str, **kwargs):
    service = (
        MinimalServiceBuilder(service=service)
        .set_chatmodel(
            service='google-genai',
            model='gemini-1.5-pro',
            cache=CacheFactory().create('redis'),
        )
        .set_system_msg_support(False)
        .build()
    )
    return await invoke_service_set(file=file, services=[service])


async def invoke_service_set(services: list[BaseService], file: UploadFile = File(...)):
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
