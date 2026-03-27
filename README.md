# Vivimos Agent Service

FastAPI microservice for RAG-based document intelligence and AI agent chat.

## Setup

### 1. Create virtual environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure environment
```bash
cp .env.example .env
# Edit .env with your actual values:
# - DATABASE_URL (PostgreSQL with pgvector extension)
# - ANTHROPIC_API_KEY
# - OPENAI_API_KEY
```

### 4. Test startup
```bash
# Run the test
python test_startup.py

# Or start the server
python -m main
```

Server runs at `http://localhost:8000`
Docs at `http://localhost:8000/docs`

## API Endpoints

- `POST /ingest` - Upload and process a PDF
- `POST /chat` - Query documents with AI agent
- `GET /` - Health check

## Project Structure

```
.
├── main.py              # FastAPI app entry point
├── config.py            # Environment configuration
├── models/              # SQLAlchemy ORM models
├── routes/              # API route handlers (TODO)
├── services/            # Business logic (TODO)
└── utils/               # Utility functions (TODO)
```

## Requirements

- Python 3.12+
- PostgreSQL 13+ with pgvector extension
- Anthropic API key
- OpenAI API key
