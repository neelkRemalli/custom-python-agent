import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    api_key: str
    model: str
    max_tool_rounds: int


def load_settings() -> Settings:
    """Load and validate settings from the environment and optional .env file."""
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    model = os.getenv("OPENAI_MODEL", "gpt-6").strip()
    try:
        max_rounds = int(os.getenv("MAX_TOOL_ROUNDS", "5"))
    except ValueError as exc:
        raise ValueError("MAX_TOOL_ROUNDS must be an integer.") from exc

    if not api_key:
        raise ValueError("OPENAI_API_KEY is missing.")
    if not model:
        raise ValueError("OPENAI_MODEL is missing.")
    if max_rounds < 1:
        raise ValueError("MAX_TOOL_ROUNDS must be at least 1.")

    return Settings(api_key=api_key, model=model, max_tool_rounds=max_rounds)
