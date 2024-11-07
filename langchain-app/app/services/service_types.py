from enum import StrEnum


class ServiceTypes(StrEnum):
    """
    Enumeration of supported service types.

    This class defines string-based constants for various service types, enabling
    consistent usage across the application.
    """
    SUMMARIZATION = "summarization"
    DESCRIPTION = "description"
    TAGGING = "tagging"
    TRANSLATION = "translation"
