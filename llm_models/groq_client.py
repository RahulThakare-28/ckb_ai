import os
from dotenv import load_dotenv
load_dotenv() 

from typing import Optional
from groq import Groq
from llm_models.config import LLMConfig


class GroqClient:
    def __init__(self, config: LLMConfig):
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables.")

        self.config = config
        self.client = Groq(api_key=self.api_key)

    def generate(self, prompt: str) -> Optional[str]:
        try:
            response = self.client.chat.completions.create(
                model=self.config.model,
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens,
                top_p=self.config.top_p,
                messages=[
                    {"role": "system", "content": "You are a helpful AI assistant."},
                    {"role": "user", "content": prompt}
                ],
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            print(f"[Groq ERROR]: {e}")
            return None