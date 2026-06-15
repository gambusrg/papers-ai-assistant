# Papers Assistant

A conversational AI assistant for scientific papers. Index a paper by URL or PDF and chat with it using RAG (Retrieval-Augmented Generation).

## Features

- Index papers from URL or PDF upload
- Conversational chat with automatic routing (RAG vs. plain chat)
- Semantic search over paper content using ChromaDB
- Conversation history persistence with SQLite
- Clean hexagonal architecture with LangGraph agent orchestration

## Tech Stack

| Component | Technology |
|---|---|
| API | FastAPI |
| Agent orchestration | LangGraph |
| LLM | Groq (Llama 3.3 70B) |
| Vector store | ChromaDB + sentence-transformers |
| Embeddings | all-MiniLM-L6-v2 |
| Persistence | SQLite |
| PDF extraction | PyMuPDF |

## Architecture

The system has two main flows:

**Indexing** — `POST /papers`
```
Reader → Indexer → Extractor → Memory
```

**Conversation** — `POST /conversation/{id}/message`
```
Router → RAG (ChromaDB search) → Generator
       → CHAT                  → Generator
```

## Getting Started

### Prerequisites

- Python 3.12
- [uv](https://docs.astral.sh/uv/)
- A [Groq API key](https://console.groq.com)

### Local setup

```bash
# Install dependencies
uv sync

# Create .env file
cp .env.example .env
# Add your GROQ_API_KEY to .env

# Run the app
uv run uvicorn src.adapters.input.rest.api:app --host 0.0.0.0 --port 8080 --reload
```

Open `http://localhost:8080` in your browser.

### Docker

```bash
# Build and run
docker compose up --build
```

The app will be available at `http://localhost:8080`.

Data is persisted in Docker-managed volumes between sessions.

## Project Structure

```
src/
├── domain/          # Models, state, abstract ports
├── application/
│   ├── agents/      # LangGraph nodes (reader, indexer, extractor, memory, conversational)
│   └── graph/       # LangGraph graph definitions
├── adapters/
│   ├── input/rest/  # FastAPI endpoints
│   └── output/      # ChromaDB, Groq, SQLite implementations
└── core/            # Dependency injection
resources/
├── prompts/         # YAML prompt templates
└── db_tables/       # SQLite schema
static/              # Frontend (HTML/CSS/JS)
```

## Environment Variables

| Variable | Description |
|---|---|
| `GROQ_API_KEY` | Groq API key |
| `GOOGLE_API_KEY` | Google Gemini API key (optional) |
