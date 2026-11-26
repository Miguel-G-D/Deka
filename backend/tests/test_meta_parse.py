"""Parse Instagram webhook payloads into InboundMessage."""

from backend.infrastructure.meta_parse import parse_instagram_inbound


def test_parses_instagram_text_message() -> None:
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
    messages = parse_instagram_inbound(payload)
    assert len(messages) == 1
    assert messages[0].sender_id == "igsid-1"
    assert messages[0].text == "hola"
    assert messages[0].message_id == "mid-1"
    assert messages[0].is_echo is False


def test_parses_echo_flag() -> None:
    payload = {
        "object": "instagram",
        "entry": [
            {
                "id": "igid-1",
                "messaging": [
                    {
                        "sender": {"id": "igid-1"},
                        "recipient": {"id": "igsid-1"},
                        "message": {
                            "mid": "mid-2",
                            "text": "reply",
                            "is_echo": True,
                        },
                    }
                ],
            }
        ],
    }
    messages = parse_instagram_inbound(payload)
    assert len(messages) == 1
    assert messages[0].is_echo is True


def test_ignores_non_instagram_object() -> None:
    assert parse_instagram_inbound({"object": "page", "entry": []}) == []


def test_filters_by_ig_account_id() -> None:
    payload = {
        "object": "instagram",
        "entry": [
            {
                "id": "igid-other",
                "messaging": [
                    {
                        "sender": {"id": "igsid-1"},
                        "message": {"mid": "m", "text": "x"},
                    }
                ],
            },
            {
                "id": "igid-mine",
                "messaging": [
                    {
                        "sender": {"id": "igsid-2"},
                        "message": {"mid": "m2", "text": "y"},
                    }
                ],
            },
        ],
    }
    messages = parse_instagram_inbound(payload, ig_account_id="igid-mine")
    assert len(messages) == 1
    assert messages[0].sender_id == "igsid-2"


def test_skips_events_without_text_message() -> None:
    payload = {
        "object": "instagram",
        "entry": [
            {
                "id": "igid-1",
                "messaging": [
                    {"sender": {"id": "igsid-1"}, "read": {"mid": "m"}},
                    {
                        "sender": {"id": "igsid-1"},
                        "message": {"mid": "m2", "attachments": [{"type": "image"}]},
                    },
                ],
            }
        ],
    }
    assert parse_instagram_inbound(payload) == []
