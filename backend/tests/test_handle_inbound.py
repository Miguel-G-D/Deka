"""HandleInboundMessage use case tests."""

from backend.application.inbound import HandleInboundMessage
from backend.domain.channel import InboundMessage, OutboundMessage
from backend.infrastructure.stub_handler import StubEchoHandler


class _RecordingSender:
    def __init__(self) -> None:
        self.sent: list[OutboundMessage] = []

    def send(self, outbound: OutboundMessage) -> None:
        self.sent.append(outbound)


def test_sends_stub_reply_for_text_message() -> None:
    sender = _RecordingSender()
    uc = HandleInboundMessage(StubEchoHandler(), sender)
    uc.execute(
        InboundMessage(sender_id="igsid-1", text="hola", message_id="mid-1"),
    )
    assert len(sender.sent) == 1
    assert sender.sent[0] == OutboundMessage(
        recipient_id="igsid-1",
        text="Deka ok: hola",
    )


def test_skips_echo_messages() -> None:
    sender = _RecordingSender()
    uc = HandleInboundMessage(StubEchoHandler(), sender)
    uc.execute(
        InboundMessage(
            sender_id="igsid-1",
            text="hola",
            message_id="mid-1",
            is_echo=True,
        ),
    )
    assert sender.sent == []


def test_skips_blank_text() -> None:
    sender = _RecordingSender()
    uc = HandleInboundMessage(StubEchoHandler(), sender)
    uc.execute(
        InboundMessage(sender_id="igsid-1", text="   ", message_id="mid-1"),
    )
    assert sender.sent == []
