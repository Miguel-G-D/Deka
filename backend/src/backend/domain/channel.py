"""Inbound/outbound messaging channel entities and ports."""

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True, slots=True)
class InboundMessage:
    sender_id: str
    text: str
    message_id: str
    is_echo: bool = False


@dataclass(frozen=True, slots=True)
class OutboundMessage:
    recipient_id: str
    text: str


class MessageHandler(Protocol):
    def handle(self, inbound: InboundMessage) -> str: ...


class MessageSender(Protocol):
    def send(self, outbound: OutboundMessage) -> None: ...
