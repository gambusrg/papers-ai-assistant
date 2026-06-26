import logging
import yaml

from src.domain.ports import LLMPort
from src.domain.state import ConversationState

logger = logging.getLogger(__name__)

with open("resources/prompts/conversational.yaml") as f:
    CONVERSATIONAL_PROMPT = yaml.safe_load(f)


def route(state: ConversationState, llm: LLMPort) -> str:
    """Decides whether to respond via RAG or plain chat."""
    prompt = CONVERSATIONAL_PROMPT["conversational"]["router_system"].format(
        history=state["chat_history"],
        query=state["query"],
    )
    response = llm.complete(prompt=prompt, model="llama-3.3-70b-versatile")
    logger.info(f"ROUTER | query='{state['query']}' → {response.strip()}")
    return "rag" if "rag" in response.lower() else "chat"
