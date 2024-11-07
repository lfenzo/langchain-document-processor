from app.services import Summarizer, ServiceTypes, Descriptor, Tagger, Translator, MinimalService


class ServiceFactory:
    """
    A factory class for creating service instances, both minimal and custom.

    This class supports the creation of predefined minimal services and allows
    the customization of services through additional configurations.
    """

    MINIMAL_SERVICES = {
        ServiceTypes.SUMMARIZATION: Summarizer,
        ServiceTypes.DESCRIPTION: Descriptor,
        ServiceTypes.TAGGING: Tagger,
        ServiceTypes.TRANSLATION: Translator,
    }

    def create_minimal_service(self, service: str, **kwargs) -> MinimalService:
        """
        Creates a minimal service instance based on the predefined mappings.

        Parameters
        ----------
        service : str
            The type of service to create, as defined in `ServiceTypes`.
        **kwargs
            Additional keyword arguments passed to the service constructor.

        Returns
        -------
        MinimalService
            An instance of the minimal service corresponding to the specified type.

        Raises
        ------
        KeyError
            If the specified service type is not defined in `MINIMAL_SERVICES`.
        """
        return self.MINIMAL_SERVICES[service](**kwargs)

    def create_custom_service(self, service: str, **kwargs):
        """
        Creates a custom service instance based on the specified type and parameters.

        This method is a placeholder and should be implemented to handle
        custom service creation logic.

        Parameters
        ----------
        service : str
            The type of custom service to create.
        **kwargs
            Additional keyword arguments to configure the custom service.

        Returns
        -------
        Any
            The created custom service instance.
        """
        pass
