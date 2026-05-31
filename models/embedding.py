from sqlalchemy import Column, Integer, Text, DateTime, func, ForeignKey
from pgvector.sqlalchemy import Vector
from .document import Base


class Embedding(Base):
    """Stores text chunks and their vector embeddings."""

    __tablename__ = "embeddings"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), index=True)
    chunk_index = Column(Integer)
    text = Column(Text)
    embedding = Column(Vector(1536))  # OpenAI text-embedding-3-small is 1536 dims
    created_at = Column(DateTime, server_default=func.now())
