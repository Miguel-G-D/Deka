"""Intent classification use case (stub — no model calls)."""

from agent.domain.conversation import ConversationIntent


class ClassifyIntent:
    """Classify a customer message into a conversation intent."""

    def execute(self, message: str) -> ConversationIntent:
        normalized = message.strip().lower()
        if "reserv" in normalized:
            return ConversationIntent(name="reservation")
        return ConversationIntent(name="unknown")
