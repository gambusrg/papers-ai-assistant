import json

from google import genai

from src.domain.ports import LLMPort


class GoogleLLM(LLMPort):
    def __init__(self, client: genai.Client):
        self.client = client

    def complete(self, prompt: str, model: str) -> str:
        response = self.client.models.generate_content(model=model, contents=prompt)
        return response.text
