"""Application configuration using pydantic-settings."""

from functools import lru_cache

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",  # Allow extra env vars in .env without error
    )

    # Application
    app_name: str = "Antigravity Workspace"
    app_version: str = "1.0.0"
    environment: str = Field("development", validation_alias="APP_ENV")
    debug: bool = Field(False, validation_alias="APP_DEBUG")

    # Paths (F-06: Robust relative paths)
    # Allows identifying root regardless of execution dir
    workspace_root: str = "."  # Can be derived using pathlib in future iteration

    # Server
    host: str = "0.0.0.0"
    port: int = Field(8000, validation_alias="APP_PORT")

    # Security
    api_key: str = Field("change-me", validation_alias="API_KEY")

    @model_validator(mode="after")
    def _check_api_key_not_default(self) -> "Settings":
        """Reject known placeholder API keys in production."""
        forbidden = {"dev-secret-key", "change-me", "change_me", ""}
        if self.environment == "production" and self.api_key in forbidden:
            msg = "API_KEY must be set to a secure value in production (env var API_KEY)"
            raise ValueError(msg)
        return self

    frontend_url: str = Field("http://localhost:3000", validation_alias="FRONTEND_URL")

    # Database (optional)
    database_url: str = "sqlite:///./data/app.db"

    # Logging
    log_level: str = "INFO"
    log_format: str = "json"


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
