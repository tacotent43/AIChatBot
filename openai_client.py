import os
from openai import AsyncOpenAI


class LLMClient:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY", "lm-studio")
        self.model = os.getenv("OPENAI_MODEL", "openai/gpt-oss-20b")
        self.base_url = os.getenv("BASE_URL")

        if self.base_url:
            self.client = AsyncOpenAI(api_key=self.api_key, base_url=self.base_url)
        else:
            self.client = AsyncOpenAI(api_key=self.api_key)

    async def chat(self, messages: list[dict], temperature: float = 0.7) -> str:
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=1500,
            )
            return response.choices[0].message.content.strip()

        except Exception as e:
            return f"Error accessing the model: {e}"


llm = LLMClient()


async def call_openai_chat(messages: list[dict], temperature: float = 0.7) -> str:
    return await llm.chat(messages, temperature)