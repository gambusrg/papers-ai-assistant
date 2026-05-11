import uuid

from pydantic import BaseModel


class PaperRequest(BaseModel):
    source: str


class ConversationRequest(BaseModel):
    paper_id: uuid.UUID
    query: str
