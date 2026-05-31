"""Generate text embeddings using OpenAI text-embedding-3-small."""

from typing import List
from openai import OpenAI
from config import settings


EMBEDDING_MODEL = "text-embedding-3-small"
EMBEDDING_DIMS = 1536

_client = None


def _get_client() -> OpenAI:
    global _client
    if _client is None:
        _client = OpenAI(api_key=settings.openai_api_key)
    return _client


def embed_chunks(chunks: List[dict]) -> List[dict]:
    """
    Add an 'embedding' list to each chunk dict.

    Args:
        chunks: List of dicts with 'chunk_index' and 'text' keys

    Returns:
        Same list with 'embedding' key added (list of 1536 floats)
    """
    if not chunks:
        return chunks

    texts = [c["text"] for c in chunks]
    client = _get_client()

    response = client.embeddings.create(model=EMBEDDING_MODEL, input=texts)

    for chunk, item in zip(chunks, response.data):
        chunk["embedding"] = item.embedding

    return chunks
