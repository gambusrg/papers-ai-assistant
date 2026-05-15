import uuid

import chromadb

from src.domain.ports import VectorStorePort


class ChromaVectorStore(VectorStorePort):
    """ChromaDB implementation of VectorStorePort. Stores paper chunks with metadata for semantic search."""

    def __init__(self, collection: chromadb.Collection):
        self.collection = collection

    def exists(self, paper_id: uuid.UUID) -> bool:
        """Checks if a paper has already been indexed.

        Returns:
            bool: True if any chunk with the given paper_id exists.
        """
        result = self.collection.get(where={"paper_id": str(paper_id)}, limit=1)
        return len(result["ids"]) > 0

    def search_similar(
        self, query: str, user_id: str, paper_id: str
    ) -> list[uuid.UUID]:
        """Finds other papers by the same user that are semantically similar to the query.

        Args:
            query (str): semantic search query built from title, technologies and headers.
            user_id (str): filters results to the current user's papers.
            paper_id (str): excludes the current paper from results.

        Returns:
            list[uuid.UUID]: deduplicated list of related paper IDs.
        """
        total = self.collection.count()
        if total == 0:
            return []
        results = self.collection.query(
            query_texts=[query],
            n_results=min(20, total),
            where={"$and": [{"user_id": user_id}, {"paper_id": {"$ne": paper_id}}]},
        )
        seen = set()
        related = []
        for m in (results["metadatas"] or [[]])[0]:
            pid = str(m["paper_id"])
            if pid not in seen:
                seen.add(pid)
                related.append(uuid.UUID(pid))
        return related

    def search_similar_chunks(
        self, query: str, user_id: str, paper_id: str
    ) -> list[str]:
        """Retrieves the most relevant chunks from a specific paper for RAG.

        Returns:
            list[str]: top-15 chunks ranked by semantic similarity to the query.
        """
        total = self.collection.count()
        if total == 0:
            return []
        results = self.collection.query(
            query_texts=[query],
            n_results=min(15, total),
            where={"$and": [{"paper_id": paper_id}, {"user_id": user_id}]},
        )
        return (results["documents"] or [[]])[0]

    def index_paper(
        self,
        texts: list[str],
        paper_id: str,
        user_id: str,
        title: str,
        headers: list[str],
        pages: int,
    ) -> None:
        """Adds chunked paper text to ChromaDB with metadata.

        Args:
            texts (list[str]): list of text chunks from the paper.
            paper_id, user_id, title, headers, pages: metadata stored on every chunk.
        """
        self.collection.add(
            ids=[f"{paper_id}_{i}" for i in range(len(texts))],
            documents=texts,
            metadatas=[
                {
                    "paper_id": paper_id,
                    "user_id": user_id,
                    "title": title,
                    "headers": "|".join(headers),
                    "pages": pages,
                }
                for _ in texts
            ],
        )
