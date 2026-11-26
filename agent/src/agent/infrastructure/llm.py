"""LLM provider wiring stub (OpenRouter via LangChain — no live calls)."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class OpenRouterConfig:
    """Configuration for OpenRouter-backed models."""

    model: str = "openai/gpt-4o-mini"
    base_url: str = "https://openrouter.ai/api/v1"

    def is_configured(self, api_key: str | None) -> bool:
        return bool(api_key and api_key.strip())
