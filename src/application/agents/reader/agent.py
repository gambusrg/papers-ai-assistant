from src.application.agents.reader.factory import ReaderFactory
from src.domain.state import State


def reader_agent(state: State) -> dict:
    """
    Updates the state with the read paper

    Args:
        state (State): _description_

    Returns:
        dict: _description_
    """
    reader = ReaderFactory.create_strategy(source=state["source"])
    raw_paper = reader.read(source=state["source"])

    return {
        "title": raw_paper.title,
        "headers": raw_paper.headers,
        "content": raw_paper.content,
        "pages": raw_paper.pages,
    }
