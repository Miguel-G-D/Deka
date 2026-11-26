"""Agent application stub tests."""

from agent.application.classify_intent import ClassifyIntent
from agent.infrastructure.llm import OpenRouterConfig
from agent.presentation.entry import handle_message


def test_classify_reservation_intent() -> None:
    intent = ClassifyIntent().execute("I'd like to reserve a table")
    assert intent.is_reservation()


def test_classify_unknown_intent() -> None:
    intent = ClassifyIntent().execute("hello")
    assert intent.name == "unknown"


def test_handle_message_delegates() -> None:
    intent = handle_message("reservation for two")
    assert intent.is_reservation()


def test_openrouter_config_requires_key() -> None:
    config = OpenRouterConfig()
    assert config.is_configured(None) is False
    assert config.is_configured("sk-test") is True
