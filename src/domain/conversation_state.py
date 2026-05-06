import uuid
from typing import TypedDict


class ConversationState(TypedDict):
    user_id: uuid.UUID
    query: str
    response: str
    conversation_context: list[str]
    paper_id: uuid.UUID
