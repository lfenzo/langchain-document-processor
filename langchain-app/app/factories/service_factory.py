from app.services import Summarizer, ServiceTypes, Descriptor, Tagger, Translator, MinimalService


class ServiceFactory:

    MINIMAL_SERVICES = {
        ServiceTypes.SUMMARIZATION: Summarizer,
        ServiceTypes.DESCRIPTION: Descriptor,
        ServiceTypes.TAGGING: Tagger,
        ServiceTypes.TRANSLATION: Translator,
    }

    def create_minimal_service(self, service: str, **kwargs) -> MinimalService:
        return self.MINIMAL_SERVICES[service](**kwargs)

    def create_custom_service(self, service: str, **kwargs):
        pass
