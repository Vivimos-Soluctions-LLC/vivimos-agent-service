from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
from config import settings
from models import Base, Document
from services import ingest_document, chat_with_document

# Create FastAPI app
app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
    debug=settings.debug,
)

# Database setup
engine = create_engine(settings.database_url, echo=settings.sqlalchemy_echo)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
async def startup_event():
    """Create all tables on startup."""
    Base.metadata.create_all(bind=engine)


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "service": "Vivimos Agent Service",
        "status": "running",
        "version": settings.api_version,
    }


@app.post("/ingest")
async def ingest(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """
    POST /ingest: Upload and process a PDF document.

    Accepts a PDF file, extracts text, generates embeddings, and stores in pgvector.
    Returns the created document record with chunk count.
    """
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    file_bytes = await file.read()

    if len(file_bytes) == 0:
        raise HTTPException(status_code=400, detail="Uploaded file is empty")

    document = ingest_document(db=db, filename=file.filename, file_bytes=file_bytes)

    # Count embeddings stored for this document
    from models import Embedding
    chunk_count = db.query(Embedding).filter(Embedding.document_id == document.id).count()

    return {
        "document_id": document.id,
        "filename": document.filename,
        "file_size": document.file_size,
        "chunks_stored": chunk_count,
        "status": "ingested",
    }


class ChatRequest(BaseModel):
    query: str
    document_id: int


@app.post("/chat")
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    """POST /chat: Query a document with an AI agent using vector similarity search."""
    document = db.query(Document).filter(Document.id == request.document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    answer = chat_with_document(db=db, document_id=request.document_id, query=request.query)

    return {
        "document_id": request.document_id,
        "query": request.query,
        "answer": answer,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
    )
