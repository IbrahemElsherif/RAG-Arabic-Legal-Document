from pathlib import Path

from legal_rag.config import Settings, get_settings


def test_defaults(monkeypatch):
    monkeypatch.delenv("LLM_API_KEY", raising=False)
    settings = Settings(_env_file=None)
    assert settings.embedding_model == "BAAI/bge-m3"
    assert settings.qdrant_path == Path("data/index")
    assert settings.llm_api_key is None


def test_env_override(monkeypatch):
    monkeypatch.setenv("TOP_K", "8")
    monkeypatch.setenv("LLM_API_KEY", "sk-secret")
    settings = Settings(_env_file=None)
    assert settings.top_k == 8
    assert settings.llm_api_key.get_secret_value() == "sk-secret"
    # The key must never appear in a repr or a log line.
    assert "sk-secret" not in repr(settings)


def test_get_settings_is_cached():
    assert get_settings() is get_settings()
