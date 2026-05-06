import datetime
import uuid

import chromadb

from src.domain.models import Paper
from src.domain.ports import VectorStorePort


class ChromaVectorStore(VectorStorePort):
    def __init__(self, collection: chromadb.Collection):
        self.collection = collection

    def exists(self, paper_id: uuid.UUID) -> bool:
        result = self.collection.get(ids=[str(paper_id)])
        return len(result["ids"]) > 0

    def search_similar(self, query: str, user_id: str) -> list[Paper]:
        results = self.collection.query(
            query_texts=[query],
            n_results=5,
            where={"user_id": user_id},
        )
        return [
            Paper(
                id=uuid.UUID(m["id"]),
                user_id=uuid.UUID(m["user_id"]),
                title=m["title"],
                headers=m["headers"],
                pages=m["pages"],
                technologies=m["technologies"],
                timestamp=datetime.datetime.fromisoformat(m["timestamp"]),
                content=doc,
                user_interest_points=m["user_interest_points"],
                project_interest_points=m["project_interest_points"],
                user_content_points=m["user_content_points"],
                project_content_points=m["project_content_points"],
            )
            for m, doc in zip(results["metadatas"][0], results["documents"][0])
        ]

    def save_paper(self, paper: Paper) -> None:
        self.collection.add(
            ids=[str(paper.id)],
            documents=[paper.content],
            metadatas=[
                {
                    "id": str(paper.id),
                    "user_id": str(paper.user_id),
                    "title": paper.title,
                    "headers": paper.headers,
                    "pages": paper.pages,
                    "technologies": paper.technologies,
                    "timestamp": paper.timestamp.isoformat(),
                    "user_interest_points": paper.user_interest_points,
                    "project_interest_points": paper.project_interest_points,
                    "user_content_points": paper.user_content_points,
                    "project_content_points": paper.project_content_points,
                }
            ],
        )
