from src.domain.models import Paper
from src.domain.ports import VectorStorePort


def orchestrate(paper: Paper, vector_store: VectorStorePort) -> bool:
    """_summary_

    Args:
        paper (Paper): _description_
        vector_store (VectorStorePort): _description_

    Returns:
        str: _description_
    """
    exists = vector_store.exists(paper_id=paper.id)
    if exists:
        return True
    else:
        return False
