import sys
import argparse
from pathlib import Path
import logging

# Add src to path to allow absolute imports within the project
sys.path.append(str(Path(__file__).parent))

from src.core import KnowledgeVault

# Configure Logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("DeepResearch")


def load_system_prompt():
    prompt_path = Path(__file__).parent / "src" / "prompts" / "system_prompt.md"
    if prompt_path.exists():
        return prompt_path.read_text(encoding="utf-8")
    return "SYSTEM PROMPT NOT FOUND"


def cmd_audit(args, vault):
    logger.info(f"Starting Audit for process file: {args.input_file}")
    logger.info("Initializing Agent with System Prompt...")
    _ = load_system_prompt()

    # TODO: Connect to LangChain/LLM here
    # print(f"\n[MOCK AGENT] Reading {args.input_file}...")
    # print("[MOCK AGENT] Identifying keywords: 'Vacunas', 'Cadena de Frio'")
    # print("[MOCK AGENT] Searching Knowledge Vault...")

    from src.core.tools import get_search_tool

    try:
        search_tool = get_search_tool()
        logger.info("Search tool initialized: DuckDuckGo (Region: cl-es)")

        # Simple implementation for now: Search for the file name as a query
        # In a full implementation, this would be an Agent action
        query = f"Normativa Minsal Chile {Path(args.input_file).stem}"
        print(f"\n[AGENT] Executing search for: '{query}'...")
        results = search_tool.invoke(query)
        print(f"\n[AGENT] Search Results:\n{results}\n")

    except Exception as e:
        logger.error(f"Failed to initialize or run search tool: {e}")
        print(f"[ERROR] Could not run search: {e}")

    # Mock Interaction with Vault
    vault.log_operation("AUDIT_START", {"file": args.input_file})
    print(f"[VAULT] Audit session logged in {vault.db_path}")

def cmd_sync(args, vault):
    """Check vault status and report sync state."""
    logger.info("Starting Knowledge Sync...")
    import sqlite3

    conn = sqlite3.connect(vault.db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM sources_index")
    source_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM findings_memory")
    finding_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM audit_log")
    log_count = cursor.fetchone()[0]

    conn.close()

    print(f"[SYNC] Vault: {vault.db_path}")
    print(f"[SYNC] Sources: {source_count} | Findings: {finding_count} | Log entries: {log_count}")
    print("[SYNC] Local Vault status: OK")


def cmd_research(args, vault):
    try:
        from src.agents.researcher import CodexResearcher

        logger.info(f"Starting Research on: {args.query} (Deep Mode: {args.deep})")

        if args.deep:
            # Codex Deep Research Mode
            agent = CodexResearcher(vault)
            report_path = agent.run_deep_research(args.query)
            print("\n[SUCCESS] Deep Research Completed.")
            print(f"Report available at: {report_path}")

        else:
            # Standard Quick Search
            from src.core.tools import get_search_tool

            search_tool = get_search_tool()
            print(f"\n[AGENT] Executing quick search for: '{args.query}'...")
            results = search_tool.invoke(args.query)
            print(f"\n[AGENT] Search Results:\n{results}\n")

    except Exception as e:
        logger.error(f"Failed to run research: {e}")
        print(f"[ERROR] {e}")


def main():
    parser = argparse.ArgumentParser(description="AG_DeepResearch_Salud_Chile CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Command: Audit
    parser_audit = subparsers.add_parser("audit", help="Audit a process document")
    parser_audit.add_argument(
        "input_file", help="Path to the process description (txt/md)"
    )

    # Command: Sync
    subparsers.add_parser(
        "sync", help="Sync knowledge with central vault"
    )

    # Command: Research
    parser_research = subparsers.add_parser(
        "research", help="Perform a direct search query"
    )
    parser_research.add_argument("query", help="Search query string")
    parser_research.add_argument(
        "--deep",
        action="store_true",
        help="Enable Codex Deep Research (Scraping & Archival)",
    )

    args = parser.parse_args()

    # Initialize Vault
    root_dir = Path(__file__).parent
    vault = KnowledgeVault(str(root_dir))

    if args.command == "audit":
        cmd_audit(args, vault)
    elif args.command == "sync":
        cmd_sync(args, vault)
    elif args.command == "research":
        cmd_research(args, vault)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
