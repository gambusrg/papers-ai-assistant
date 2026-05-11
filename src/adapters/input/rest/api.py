import datetime
import uuid

from fastapi import FastAPI


from src.application.graph import conversation_graph
from src.application.graph.processing_graph import graph
from src.application.graph.conversation_graph import conversation_graph
from src.adapters.input.rest.api_models import ConversationRequest, PaperRequest
from src.domain.conversation_state import ConversationState
from src.domain.state import State
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app = FastAPI()


@app.post("/papers")
def add_paper(request: PaperRequest):
    """
    Adds a new paper

    Args:
        paper_soruce (str): _description_
    """
    initial_state: State = {
        "user_id": uuid.UUID("00000000-0000-0000-0000-000000000001"),
        "source": request.source,
        "id": uuid.uuid4(),
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
        "previous_user_interests": [],
        "previous_project_interests": [],
        "user_interests": [],
        "project_interests": [],
    }
    state = graph.invoke(initial_state)

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
