from unittest.mock import MagicMock

from src.application.agents.memory.agent import memory_agent
from src.domain.ports import SQLitePort, VectorStorePort
from tests.constants import TEST_PAPER_ID, TEST_STATE


def test_memory_agent_related_papers():
    mock_vector_store = MagicMock(spec=VectorStorePort)
    mock_vector_store.search_similar.return_value = [TEST_PAPER_ID]
    mock_sql = MagicMock(spec=SQLitePort)

    result = memory_agent(
        state=TEST_STATE, vector_store=mock_vector_store, sql=mock_sql
    )

    assert result == {"related_papers": [TEST_PAPER_ID]}
    mock_sql.add_paper.assert_called_once()


def test_memory_agent_no_related_papers():
    mock_vector_store = MagicMock(spec=VectorStorePort)
    mock_vector_store.search_similar.return_value = []
    mock_sql = MagicMock(spec=SQLitePort)

    result = memory_agent(
        state=TEST_STATE, vector_store=mock_vector_store, sql=mock_sql
    )

    assert result == {"related_papers": []}
