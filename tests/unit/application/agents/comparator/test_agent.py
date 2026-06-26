from src.application.agents.comparator.agent import compare
from tests.constants import TEST_STATE


def test_compare_reprocess():
    # Arrange
    # Act
    result = compare(state=TEST_STATE)

    # Assert
    assert result == "reprocess"


def test_compare_discard():
    # Arrange
    TEST_STATE["project_interests"] = []
    TEST_STATE["user_interests"] = []
    TEST_STATE["previous_user_interests"] = []
    TEST_STATE["previous_project_interests"] = []

    # Act
    result = compare(state=TEST_STATE)

    # Assert
    assert result == "discard"
