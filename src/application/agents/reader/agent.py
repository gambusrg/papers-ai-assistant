from src.application.agents.reader.factory import ReaderFactory
from src.domain.state import State


def reader_agent(state: State) -> dict:
    """Reads paper content from source URL or file path.

    Args:
        state (State): current graph state, requires 'source' field.

    Returns:
        dict: updated title, headers, content and pages.
    """
    reader = ReaderFactory.create_strategy(source=state["source"])
    raw_paper = reader.read(source=state["source"])

    return {
        "title": raw_paper.title,
        "headers": raw_paper.headers,
        "content": raw_paper.content,
        "pages": raw_paper.pages,
    }
