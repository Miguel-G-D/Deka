"""Meta webhook HTTP integration tests."""

from __future__ import annotations

import hashlib
import hmac
import json

from fastapi.testclient import TestClient

from backend.application.inbound import HandleInboundMessage
from backend.domain.channel import OutboundMessage
from backend.infrastructure.meta_settings import MetaSettings
from backend.infrastructure.stub_handler import StubEchoHandler
from backend.presentation.deps import get_inbound_use_case, get_meta_settings
from backend.presentation.main import create_app

_SETTINGS = MetaSettings(
    verify_token="test-verify",
    app_secret="test-secret",
    page_access_token="page-token",
    api_version="v21.0",
)


class _RecordingSender:
    def __init__(self) -> None:
        self.sent: list[OutboundMessage] = []

    def send(self, outbound: OutboundMessage) -> None:
        self.sent.append(outbound)


def _sign(body: bytes) -> str:
    digest = hmac.new(
        _SETTINGS.app_secret.encode("utf-8"),
        body,
        hashlib.sha256,
    ).hexdigest()
    return f"sha256={digest}"


def _client_with_overrides(sender: _RecordingSender) -> TestClient:
    app = create_app()
    app.dependency_overrides[get_meta_settings] = lambda: _SETTINGS
    app.dependency_overrides[get_inbound_use_case] = lambda: HandleInboundMessage(
        StubEchoHandler(),
        sender,
    )
    return TestClient(app)


def test_verify_webhook_returns_challenge() -> None:
    sender = _RecordingSender()
    client = _client_with_overrides(sender)
    response = client.get(
        "/webhooks/meta",
        params={
            "hub.mode": "subscribe",
            "hub.verify_token": "test-verify",
            "hub.challenge": "CHALLENGE_ACCEPTED",
        },
    )
    assert response.status_code == 200
    assert response.text == "CHALLENGE_ACCEPTED"


def test_verify_webhook_rejects_bad_token() -> None:
    client = _client_with_overrides(_RecordingSender())
    response = client.get(
        "/webhooks/meta",
        params={
            "hub.mode": "subscribe",
            "hub.verify_token": "wrong",
            "hub.challenge": "CHALLENGE_ACCEPTED",
        },
    )
    assert response.status_code == 403


def test_post_signed_instagram_message_sends_stub_reply() -> None:
    sender = _RecordingSender()
    client = _client_with_overrides(sender)
    payload = {
        "object": "instagram",
        "entry": [
            {
                "id": "igid-1",
                "messaging": [
                    {
                        "sender": {"id": "igsid-1"},
                        "recipient": {"id": "igid-1"},
                        "message": {"mid": "mid-1", "text": "hola"},
                    }
                ],
            }
        ],
    }
    body = json.dumps(payload).encode("utf-8")
    response = client.post(
        "/webhooks/meta",
        content=body,
        headers={
            "Content-Type": "application/json",
            "X-Hub-Signature-256": _sign(body),
        },
    )
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    assert sender.sent == [
        OutboundMessage(recipient_id="igsid-1", text="Deka ok: hola"),
    ]


def test_post_bad_signature_forbidden() -> None:
    sender = _RecordingSender()
    client = _client_with_overrides(sender)
    body = b'{"object":"instagram","entry":[]}'
    response = client.post(
        "/webhooks/meta",
        content=body,
        headers={
            "Content-Type": "application/json",
            "X-Hub-Signature-256": "sha256=deadbeef",
        },
    )
    assert response.status_code == 403
    assert sender.sent == []
