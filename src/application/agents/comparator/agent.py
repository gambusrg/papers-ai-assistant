from src.domain.state import State


def comparator_node(state: State) -> dict:
    """Pass-through node required by LangGraph before the routing conditional edge.

    Returns:
        dict: empty dict, no state updates.
    """
    return {}


def compare(state: State) -> str:
    """Determines whether to reprocess an existing paper based on interest changes.

    Args:
        state (State): current graph state with user_interests, project_interests and their previous values.

    Returns:
        str: 'reprocess' if interests changed, 'discard' otherwise.
    """
    if (
        state["user_interests"] == state["previous_user_interests"]
        and state["previous_project_interests"] == state["project_interests"]
    ):
        return "discard"
    else:
        return "reprocess"
