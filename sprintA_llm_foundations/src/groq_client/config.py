from dataclasses import dataclass


@dataclass
class Config:
    model: str = "llama-3.1-8b-instant"
    system_prompt: str = "You are concise, friendly assistant."
    max_history_turns: int = 5
