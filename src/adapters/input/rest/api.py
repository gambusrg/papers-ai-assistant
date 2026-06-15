import datetime
import hashlib
import os
import tempfile
import uuid

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from src.application.graph.processing_graph import graph
from src.application.graph.conversational_graph import conv_graph
from src.adapters.input.rest.api_models import StartConversationRequest, MessageRequest
from src.core.dependency_injector import conversation_repo
from src.domain.state import ConversationState, State
import logging

logging.basicConfig(level=logging.INFO)
for noisy in ("httpx", "chromadb", "hpack", "httpcore", "urllib3", "sentence_transformers", "watchfiles"):
    logging.getLogger(noisy).setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def root():
    return FileResponse("static/index.html")


@app.post("/papers")
def add_paper(
    source: str | None = Form(default=None),
    file: UploadFile | None = File(default=None),
):
    if not source and not file:
        raise HTTPException(
            status_code=400, detail="Provide either a source URL or a PDF file"
        )

    tmp_path = None
    try:
        if file:
            pdf_bytes = file.file.read()
            paper_id = uuid.uuid5(
                uuid.NAMESPACE_URL, hashlib.sha256(pdf_bytes).hexdigest()
            )
            tmp = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
            tmp.write(pdf_bytes)
            tmp.close()
            tmp_path = tmp.name
            source_path = tmp_path
        else:
            source = str(source)
            paper_id = uuid.uuid5(uuid.NAMESPACE_URL, source)
            source_path = source

        initial_state: State = {
            "user_id": uuid.UUID("00000000-0000-0000-0000-000000000001"),
            "source": source_path,
            "id": paper_id,
            "title": "",
            "content": "",
            "headers": [],
            "pages": 0,
            "technologies": [],
            "timestamp": datetime.datetime.now(),
            "project_interest_points": [],
            "user_interest_points": [],
            "project_content_points": "",
            "user_content_points": "",
            "related_papers": [],
            "previous_user_interests": [
                "deep learning",
                "NLP",
                "transformers",
                "attention mechanisms",
            ],
            "previous_project_interests": ["Python", "LLMs", "RAG", "vector databases"],
            "user_interests": [
                "deep learning",
                "NLP",
                "transformers",
                "attention mechanisms",
            ],
            "project_interests": ["Python", "LLMs", "RAG", "vector databases"],
        }
        state = graph.invoke(initial_state)
    finally:
        if tmp_path:
            os.unlink(tmp_path)

    return {"id": state["id"]}


@app.get("/papers")
def list_papers():
    """Returns all papers indexed by the current user."""
    user_id = "00000000-0000-0000-0000-000000000001"
    return conversation_repo.get_papers(user_id=user_id)


@app.post("/conversation")
def start_conversation(request: StartConversationRequest):
    """Creates a new conversation about a specific paper.

    Args:
        request (StartConversationRequest): contains paper_id.

    Returns:
        dict: the new conversation_id.
    """
    user_id = "00000000-0000-0000-0000-000000000001"
    conversation_id = conversation_repo.create_conversation(
        user_id=user_id, paper_id=str(request.paper_id)
    )
    return {"conversation_id": conversation_id}


@app.post("/conversation/{conversation_id}/message")
def send_message(conversation_id: str, request: MessageRequest):
    """Sends a message in an existing conversation and returns the assistant response.

    Args:
        conversation_id (str): ID of the conversation.
        request (MessageRequest): contains the user query.

    Returns:
        dict: the assistant response.
    """
    user_id = "00000000-0000-0000-0000-000000000001"
    paper_id = conversation_repo.get_paper_id(conversation_id)

    conversation_repo.add_message(conversation_id=conversation_id, role="user", content=request.query)
    messages = conversation_repo.get_messages(conversation_id=conversation_id)
    history = "\n".join(f"{m['role']}: {m['content']}" for m in messages)

    initial_state: ConversationState = {
        "conversation_id": conversation_id,
        "paper_id": paper_id,
        "user_id": user_id,
        "query": request.query,
        "chat_history": history,
        "chunks": [],
        "response": "",
    }

    result = conv_graph.invoke(initial_state)
    return {"response": result["response"]}
