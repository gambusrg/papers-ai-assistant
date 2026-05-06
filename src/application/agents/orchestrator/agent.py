from src.domain.ports import VectorStorePort
from src.domain.state import State


def orchestrate(state: State, vector_store: VectorStorePort) -> str:
    """Checks if the paper already exists in the vector store and routes accordingly.

    Args:
        state (State): current graph state
        vector_store (VectorStorePort): vector store port implementation

    Returns:
        str: "existing" if paper already processed, "new" otherwise
    """
    exists = vector_store.exists(paper_id=state["id"])
    return "existing" if exists else "new"
