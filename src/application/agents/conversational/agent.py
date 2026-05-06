import yaml

from src.domain.conversation_state import ConversationState
from src.domain.ports import LLMPort, VectorStorePort

with open("resources/prompts/conversational.yaml") as f:
    CONVERSATIONAL_PROMPT = yaml.safe_load(f)


def conversation_agent(state: ConversationState, llm: LLMPort) -> dict:
    """Generates a response to the user query using available conversation context.

    Args:
        state (ConversationState): current conversation state
        llm (LLMPort): LLM port implementation

    Returns:
        dict: updated state with response
    """
    prompt = CONVERSATIONAL_PROMPT["conversational"]["system"].format(
        conversation_context=state["conversation_context"], query=state["query"]
    )
    response = llm.complete(prompt=prompt, model="gemini-2.0-flash")

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
