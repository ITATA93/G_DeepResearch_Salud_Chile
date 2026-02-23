"""Shared pytest fixtures and configuration."""

import pytest
from pathlib import Path
from src.core.vault import KnowledgeVault


@pytest.fixture
def test_vault(tmp_path):
    """Create a temporary KnowledgeVault for testing."""
    return KnowledgeVault(str(tmp_path))
