import hashlib
import uuid
from enum import Enum
from typing import Any, List, Union

from pydantic import BaseModel, Extra

Number = Union[int, float]
Embedding = List[Number]
Embeddings = List[Embedding]


class Entity(str, Enum):
    """
    Enum for the different types of entities that can respond to the current message.
    """

    AGENT = "Agent"
    LLM = "LLM"
    USER = "User"


class DocMetaData(BaseModel):
    """Metadata for a document."""

    source: str = "context"

    class Config:
        extra = Extra.allow


class Document(BaseModel):
    """Interface for interacting with a document."""

    content: str
    metadata: DocMetaData

    def _unique_hash_id(self) -> str:
        # Encode the document as UTF-8
        doc_utf8 = str(self).encode("utf-8")

        # Create a SHA256 hash object
        sha256_hash = hashlib.sha256()

        # Update the hash object with the bytes of the document
        sha256_hash.update(doc_utf8)

        # Get the hexadecimal representation of the hash
        hash_hex = sha256_hash.hexdigest()

        # Convert the first part of the hash to a UUID
        hash_uuid = uuid.UUID(hash_hex[:32])

        return str(hash_uuid)

    def id(self) -> Any:
        if hasattr(self.metadata, "id"):
            return self.metadata.id
        else:
            return self._unique_hash_id()

    def __str__(self) -> str:
        # TODO: make metadata a pydantic model to enforce "source"
        self.metadata.json()
        return f"{self.content} {self.metadata.json()}"
