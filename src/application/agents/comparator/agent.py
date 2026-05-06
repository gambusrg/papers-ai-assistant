from src.domain.state import State


def compare(state: State) -> str:
    """_summary_

    Args:
        state (State): _description_

    Returns:
        dict: _description_
    """
    if (
        state["user_interests"] == state["previous_user_interests"]
        and state["previous_project_interests"] == state["project_interests"]
    ):
        return "discard"
    else:
        return "reprocess"
