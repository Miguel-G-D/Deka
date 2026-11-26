"""Handle inbound channel messages."""

from backend.domain.channel import InboundMessage, MessageHandler, MessageSender, OutboundMessage


class HandleInboundMessage:
    def __init__(self, handler: MessageHandler, sender: MessageSender) -> None:
        self._handler = handler
        self._sender = sender

    def execute(self, inbound: InboundMessage) -> None:
        if inbound.is_echo or not inbound.text.strip():
            return
        reply = self._handler.handle(inbound)
        self._sender.send(OutboundMessage(inbound.sender_id, reply))
