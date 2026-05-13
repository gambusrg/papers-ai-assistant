from groq import Groq

from src.domain.ports import LLMPort


class GroqLLM(LLMPort):
    def __init__(self, client: Groq):
        self.client = client

    def complete(
        self,
        prompt: str,
        model: str,
        system_prompt: str | None = None,
    ) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
        )
        return response.choices[0].message.content or ""
