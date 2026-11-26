"""Meta webhook signature verification."""

import hashlib
import hmac

from backend.infrastructure.meta_signature import verify_signature


def _sign(secret: str, body: bytes) -> str:
    digest = hmac.new(secret.encode("utf-8"), body, hashlib.sha256).hexdigest()
    return f"sha256={digest}"


def test_valid_signature_accepted() -> None:
    body = b'{"object":"instagram"}'
    secret = "test-secret"
    assert verify_signature(body, _sign(secret, body), secret) is True


def test_invalid_signature_rejected() -> None:
    body = b'{"object":"instagram"}'
    assert verify_signature(body, "sha256=deadbeef", "test-secret") is False


def test_missing_or_malformed_header_rejected() -> None:
    body = b"{}"
    assert verify_signature(body, None, "secret") is False
    assert verify_signature(body, "sha1=abc", "secret") is False
    assert verify_signature(body, "", "secret") is False
