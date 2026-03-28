from dataclasses import dataclass


@dataclass
class LLMConfig:
    model: str = "llama-3.3-70b-versatile"
    temperature: float = 0.2
    max_tokens: int = 512
    top_p: float = 1.0