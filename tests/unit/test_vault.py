"""Unit tests for KnowledgeVault."""

import pytest
import sqlite3
from pathlib import Path
from src.core.vault import KnowledgeVault


def test_vault_initialization(test_vault):
    """Test that the vault initializes and creates the database."""
    assert test_vault.db_path.exists()

    conn = sqlite3.connect(test_vault.db_path)
    cursor = conn.cursor()

    # Check tables exist
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall()]

    assert "sources_index" in tables
    assert "audit_log" in tables
    conn.close()


def test_register_source(test_vault):
    """Test registering a source file."""
    folio = "TEST-001"
    filename = "test_doc.pdf"
    filehash = "abc123hash"

    test_vault.register_source(folio, filename, filehash, {"institution": "Minsal"})

    conn = sqlite3.connect(test_vault.db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sources_index WHERE folio_id=?", (folio,))
    row = cursor.fetchone()
    conn.close()

    assert row is not None
    assert row[0] == folio
    assert row[1] == filename


def test_audit_log(test_vault):
    """Test that operations are logged."""
    test_vault.log_operation("TEST_OP", {"status": "ok"})

    conn = sqlite3.connect(test_vault.db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM audit_log WHERE operation=?", ("TEST_OP",))
    row = cursor.fetchone()
    conn.close()

    assert row is not None
    assert "TEST_OP" in row[2]
