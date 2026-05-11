from groq import Groq

from src.domain.ports import LLMPort


class GroqLLM(LLMPort):
    def __init__(self, client: Groq):
        self.client = client

    def complete(self, prompt: str, model: str) -> str:
        response = self.client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content
