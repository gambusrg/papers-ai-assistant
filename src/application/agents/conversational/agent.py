import logging
import yaml

from src.domain.ports import LLMPort, SQLitePort, VectorStorePort
from src.domain.state import ConversationState

logger = logging.getLogger(__name__)

with open("resources/prompts/conversational.yaml") as f:
    CONVERSATIONAL_PROMPT = yaml.safe_load(f)


def rag_node(state: ConversationState, vector_store: VectorStorePort) -> dict:
    """Retrieves relevant chunks from ChromaDB for the user query."""
    chunks = vector_store.search_similar_chunks(
        query=state["query"],
        user_id=state["user_id"],
        paper_id=state["paper_id"],
    )
    logger.info(f"RAG NODE | Retrieved {len(chunks)} chunks for query='{state['query']}'")
    return {"chunks": chunks}


def generator_node(state: ConversationState, llm: LLMPort, sql: SQLitePort) -> dict:
    """Generates a response using the conversation history and retrieved chunks."""
    system_prompt = CONVERSATIONAL_PROMPT["conversational"]["system"]
    prompt_key = "user_with_context" if state["chunks"] else "user_without_context"
    user_prompt = CONVERSATIONAL_PROMPT["conversational"][prompt_key].format(
        history=state["chat_history"],
        chunks="\n\n".join(state["chunks"]),
        query=state["query"],
    )

    logger.info(f"GENERATOR NODE | mode={'rag' if state['chunks'] else 'chat'}")
    response = llm.complete(
        prompt=user_prompt,
        model="llama-3.3-70b-versatile",
        system_prompt=system_prompt,
    )

    sql.add_message(
        conversation_id=state["conversation_id"],
        role="assistant",
        content=response,
    )
    return {"response": response}
