import datetime
import uuid

from src.domain.models import Paper
from src.domain.ports import VectorStorePort


class MockVectorStore(VectorStorePort):
    def exists(self, paper_id: uuid.UUID) -> bool:
        return True

    def search_similar(self, query: str, user_id: str) -> list[Paper]:
        return [
            Paper(
                title="Mock Paper",
                technologies=["python"],
                content="mock content",
                headers=["intro"],
                pages=5,
                timestamp=datetime.datetime.now(),
            )
        ]

    def save_paper(self, paper: Paper) -> None:
        return None
