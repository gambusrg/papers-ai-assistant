import json

from src.domain.ports import LLMPort


class MockLLM(LLMPort):
    def complete(self, prompt: str, model: str) -> str:
        return json.dumps(
            {
                "user_interest_points": "LLM",
                "project_interest_points": "Azure",
                "user_content_points": "LLMs are the new AI",
                "project_content_points": "Azure is implementing a new LLM",
            }
        )
