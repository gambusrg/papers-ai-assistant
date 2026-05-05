import datetime
from typing import TypedDict
import uuid


class State(TypedDict):
    id: uuid.UUID
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
