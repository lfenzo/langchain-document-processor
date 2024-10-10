from app.services.service_types import ServiceTypes
from app.services.minimal import MinimalService
from app.services.description.minimal import Descriptor
from app.services.summarization.minimal import Summarizer
from app.services.tagging.minimal import Tagger
from app.services.translation.minimal import Translator


__all__ = [
    'Summarizer',
    'Tagger',
    'Descriptor',
    'MinimalService',
    'ServiceTypes',
    'Translator',
]
