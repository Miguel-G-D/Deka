"""Parse Meta Instagram webhook JSON into domain inbound messages."""

from __future__ import annotations

from typing import Any

from backend.domain.channel import InboundMessage


def parse_instagram_inbound(
    payload: dict[str, Any],
    ig_account_id: str | None = None,
) -> list[InboundMessage]:
    if payload.get("object") != "instagram":
        return []

    results: list[InboundMessage] = []
    for entry in payload.get("entry") or []:
        if not isinstance(entry, dict):
            continue
        entry_id = str(entry.get("id") or "")
        if ig_account_id and entry_id != ig_account_id:
            continue
        for event in entry.get("messaging") or []:
            if not isinstance(event, dict):
                continue
            message = event.get("message")
            if not isinstance(message, dict):
                continue
            text = message.get("text")
            if not isinstance(text, str):
                continue
            sender = event.get("sender") or {}
            sender_id = str(sender.get("id") or "")
            mid = str(message.get("mid") or "")
            if not sender_id or not mid:
                continue
            results.append(
                InboundMessage(
                    sender_id=sender_id,
                    text=text,
                    message_id=mid,
                    is_echo=bool(message.get("is_echo")),
                )
            )
    return results
