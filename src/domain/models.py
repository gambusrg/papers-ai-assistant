import datetime
from typing import Optional
import uuid

from pydantic import BaseModel, Field


class User(BaseModel):
    id: uuid.UUID = Field(description="id of the user", default_factory=uuid.uuid4)
    name: str
    creation_date: datetime.datetime
    profile_id: uuid.UUID


class Project(BaseModel):
    id: uuid.UUID = Field(description="id of the project", default_factory=uuid.uuid4)
    name: str
    description: str
    technologies: list[str]
    repository_url: Optional[str] = Field(
        default=None,
        description="URL of the repository that wants to be added as interest",
    )


class Profile(BaseModel):
    id: uuid.UUID = Field(
        description="id of the user profile", default_factory=uuid.uuid4
    )
    user_id: uuid.UUID
    projects: list[Project] = Field(default_factory=list)
    explicit_interests: list[str] = Field(default_factory=list)
    implicit_interests: list[str] = Field(default_factory=list)


class Paper(BaseModel):
    id: uuid.UUID = Field(description="id of the paper", default_factory=uuid.uuid4)
    title: str
    technologies: list[str]
    content: str
    headers: list[str]
    pages: int
    timestamp: datetime.datetime = Field(default_factory=datetime.datetime.now)
    project_interest_points: list[str] = Field(default_factory=list)
    user_interest_points: list[str] = Field(default_factory=list)
    project_content_points: str = ""
    user_content_points: str = ""
    previous_user_interests: list[str] = Field(default_factory=list)
    previous_project_interests: list[str] = Field(default_factory=list)
    related_papers: list[uuid.UUID] = Field(default_factory=list)


class RawPaper(BaseModel):
    id: uuid.UUID = Field(description="id of the paper", default_factory=uuid.uuid4)
    title: str
    headers: list[str]
    content: str
    pages: int

    @classmethod
    def from_dict(cls, document: dict) -> "RawPaper":
        return cls(
            title=document.get("title", ""),
            headers=document.get("headers", []),
            content=document.get("content", ""),
            pages=document.get("pages", 0),
        )
