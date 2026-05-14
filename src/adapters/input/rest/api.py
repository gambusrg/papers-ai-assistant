import datetime
import hashlib
import os
import tempfile
import uuid

from fastapi import FastAPI, File, Form, HTTPException, UploadFile

from src.application.graph.processing_graph import graph
from src.application.graph.conversation_graph import conversation_graph
from src.adapters.input.rest.api_models import ConversationRequest
from src.domain.conversation_state import ConversationState
from src.domain.state import State
import logging

logging.basicConfig(level=logging.WARNING)
logging.getLogger("src").setLevel(logging.INFO)
logger = logging.getLogger(__name__)


app = FastAPI()


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


@app.post("/conversation")
def start_conversation(request: ConversationRequest):
    """
    Starts a new conversation

    Args:
        request (ConversationRequest): _description_
    """

    initial_state: ConversationState = {
        "user_id": uuid.UUID("00000000-0000-0000-0000-000000000001"),
        "query": request.query,
        "response": "",
        "conversation_context": [],
        "paper_id": request.paper_id,
    }

    state = conversation_graph.invoke(initial_state)

    return {"response": state["response"]}
