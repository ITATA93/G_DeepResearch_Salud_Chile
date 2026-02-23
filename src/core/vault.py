import sqlite3
import json
from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path


class KnowledgeVault:
    """
    Standard Antigravity Knowledge Vault (v1.1).
    Manages the persistent SQLite memory for the project.
    Now supports Deep Research findings and Content Archival.
    """

    def __init__(self, project_root: str):
        self.root = Path(project_root)
        self.data_dir = self.root / "data"
        self.db_path = self.data_dir / "knowledge_vault.db"
        self._setup()

    def _setup(self):
        """Ensure data directory and database schema exist."""
        if not self.data_dir.exists():
            self.data_dir.mkdir(parents=True, exist_ok=True)

        self._init_db()

    def _init_db(self):
        """Initialize the Universal SQL Schema."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # 1. Sources Index (Inventario de Fuentes - Files/URLs)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sources_index (
                folio_id TEXT PRIMARY KEY,
                file_name TEXT NOT NULL,
                file_hash TEXT,
                source_url TEXT,
                institution TEXT,
                ingestion_date TEXT,
                validity_status TEXT DEFAULT 'active'
            )
        """)

        # 2. Findings Memory (Memoria de Hallazgos - Atomic Facts)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS findings_memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                folio_id TEXT NOT NULL,
                topic TEXT NOT NULL,
                content TEXT NOT NULL,
                finding_type TEXT DEFAULT 'general',
                confidence_score REAL DEFAULT 1.0,
                FOREIGN KEY(folio_id) REFERENCES sources_index(folio_id)
            )
        """)

        # 3. Audit Log (Trazabilidad)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS audit_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                operation TEXT,
                details TEXT
            )
        """)

        conn.commit()
        conn.close()

    def register_source(
        self,
        folio_id: str,
        file_name: str,
        file_hash: str,
        metadata: Dict[str, Any] = None,
    ):
        """Register or update a source in the vault."""
        if metadata is None:
            metadata = {}

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        now = datetime.now().isoformat()

        try:
            cursor.execute(
                """
                INSERT OR REPLACE INTO sources_index
                (folio_id, file_name, file_hash, source_url, institution, ingestion_date, validity_status)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    folio_id,
                    file_name,
                    file_hash,
                    metadata.get("url"),
                    metadata.get("institution", "Unknown"),
                    now,
                    "active",
                ),
            )
            conn.commit()
            self.log_operation(
                "REGISTER_SOURCE", {"folio": folio_id, "file": file_name}
            )
        except Exception as e:
            print(f"[Vault Error] Failed to register source {folio_id}: {e}")
        finally:
            conn.close()

    def add_finding(
        self,
        folio_id: str,
        topic: str,
        content: str,
        finding_type: str = "research_note",
    ):
        """Store a specific finding or extracted content block linked to a source."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO findings_memory (folio_id, topic, content, finding_type)
                VALUES (?, ?, ?, ?)
                """,
                (folio_id, topic, content, finding_type),
            )
            conn.commit()
        finally:
            conn.close()

    def get_findings(self, topic_filter: str = None) -> List[tuple]:
        """Retrieve findings, optionally filtered by topic."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            if topic_filter:
                cursor.execute(
                    "SELECT * FROM findings_memory WHERE topic LIKE ?",
                    (f"%{topic_filter}%",),
                )
            else:
                cursor.execute("SELECT * FROM findings_memory")
            return cursor.fetchall()
        finally:
            conn.close()

    def log_operation(self, operation: str, details: Dict[str, Any]):
        """Log an operational event."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO audit_log (operation, details) VALUES (?, ?)",
                (operation, json.dumps(details)),
            )
            conn.commit()
        finally:
            conn.close()
