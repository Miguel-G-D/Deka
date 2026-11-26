"""Meta settings from environment."""

from pathlib import Path

from backend.infrastructure.meta_settings import load_dotenv, load_meta_settings


def test_load_dotenv_sets_missing_keys(tmp_path: Path, monkeypatch) -> None:
    env_file = tmp_path / ".env"
    env_file.write_text(
        "META_VERIFY_TOKEN=from-file\n# comment\nEMPTY=\n",
        encoding="utf-8",
    )
    monkeypatch.delenv("META_VERIFY_TOKEN", raising=False)
    load_dotenv(env_file)
    assert load_meta_settings({"META_VERIFY_TOKEN": "from-file"}).verify_token == (
        "from-file"
    )
    # After load_dotenv, os.environ should have the key
    import os

    assert os.environ.get("META_VERIFY_TOKEN") == "from-file"


def test_load_meta_settings_from_environ() -> None:
    settings = load_meta_settings(
        {
            "META_VERIFY_TOKEN": "vt",
            "META_APP_SECRET": "secret",
            "META_PAGE_ACCESS_TOKEN": "token",
            "META_API_VERSION": "v19.0",
            "META_IG_ACCOUNT_ID": "igid-1",
        }
    )
    assert settings.verify_token == "vt"
    assert settings.app_secret == "secret"
    assert settings.page_access_token == "token"
    assert settings.api_version == "v19.0"
    assert settings.ig_account_id == "igid-1"


def test_empty_ig_account_id_becomes_none() -> None:
    settings = load_meta_settings(
        {
            "META_VERIFY_TOKEN": "vt",
            "META_APP_SECRET": "secret",
            "META_PAGE_ACCESS_TOKEN": "token",
            "META_IG_ACCOUNT_ID": "  ",
        }
    )
    assert settings.api_version == "v21.0"
    assert settings.ig_account_id is None
