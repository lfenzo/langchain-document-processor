from langchain_core.language_models.chat_models import BaseChatModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_vertexai import ChatVertexAI
from langchain_ollama import ChatOllama


class ChatModelFactory:
    """
    Factory class for creating chat model instances.

    Attributes
    ----------
    available_chatmodel_services : dict
        A dictionary mapping chat model service names (str) to their respective classes.
    """

    def __init__(self) -> None:
        self.available_chatmodel_services = {
            'google-genai': ChatGoogleGenerativeAI,
            'google-vertex': ChatVertexAI,
            'ollama': ChatOllama,
        }

    def create(self, service: str, **kwargs) -> BaseChatModel:
        """
        Create a chat model instance based on the specified chat model type.

        Parameters
        ----------
        service : str
            The chat model service to be used (e.g., 'google-genai').
        **kwargs : dict
            Additional keyword arguments passed to the chat model class.

        Returns
        -------
        BaseChatModel
            The chat model instance created.

        Raises
        ------
        ValueError
            If the specified chat model type is not valid.

        Examples
        --------
        >>> factory = ChatModelFactory()
        >>> chat_model = factory.create('ollama', model='llama3.1')
        """
        if service not in self.available_chatmodel_services:
            raise ValueError(
                f"Invalid chat model '{service}'. "
                f"Valid chat models are: {self.get_valid_chat_models()}"
            )
        return self.available_chatmodel_services[service](**kwargs)

    def get_valid_chatmodel_services(self) -> list[str]:
        """
        Get a list of valid chat models services that can be used.

        Returns
        -------
        list[str]
            A list of valid chat model keys.
        """
        return list(self.available_chatmodel_services.keys())
