from abc import ABC, abstractmethod
import uuid


class VectorStorePort(ABC):
    """Abstract port for vector store operations."""

    @abstractmethod
    def search_similar(
        self, query: str, user_id: str, paper_id: str
    ) -> list[uuid.UUID]: ...
    @abstractmethod
    def exists(self, paper_id: uuid.UUID) -> bool: ...
    @abstractmethod
    def index_paper(
        self,
        texts: list[str],
        paper_id: str,
        user_id: str,
        title: str,
        headers: list[str],
        pages: int,
    ) -> None: ...
    @abstractmethod
    def search_similar_chunks(
        self, query: str, user_id: str, paper_id: str
    ) -> list[str]: ...


class LLMPort(ABC):
    """Abstract port for LLM completions."""

    @abstractmethod
    def complete(
        self, prompt: str, model: str, system_prompt: str | None = None
    ) -> str: ...


class SQLitePort(ABC):
    """Abstract port for conversation persistence operations."""

    @abstractmethod
    def create_conversation(self, user_id: str, paper_id: str) -> str: ...

    @abstractmethod
    def add_message(self, conversation_id: str, role: str, content: str) -> None: ...

    @abstractmethod
    def get_messages(self, conversation_id: str) -> list[dict]: ...

    @abstractmethod
    def get_paper_id(self, conversation_id: str) -> str: ...

    @abstractmethod
    def add_paper(self, paper_id: str, user_id: str, title: str) -> None: ...

    @abstractmethod
    def get_papers(self, user_id: str) -> list[dict]: ...
