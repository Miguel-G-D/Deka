"""Meta Graph API message sender."""

from __future__ import annotations

import httpx

from backend.domain.channel import OutboundMessage


class MetaGraphClient:
    def __init__(
        self,
        page_access_token: str,
        api_version: str = "v21.0",
        client: httpx.Client | None = None,
    ) -> None:
        self._token = page_access_token
        self._api_version = api_version
        self._client = client

    def send(self, outbound: OutboundMessage) -> None:
        url = f"https://graph.facebook.com/{self._api_version}/me/messages"
        payload = {
            "recipient": {"id": outbound.recipient_id},
            "message": {"text": outbound.text},
        }
        params = {"access_token": self._token}
        if self._client is not None:
            response = self._client.post(url, params=params, json=payload)
            response.raise_for_status()
            return
        with httpx.Client(timeout=10.0) as client:
            response = client.post(url, params=params, json=payload)
            response.raise_for_status()
