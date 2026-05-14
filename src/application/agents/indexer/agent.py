from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.domain.ports import VectorStorePort
from src.domain.state import State

import logging

logger = logging.getLogger(__name__)


def indexer_agent(state: State, vector_store: VectorStorePort) -> dict:
    """Splits paper content into chunks and indexes them in the vector store.

    Args:
        state (State): current graph state, requires 'content', 'id', 'user_id', 'title', 'headers', 'pages'.
        vector_store (VectorStorePort): vector store to persist the chunks.

    Returns:
        dict: empty dict, no state updates.
    """
    text_splitter = RecursiveCharacterTextSplitter()
    texts = text_splitter.split_text(text=state["content"])

    logger.info(f"INDEXING AGENT | Indexing chunks")
    vector_store.index_paper(
        texts=texts,
        paper_id=str(state["id"]),
        user_id=str(state["user_id"]),
        title=state["title"],
        headers=state["headers"],
        pages=state["pages"],
    )

    return {}
