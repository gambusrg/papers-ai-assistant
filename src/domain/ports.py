from abc import ABC, abstractmethod

from src.domain.models import Paper


class VectorStorePort(ABC):
    @abstractmethod
    def save_paper(self, paper: Paper) -> None: ...
    @abstractmethod
    def search_similar(self, query: str, user_id: str) -> list[Paper]: ...


class LLMPort(ABC):
    @abstractmethod
    def complete(self, prompt: str, model: str) -> str: ...
