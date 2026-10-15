"""Application settings. All values come from env vars or `.env`."""

from functools import lru_cache
from pathlib import Path

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Paths
    raw_pdf_path: Path = Path("data/raw/egyptian_civil_code.pdf")
    corpus_path: Path = Path("data/processed/articles.json")
    qdrant_path: Path = Path("data/index")
    qdrant_collection: str = "civil_code"

    # Retrieval
    embedding_model: str = "BAAI/bge-m3"
    top_k: int = 5

    # LLM provider "api" (OpenRouter)
    api_llm_base_url: str = "https://openrouter.ai/api/v1"
    api_llm_model: str = ""
    llm_api_key: SecretStr | None = None

    # LLM provider "local" (vLLM)
    local_llm_base_url: str = "http://vllm:8000/v1"
    local_llm_model: str = "Qwen/Qwen2.5-1.5B-Instruct-AWQ"

    # Tracking
    mlflow_tracking_uri: str = "http://localhost:5000"

    # Logging
    log_level: str = "INFO"


@lru_cache
def get_settings() -> Settings:
    """Return one shared Settings instance."""
    return Settings()
