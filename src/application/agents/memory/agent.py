from src.domain.ports import VectorStorePort
from src.domain.state import State
import logging

logger = logging.getLogger(__name__)


def memory_agent(state: State, vector_store: VectorStorePort) -> dict:

    logger.info("MEMORY | Searching for related papers")
    query = f"{state['title']} {' '.join(state['technologies'])} {' '.join(state['headers'])}"
    related_paper_ids = vector_store.search_similar(
        query=query, user_id=str(state["user_id"]), paper_id=str(state["id"])
    )

    logger.info(f"MEMORY | Related papers found: {len(related_paper_ids)}")

    return {"related_papers": related_paper_ids}
