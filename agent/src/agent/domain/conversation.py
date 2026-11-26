"""Conversation domain primitives (scaffold)."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ConversationIntent:
    """High-level intent inferred from a customer message."""

    name: str

    def is_reservation(self) -> bool:
        return self.name == "reservation"
