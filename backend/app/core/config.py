from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Use-Case Intelligence Platform"
    app_env: str = Field(default="dev", alias="APP_ENV")
    backend_host: str = "0.0.0.0"
    backend_port: int = 8000

    sql_db_url: str = "sqlite:///./data/app.db"
    sql_echo: bool = False

    vector_provider: str = "faiss"
    vector_dimension: int = 384
    vector_index_path: str = "./data/faiss.index"

    embedding_provider: str = "deterministic"

    cors_origins: str = "http://localhost:5173"

    mcp_transport: str = "stdio"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]

    def ensure_data_dirs(self) -> None:
        Path("./data").mkdir(parents=True, exist_ok=True)


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    settings.ensure_data_dirs()
    return settings
