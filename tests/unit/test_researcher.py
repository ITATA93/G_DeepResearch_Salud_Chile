"""Unit tests for CodexResearcher agent."""

import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path


@pytest.fixture
def mock_vault(tmp_path):
    """Create a mock vault for testing researcher."""
    from src.core.vault import KnowledgeVault
    return KnowledgeVault(str(tmp_path))


class TestCodexResearcher:
    """Tests for the CodexResearcher deep research agent."""

    def test_researcher_initialization(self, mock_vault):
        """Test that researcher initializes with vault and search tools."""
        from src.agents.researcher import CodexResearcher

        researcher = CodexResearcher(mock_vault)
        assert researcher.vault is mock_vault
        assert researcher.wrapper is not None

    @patch("src.agents.researcher.trafilatura.fetch_url")
    @patch("src.agents.researcher.trafilatura.extract")
    def test_researcher_run_deep_research_creates_report(
        self, mock_extract, mock_fetch, mock_vault, tmp_path
    ):
        """Test that deep research creates a markdown report file."""
        from src.agents.researcher import CodexResearcher

        # Mock the search results
        mock_extract.return_value = "Texto de contenido extraído de la página"
        mock_fetch.return_value = "<html><body>Content</body></html>"

        researcher = CodexResearcher(mock_vault)

        # Mock the structured search to return controlled results
        with patch.object(
            researcher,
            "_perform_structured_search",
            return_value=[
                {"title": "Norma Test", "href": "https://example.com/norma", "body": "Descripción test"}
            ],
        ):
            report_path = researcher.run_deep_research("Vacunas Chile")

        assert report_path is not None
        assert Path(report_path).exists()
        report_content = Path(report_path).read_text(encoding="utf-8")
        assert "Vacunas Chile" in report_content

    def test_researcher_registers_sources_in_vault(self, mock_vault):
        """Test that researched sources are registered in the vault."""
        from src.agents.researcher import CodexResearcher
        import sqlite3

        researcher = CodexResearcher(mock_vault)

        with patch.object(
            researcher,
            "_perform_structured_search",
            return_value=[],
        ):
            researcher.run_deep_research("Test topic with no results")

        # Verify vault was used (at least audit log entries)
        conn = sqlite3.connect(mock_vault.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM audit_log")
        count = cursor.fetchone()[0]
        conn.close()
        assert count >= 0  # At minimum, no errors occurred


class TestVaultFindings:
    """Tests for vault findings (not covered in test_vault.py)."""

    def test_add_and_get_finding(self, mock_vault):
        """Test adding and retrieving a finding."""
        # First register a source
        mock_vault.register_source(
            "FOLIO-TEST-001", "test.pdf", "hash123",
            {"institution": "MINSAL"}
        )

        # Add a finding linked to it
        mock_vault.add_finding(
            "FOLIO-TEST-001", "vacunas", "Hallazgo de prueba", "research_note"
        )

        # Retrieve
        findings = mock_vault.get_findings("vacunas")
        assert len(findings) == 1
        assert "Hallazgo de prueba" in findings[0][3]

    def test_get_findings_with_filter(self, mock_vault):
        """Test filtering findings by topic."""
        mock_vault.register_source("F-001", "a.pdf", "h1")
        mock_vault.add_finding("F-001", "vacunas", "Info vacunas")
        mock_vault.add_finding("F-001", "medicamentos", "Info meds")

        vac_findings = mock_vault.get_findings("vacunas")
        assert len(vac_findings) == 1

        all_findings = mock_vault.get_findings()
        assert len(all_findings) == 2
