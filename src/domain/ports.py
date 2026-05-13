from abc import ABC, abstractmethod
import uuid

from src.domain.models import Paper


class VectorStorePort(ABC):
    @abstractmethod
    def save_paper(self, paper: Paper) -> None: ...
    @abstractmethod
    def search_similar(
        self, query: str, user_id: str, paper_id: str
    ) -> list[Paper]: ...
    @abstractmethod
    def exists(self, paper_id: uuid.UUID) -> bool: ...
    @abstractmethod
    def index_paper(self, texts: list[str], paper_id: str, user_id: str) -> None: ...
    @abstractmethod
    def search_similar_chunks(
        self, query: str, user_id: str, paper_id: str
    ) -> list[str]: ...


class LLMPort(ABC):
    @abstractmethod
    def complete(self, prompt: str, model: str, system_prompt: str | None = None) -> str: ...
