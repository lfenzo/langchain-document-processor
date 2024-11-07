import hashlib


class FileHasher:
    """
    A utility class for generating unique hashes for documents based on their content.

    The `FileHasher` processes specific parts of the document (the first and last N bytes)
    to create a SHA-256 hash. This allows documents to be identified by their content
    instead of their file name or other metadata.
    """

    def __init__(self, first_n_bytes: int = 512, last_n_bytes: int = 512) -> None:
        """
        Initializes the `FileHasher` with configuration for the number of bytes to hash.

        Parameters
        ----------
        first_n_bytes : int, optional
            The number of bytes to read from the start of the file for hashing (default is 512).
        last_n_bytes : int, optional
            The number of bytes to read from the end of the file for hashing (default is 512).
        """
        self.first_n_bytes = first_n_bytes
        self.last_n_bytes = last_n_bytes

    def hash(self, file_bytes: bytes) -> str:
        """
        Generates a SHA-256 hash for the given file content.

        The hash is based on the concatenation of the first `first_n_bytes` and the last
        `last_n_bytes` of the file content. If the file is smaller than `last_n_bytes`,
        all available bytes are used.

        Parameters
        ----------
        file_bytes : bytes
            The binary content of the file to be hashed.

        Returns
        -------
        str
            The hexadecimal representation of the SHA-256 hash.

        Examples
        --------
        >>> file_hasher = FileHasher(first_n_bytes=256, last_n_bytes=256)
        >>> file_content = b"Example file content for hashing."
        >>> file_hash = file_hasher.hash(file_content)
        >>> print(file_hash)
        'd2d2f6c90f3bd8bce58eb2a6c6a7f9f650a7c9ec16d46a20a0b5b9c9baf3bd8d'
        """
        first_part = file_bytes[:self.first_n_bytes]

        last_part = (
            file_bytes[-self.last_n_bytes:]
            if len(file_bytes) >= self.last_n_bytes else file_bytes
        )

        combined_bytes = first_part + last_part

        sha256 = hashlib.sha256()
        sha256.update(combined_bytes)

        return sha256.hexdigest()
