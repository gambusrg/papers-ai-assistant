from typing import TypedDict
import uuid


class ConversationState(TypedDict):
    user_id: uuid.UUID
    query: str
    response: str
    conversation_context: list[BaseMessage]
    paper_id: uuid.UUID
