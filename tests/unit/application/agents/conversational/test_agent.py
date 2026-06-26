from unittest.mock import MagicMock

from src.application.agents.conversational.agent import generator_node, rag_node
from tests.constants import TEST_CONVERSATION_STATE


def test_rag_node_returns_chunks():
    mock_vector_store = MagicMock()
    mock_vector_store.search_similar_chunks.return_value = ["chunk1", "chunk2"]

    state = {**TEST_CONVERSATION_STATE}
    result = rag_node(state=state, vector_store=mock_vector_store)

    assert result == {"chunks": ["chunk1", "chunk2"]}


def test_generator_node_with_chunks():
    mock_llm = MagicMock()
    mock_llm.complete.return_value = "Attention mechanisms work by..."
    mock_sql = MagicMock()

    state = {**TEST_CONVERSATION_STATE, "chunks": ["chunk1"]}
    result = generator_node(state=state, llm=mock_llm, sql=mock_sql)

    assert result == {"response": "Attention mechanisms work by..."}
    mock_sql.add_message.assert_called_once()


def test_generator_node_without_chunks():
    mock_llm = MagicMock()
    mock_llm.complete.return_value = "I don't have enough context."
    mock_sql = MagicMock()

    state = {**TEST_CONVERSATION_STATE, "chunks": []}
    result = generator_node(state=state, llm=mock_llm, sql=mock_sql)

    assert result == {"response": "I don't have enough context."}
