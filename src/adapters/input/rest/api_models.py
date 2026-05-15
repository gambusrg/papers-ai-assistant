import uuid

from pydantic import BaseModel


class PaperRequest(BaseModel):
    source: str


class StartConversationRequest(BaseModel):
    paper_id: uuid.UUID


class MessageRequest(BaseModel):
    query: str
