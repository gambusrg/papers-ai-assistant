import uuid

from src.domain.ports import VectorStorePort


class MockVectorStore(VectorStorePort):
    def exists(self, paper_id: uuid.UUID) -> bool:
        return True
