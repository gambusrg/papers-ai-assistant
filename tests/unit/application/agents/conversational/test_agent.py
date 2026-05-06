from unittest.mock import MagicMock

import pytest

from src.application.agents.conversational.agent import (
    conversation_agent,
    decide_routing,
)
from tests.constants import TEST_CONVERSATION_STATE


def test_conversation_agent_ok():
    # Arrange
    mock_llm = MagicMock()
    mock_llm.complete.return_value = "This paper explains attention mechanisms."

    # Act
    response = conversation_agent(state=TEST_CONVERSATION_STATE, llm=mock_llm)

    # Assert
    assert response["response"] == "This paper explains attention mechanisms."


def test_decide_routing():
    # Arrange
    TEST_CONVERSATION_STATE["response"] = "SEARCH_NEEDED"

    # Act
    response = decide_routing(state=TEST_CONVERSATION_STATE)

    # Assert
    assert response == "search"
