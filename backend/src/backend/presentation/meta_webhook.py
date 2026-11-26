"""Meta Instagram webhook routes."""

from __future__ import annotations

import json
from typing import Annotated

from fastapi import APIRouter, Depends, Header, HTTPException, Query, Request, Response
from fastapi.responses import PlainTextResponse

from backend.application.inbound import HandleInboundMessage
from backend.infrastructure.meta_parse import parse_instagram_inbound
from backend.infrastructure.meta_settings import MetaSettings
from backend.infrastructure.meta_signature import verify_signature
from backend.presentation.deps import get_inbound_use_case, get_meta_settings

router = APIRouter(tags=["meta"])


@router.get("/webhooks/meta")
def verify_meta_webhook(
    hub_mode: Annotated[str | None, Query(alias="hub.mode")] = None,
    hub_verify_token: Annotated[str | None, Query(alias="hub.verify_token")] = None,
    hub_challenge: Annotated[str | None, Query(alias="hub.challenge")] = None,
    settings: MetaSettings = Depends(get_meta_settings),
) -> Response:
    if (
        hub_mode == "subscribe"
        and hub_verify_token is not None
        and hub_verify_token == settings.verify_token
        and hub_challenge is not None
    ):
        return PlainTextResponse(content=hub_challenge, status_code=200)
    raise HTTPException(status_code=403, detail="Forbidden")


@router.post("/webhooks/meta")
async def receive_meta_webhook(
    request: Request,
    settings: MetaSettings = Depends(get_meta_settings),
    use_case: HandleInboundMessage = Depends(get_inbound_use_case),
    x_hub_signature_256: Annotated[str | None, Header()] = None,
) -> dict[str, str]:
    body = await request.body()
    if not verify_signature(body, x_hub_signature_256, settings.app_secret):
        raise HTTPException(status_code=403, detail="Invalid signature")

    try:
        payload = json.loads(body.decode("utf-8") or "{}")
    except json.JSONDecodeError as exc:
        raise HTTPException(status_code=400, detail="Invalid JSON") from exc

    if not isinstance(payload, dict):
        return {"status": "ok"}

    for inbound in parse_instagram_inbound(payload, settings.ig_account_id):
        use_case.execute(inbound)
    return {"status": "ok"}
