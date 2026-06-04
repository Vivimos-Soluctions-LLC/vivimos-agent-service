"""Chat pipeline: query → vector search → LLM response."""

from sqlalchemy.orm import Session
from sqlalchemy import text
from config import settings
from .embedder import _get_client as get_openai_client, EMBEDDING_MODEL


def _embed_query(query: str) -> list[float]:
    client = get_openai_client()
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=[query])
    return response.data[0].embedding


def _find_relevant_chunks(db: Session, document_id: int, query_embedding: list[float], top_k: int = 5) -> list[str]:
    vector_literal = "[" + ",".join(str(x) for x in query_embedding) + "]"
    result = db.execute(
        text(
            "SELECT text FROM embeddings "
            "WHERE document_id = :doc_id "
            "ORDER BY embedding <-> CAST(:embedding AS vector) "
            "LIMIT :k"
        ),
        {"doc_id": document_id, "embedding": vector_literal, "k": top_k},
    )
    return [row[0] for row in result]


def chat_with_document(db: Session, document_id: int, query: str) -> str:
    query_embedding = _embed_query(query)
    chunks = _find_relevant_chunks(db, document_id, query_embedding)

    if not chunks:
        return "No relevant content found in this document."

    context = "\n\n---\n\n".join(chunks)
    client = get_openai_client()

    response = client.chat.completions.create(
        model="gpt-4o",
        max_tokens=1024,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant. Answer the user's question using only "
                    "the provided document excerpts. If the answer is not in the excerpts, say so."
                ),
            },
            {
                "role": "user",
                "content": f"Document excerpts:\n\n{context}\n\nQuestion: {query}",
            },
        ],
    )

    return response.choices[0].message.content
