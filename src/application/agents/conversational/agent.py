import yaml

from src.domain.conversation_state import ConversationState
from src.domain.ports import LLMPort, VectorStorePort

with open("resources/prompts/conversational.yaml") as f:
    CONVERSATIONAL_PROMPT = yaml.safe_load(f)


def conversation_agent(
    state: ConversationState, vector_store: VectorStorePort, llm: LLMPort
) -> dict:
    """_summary_

    Args:
        state (ConversationState): _description_
        vector_store (VectorStorePort): _description_
        llm (LLMPort): _description_

    Returns:
        dict: _description_
    """
    prompt = CONVERSATIONAL_PROMPT["conversational"]["system"].format(
        conversation_context=state["conversation_context"], query=state["query"]
    )
    response = llm.complete(prompt=prompt, model="google-ai-studio")

    return {"response": response}


def decide_routing(state: ConversationState) -> str:
    """_summary_

    Args:
        state (ConversationState): _description_

    Returns:
        str: _description_
    """
    if state["response"] == "SEARCH_NEEDED":
        return "search"
    else:
        return "end"
