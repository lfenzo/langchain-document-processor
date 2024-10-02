import hashlib


class FileHasher:

    def __init__(self, first_n_bytes: int = 512, last_n_bytes: int = 512) -> None:
        self.first_n_bytes = first_n_bytes
        self.last_n_bytes = last_n_bytes

    def generate_file_hash(self, file_bytes: bytes) -> str:
        first_part = file_bytes[:self.first_n_bytes]

        last_part = (
            file_bytes[-self.last_n_bytes:]
            if len(file_bytes) >= self.last_n_bytes else file_bytes
        )

        combined_bytes = first_part + last_part

        sha256 = hashlib.sha256()
        sha256.update(combined_bytes)

        return sha256.hexdigest()
