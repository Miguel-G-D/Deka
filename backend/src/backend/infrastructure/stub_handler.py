"""Stub reply handler for Meta channel smoke tests."""

from backend.domain.channel import InboundMessage


class StubEchoHandler:
    def handle(self, inbound: InboundMessage) -> str:
        return f"Deka ok: {inbound.text}"
