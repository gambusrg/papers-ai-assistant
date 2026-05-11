from unittest.mock import MagicMock

import pytest

from src.application.agents.orchestrator.agent import orchestrate
from src.domain.ports import VectorStorePort
from tests.constants import TEST_STATE


def test_orchestrate_exists():
    # Arrange
    mock_vector_store = MagicMock(spec=VectorStorePort)
    mock_vector_store.exists.return_value = True

    # Act
    result = orchestrate(state=TEST_STATE, vector_store=mock_vector_store)

    # Assert
    assert result == "existing"
    mock_vector_store.exists.assert_called_once()


def test_orchestrate_new():
    # Arrange
    mock_vector_store = MagicMock(spec=VectorStorePort)
    mock_vector_store.exists.return_value = False

    # Act
    result = orchestrate(state=TEST_STATE, vector_store=mock_vector_store)

    # Assert
    assert result == "new"
    mock_vector_store.exists.assert_called_once()
