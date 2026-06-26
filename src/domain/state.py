import datetime
from typing import TypedDict
import uuid


class State(TypedDict):
    user_id: uuid.UUID
    id: uuid.UUID
    source: str
    title: str
    technologies: list[str]
    content: str
    headers: list[str]
    pages: int
    timestamp: datetime.datetime
    project_interest_points: list[str]
    user_interest_points: list[str]
    project_content_points: str
    user_content_points: str
    related_papers: list[uuid.UUID]
    previous_user_interests: list[str]
    previous_project_interests: list[str]
    user_interests: list[str]
    project_interests: list[str]


class ConversationState(TypedDict):
    conversation_id: str
    paper_id: str
    user_id: str
    query: str
    chat_history: str
    chunks: list[str]
    response: str
