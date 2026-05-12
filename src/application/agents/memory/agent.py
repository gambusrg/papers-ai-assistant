import datetime

from src.domain.models import Paper
from src.domain.ports import VectorStorePort
from src.domain.state import State


def memory_agent(state: State, vector_store: VectorStorePort) -> dict:
    """Searches for similar papers and saves the new paper to the vector store.

    Args:
        state (State): current graph state

    Returns:
        dict: updated state with related_papers
    """
    query = f"{state['title']} {' '.join(state['technologies'])} {' '.join(state['headers'])}"
    similar_papers = vector_store.search_similar(
        query=query, user_id=str(state["user_id"])
    )

    related_paper_ids = [paper.id for paper in similar_papers]

    new_paper = Paper(
        title=state["title"],
        technologies=state["technologies"],
        content=state["content"],
        headers=state["headers"],
        pages=state["pages"],
        timestamp=datetime.datetime.now(),
        project_interest_points=state["project_interest_points"],
        user_interest_points=state["user_interest_points"],
        project_content_points=state["project_content_points"],
        user_content_points=state["user_content_points"],
        related_papers=related_paper_ids,
        previous_user_interests=state["user_interests"],
        previous_project_interests=state["project_interests"],
    )

    vector_store.save_paper(paper=new_paper)

    return {"related_papers": related_paper_ids}
