import json
from tempfile import NamedTemporaryFile

import magic
from fastapi import APIRouter, File, UploadFile, Response, Query

from app.services.base import BaseService
from app.builders.document_processor import DocumentProcessorBuilder
from app.factories import CacheFactory, ChatModelFactory, ServiceFactory
from app.services.service_types import ServiceTypes

router = APIRouter()
service_factory = ServiceFactory()

OLLAMA_SERVER_URL = 'http://ollama-server:11434'


@router.post('/summarization')
async def process_summarization(
    text_percentage: int = Query(default=30),
    file: UploadFile = File(...)
):
    service = service_factory.create_minimal_service(
        service=ServiceTypes.SUMMARIZATION,
        chatmodel=ChatModelFactory().create(
            service='ollama',
            model='llama3.1',
            base_url=OLLAMA_SERVER_URL,
        ),
        has_system_msg_support=False,
        text_percentage=text_percentage,
    )
    return await invoke_service_set(file=file, services=[service])


@router.post('/description')
async def process_description(max_tokens: int = Query(default=85), file: UploadFile = File(...)):
    service = service_factory.create_minimal_service(
        service=ServiceTypes.DESCRIPTION,
        chatmodel=ChatModelFactory().create(
            service='google-genai',
            model='gemini-1.5-flash',
            cache=CacheFactory().create(cache='redis'),
        ),
        max_tokens=max_tokens,
    )
    return await invoke_service_set(file=file, services=[service])


@router.post('/tagging')
async def process_tagging(file: UploadFile = File(...)):
    service = service_factory.create_minimal_service(
        service=ServiceTypes.TAGGING,
        chatmodel=ChatModelFactory().create(
            service='ollama',
            model='llama3.1',
            base_url=OLLAMA_SERVER_URL,
        ),
        has_system_msg_support=True,
    )
    return await invoke_service_set(file=file, services=[service])


@router.post('/translation')
async def process_translation(
    target_language: str = Query(default='portugues'),
    file: UploadFile = File(...)
):
    service = service_factory.create_minimal_service(
        service=ServiceTypes.TRANSLATION,
        chatmodel=ChatModelFactory().create(
            service='ollama',
            model='llama3.1',
            base_url=OLLAMA_SERVER_URL,
        ),
        has_system_msg_support=True,
        target_language=target_language,
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

    service_responses = json.dumps(await processor.execute_services())
    return Response(content=service_responses, media_type='application/json')
