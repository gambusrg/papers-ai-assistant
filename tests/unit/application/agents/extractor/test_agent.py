import json
from unittest.mock import MagicMock


from src.application.agents.extractor.agent import extractor_agent
from src.domain.ports import LLMPort
from tests.constants import TEST_STATE


def test_extractor_agent():
    # Arrange
    mock_llm_port = MagicMock(specs=LLMPort)
    mock_llm_port.complete.return_value = json.dumps(
        {
            "technologies": ["transformers", "attention"],
            "user_interest_points": ["RAG", "fine-tuning"],
            "project_interest_points": ["low latency", "multimodal embeddings"],
            "user_content_points": "El paper describe una arquitectura RAG hibrida.",
            "project_content_points": "El paper menciona optimizaciones de inferencia.",
        }
    )

    mock_vector_store = MagicMock()
    mock_vector_store.search_similar_chunks.return_value = ["chunk1"]

    # Act
    result = extractor_agent(state=TEST_STATE, llm=mock_llm_port, vector_store=mock_vector_store)

    # Assert
    result == {
        "user_interest_points": ["RAG", "fine-tuning"],
        "project_interest_points": ["low latency", "multimodal embeddings"],
        "user_content_points": "El paper describe una arquitectura RAG híbrida y técnicas de fine-tuning supervisado para mejorar recuperación contextual.",
        "project_content_points": "El paper menciona optimizaciones de inferencia para reducir latencia y el uso de embeddings multimodales para búsqueda semántica.",
    }
