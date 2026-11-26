"""Read Meta Instagram adapter settings from environment."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class MetaSettings:
    verify_token: str
    app_secret: str
    page_access_token: str
    api_version: str = "v21.0"
    ig_account_id: str | None = None


def _repo_root() -> Path:
    # backend/src/backend/infrastructure/meta_settings.py → repo root
    return Path(__file__).resolve().parents[4]


def load_dotenv(path: Path | None = None) -> None:
    """Load KEY=VALUE from repo .env without overriding existing env."""
    target = path or (_repo_root() / ".env")
    if not target.exists():
        return
    for raw in target.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key:
            os.environ.setdefault(key, value)


def load_meta_settings(environ: dict[str, str] | None = None) -> MetaSettings:
    if environ is None:
        load_dotenv()
        env: dict[str, str] = dict(os.environ)
    else:
        env = environ
    ig_raw = (env.get("META_IG_ACCOUNT_ID") or "").strip()
    return MetaSettings(
        verify_token=env.get("META_VERIFY_TOKEN", ""),
        app_secret=env.get("META_APP_SECRET", ""),
        page_access_token=env.get("META_PAGE_ACCESS_TOKEN", ""),
        api_version=env.get("META_API_VERSION") or "v21.0",
        ig_account_id=ig_raw or None,
    )
