"""MetaGraphClient send tests with httpx mock transport."""

import httpx

from backend.domain.channel import OutboundMessage
from backend.infrastructure.meta_client import MetaGraphClient


def test_send_posts_to_graph_me_messages() -> None:
    recorded: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        recorded.append(request)
        return httpx.Response(200, json={"recipient_id": "igsid-1", "message_id": "m"})

    transport = httpx.MockTransport(handler)
    client = httpx.Client(transport=transport)
    sender = MetaGraphClient(
        page_access_token="page-token",
        api_version="v21.0",
        client=client,
    )
    sender.send(OutboundMessage(recipient_id="igsid-1", text="Deka ok: hola"))

    assert len(recorded) == 1
    request = recorded[0]
    assert request.method == "POST"
    assert str(request.url).startswith(
        "https://graph.facebook.com/v21.0/me/messages"
    )
    assert request.url.params["access_token"] == "page-token"
    body = request.content
    assert b"igsid-1" in body
    assert b"Deka ok: hola" in body
