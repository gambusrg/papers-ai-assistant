from src.domain.ports import SQLitePort, VectorStorePort
from src.domain.state import State
import logging

logger = logging.getLogger(__name__)


def memory_agent(state: State, vector_store: VectorStorePort, sql: SQLitePort) -> dict:
    """Finds related papers and persists paper metadata to SQLite.

    Args:
        state (State): current graph state.
        vector_store (VectorStorePort): for semantic similarity search.
        sql (SQLitePort): for paper metadata persistence.

    Returns:
        dict: updated related_papers list.
    """
    sql.add_paper(
        paper_id=str(state["id"]),
        user_id=str(state["user_id"]),
        title=state["title"],
    )
    logger.info(f"MEMORY | Saved paper {state['id']} to SQLite")

    try:
        query = f"{state['title']} {' '.join(state['technologies'])} {' '.join(state['headers'])}"
        related_paper_ids = vector_store.search_similar(
            query=query, user_id=str(state["user_id"]), paper_id=str(state["id"])
        )
        logger.info(f"MEMORY | Related papers found: {len(related_paper_ids)}")
    except Exception as e:
        logger.warning(f"MEMORY | search_similar failed: {e}")
        related_paper_ids = []

    return {"related_papers": related_paper_ids}
