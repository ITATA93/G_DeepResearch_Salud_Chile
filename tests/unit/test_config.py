"""Unit tests for Settings configuration."""

import os
import pytest
from unittest.mock import patch


def test_settings_default_values():
    """Test that Settings loads with correct defaults."""
    # Clear any env vars that might interfere
    env_overrides = {
        "API_KEY": "test-key",
        "APP_ENV": "development",
    }
    with patch.dict(os.environ, env_overrides, clear=False):
        from src.config import Settings
        settings = Settings()
        assert settings.app_name == "Antigravity Workspace"
        assert settings.environment == "development"
        assert settings.debug is False
        assert settings.port == 8000
        assert settings.log_level == "INFO"


def test_settings_rejects_default_api_key_in_production():
    """Test that production rejects placeholder API keys."""
    env_overrides = {
        "APP_ENV": "production",
        "API_KEY": "change-me",
    }
    with patch.dict(os.environ, env_overrides, clear=False):
        from src.config import Settings
        with pytest.raises(ValueError, match="API_KEY must be set"):
            Settings()


def test_settings_accepts_real_api_key_in_production():
    """Test that production accepts a real API key."""
    env_overrides = {
        "APP_ENV": "production",
        "API_KEY": "real-secure-key-12345",
    }
    with patch.dict(os.environ, env_overrides, clear=False):
        from src.config import Settings
        settings = Settings()
        assert settings.api_key == "real-secure-key-12345"
