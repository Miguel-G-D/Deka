"""Channel domain entities and port shapes."""

from backend.domain.channel import InboundMessage, OutboundMessage


def test_inbound_message_fields() -> None:
    msg = InboundMessage(
        sender_id="igsid-1",
        text="hola",
        message_id="mid-1",
        is_echo=False,
    )
    assert msg.sender_id == "igsid-1"
    assert msg.text == "hola"
    assert msg.message_id == "mid-1"
    assert msg.is_echo is False


def test_inbound_message_defaults_is_echo_false() -> None:
    msg = InboundMessage(sender_id="s", text="t", message_id="m")
    assert msg.is_echo is False


def test_outbound_message_fields() -> None:
    msg = OutboundMessage(recipient_id="igsid-1", text="Deka ok: hola")
    assert msg.recipient_id == "igsid-1"
    assert msg.text == "Deka ok: hola"
