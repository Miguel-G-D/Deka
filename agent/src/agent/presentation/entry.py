"""Agent process entry (scaffold)."""

from agent.application.classify_intent import ClassifyIntent
from agent.domain.conversation import ConversationIntent


def handle_message(message: str) -> ConversationIntent:
    """Handle an inbound message through the application layer."""
    return ClassifyIntent().execute(message)
