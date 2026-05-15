import logging
import yaml

from src.domain.ports import LLMPort, SQLitePort, VectorStorePort

logger = logging.getLogger(__name__)

with open("resources/prompts/conversational.yaml") as f:
    CONVERSATIONAL_PROMPT = yaml.safe_load(f)


def conversation_agent(
    query: str,
    conversation_id: str,
    user_id: str,
    paper_id: str,
    vector_store: VectorStorePort,
    llm: LLMPort,
    sql: SQLitePort,
) -> str:
    """Generates a response to the user query using RAG and conversation history.

    Args:
        query (str): the user's message.
        conversation_id (str): ID of the ongoing conversation.
        user_id (str): ID of the user.
        paper_id (str): ID of the paper being discussed.
        vector_store (VectorStorePort): for RAG chunk retrieval.
        llm (LLMPort): LLM port implementation.
        sql (SQLitePort): for conversation history persistence.

    Returns:
        str: the assistant response.
    """
    sql.add_message(conversation_id=conversation_id, role="user", content=query)

    messages = sql.get_messages(conversation_id=conversation_id)
    history = "\n".join(f"{m['role']}: {m['content']}" for m in messages)

    chunks = vector_store.search_similar_chunks(
        query=query, user_id=user_id, paper_id=paper_id
    )
    chunks_text = "\n\n".join(chunks)

    system_prompt = CONVERSATIONAL_PROMPT["conversational"]["system"]
    user_prompt = CONVERSATIONAL_PROMPT["conversational"]["user"].format(
        history=history,
        chunks=chunks_text,
        query=query,
    )

    logger.info(
        f"CONVERSATIONAL AGENT | Calling LLM for conversation {conversation_id}"
    )
    response = llm.complete(
        prompt=user_prompt, model="llama-3.3-70b-versatile", system_prompt=system_prompt
    )

    sql.add_message(conversation_id=conversation_id, role="assistant", content=response)

    return response
