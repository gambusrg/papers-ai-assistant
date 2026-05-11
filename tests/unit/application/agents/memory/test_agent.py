from unittest.mock import MagicMock

import pytest

from src.application.agents.memory.agent import memory_agent
from src.domain.ports import VectorStorePort
from tests.constants import TEST_PAPER, TEST_PAPER_ID, TEST_STATE


def test_memory_agent_related_papers():
    # Arrange
    mock_vector_store = MagicMock(spec=VectorStorePort)
    mock_vector_store.search_similar.return_value = [TEST_PAPER]
    mock_vector_store.save_paper.return_value = None

    # Act
    result = memory_agent(state=TEST_STATE, vector_store=mock_vector_store)

    # Assert
    assert result == {"related_papers": [TEST_PAPER_ID]}


def test_memory_agent_no_related_papers():
    # Arrange
    mock_vector_store = MagicMock(spec=VectorStorePort)
    mock_vector_store.search_similar.return_value = []
    mock_vector_store.save_paper.return_value = None

    # Act
    result = memory_agent(state=TEST_STATE, vector_store=mock_vector_store)

    # Assert
    assert result == {"related_papers": []}
