import json
from unittest.mock import MagicMock

import pytest

from src.application.agents.extractor.agent import extractor_agent
from src.domain.ports import LLMPort
from tests.constants import TEST_STATE


def test_extractor_agent():
    # Arrange
    mock_llm_port = MagicMock(specs=LLMPort)
    mock_llm_port.complete.return_value = json.dumps(
        {
            "user_interest_points": ["RAG", "fine-tuning"],
            "project_interest_points": ["low latency", "multimodal embeddings"],
            "user_content_points": "El paper describe una arquitectura RAG híbrida y técnicas de fine-tuning supervisado para mejorar recuperación contextual.",
            "project_content_points": "El paper menciona optimizaciones de inferencia para reducir latencia y el uso de embeddings multimodales para búsqueda semántica.",
        }
    )

    # Act
    result = extractor_agent(state=TEST_STATE, llm=mock_llm_port)

    # Assert
    result == {
        "user_interest_points": ["RAG", "fine-tuning"],
        "project_interest_points": ["low latency", "multimodal embeddings"],
        "user_content_points": "El paper describe una arquitectura RAG híbrida y técnicas de fine-tuning supervisado para mejorar recuperación contextual.",
        "project_content_points": "El paper menciona optimizaciones de inferencia para reducir latencia y el uso de embeddings multimodales para búsqueda semántica.",
    }
