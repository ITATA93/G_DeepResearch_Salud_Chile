"""
Deep Research Agent Strategy (Codex Implementation).
Handles the search, extraction, and synthesis loop.
"""

import hashlib
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

# Third-party imports
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
import trafilatura

from src.core.vault import KnowledgeVault


class CodexResearcher:
    def __init__(self, vault: KnowledgeVault):
        self.vault = vault
        self.wrapper = DuckDuckGoSearchAPIWrapper(
            region="cl-es", time="y", max_results=7
        )
        self.search_tool = DuckDuckGoSearchRun(api_wrapper=self.wrapper)
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")

    def run_deep_research(self, topic: str) -> str:
        """
        Executes the Deep Research Loop:
        1. Search
        2. Extract & Archive
        3. Persist to Memory
        4. Generate Foliated Report
        """
        print(f"\n[CODEX] Initiating Deep Research on: '{topic}'")

        # 1. Search
        print("[CODEX] Phase 1: Discovery (DuckDuckGo)...")
        # Direct use of wrapper to get metadata if possible, but Run gives string.
        # For deeper flows, we ideally want structured results.
        # Using run() for now, which gives a concat string, but we will try to parse or use a different method if needed.
        # Actually, let's use the wrapper directly to get snippets if possible, or just standard search.
        # search_tool.invoke returns a string. We'll do a specialized call to get links.

        # Heuristic: Using the results to find URLs (LangChain's DDG tool is opaque).
        # Better approach for "Deep" research: Use the `ddgs` library directly if available in env,
        # but sticking to configured tools for consistency.
        # We will do a generic search first.

        search_results_text = self.search_tool.invoke(topic)
        print("[CODEX] Found initial context. Analyzing...")

        # Since standard LangChain DDG tool returns a string blob, we can't easily extract URLs for scraping
        # without parsing. For a TRUE Deep Research, let's use `ddgs` directly which we installed.
        results = self._perform_structured_search(topic)

        captured_evidence = []

        # 2. Extract & Archive
        print(f"[CODEX] Phase 2: Extraction & Archival ({len(results)} sources)...")
        for i, res in enumerate(results):
            url = res.get("href")
            title = res.get("title")

            if not url:
                continue

            print(f"  > Processing: {title[:50]}...")

            # Generate Folio ID
            folio_id = f"DR-{self.session_id}-{i + 1:03d}"

            # Scrape content
            downloaded = trafilatura.fetch_url(url)
            content_text = trafilatura.extract(downloaded) if downloaded else None

            if content_text:
                # Calculate Hash
                content_hash = hashlib.sha256(content_text.encode("utf-8")).hexdigest()

                # 3. Persist to Vault
                # Register Source
                self.vault.register_source(
                    folio_id=folio_id,
                    file_name=f"{folio_id}_{title[:20]}.txt",  # Virtual filename
                    file_hash=content_hash,
                    metadata={"url": url, "institution": "WebSource"},
                )

                # Store Findings (The Content)
                self.vault.add_finding(
                    folio_id=folio_id,
                    topic=topic,
                    content=content_text,
                    finding_type="full_extraction",
                )

                captured_evidence.append(
                    {
                        "folio": folio_id,
                        "title": title,
                        "url": url,
                        "snippet": content_text[:300].replace("\n", " ") + "...",
                    }
                )
            else:
                print(f"    [!] Failed to extract content from {url}")

        # 4. Generate Foliated Report
        report_path = self._generate_report(
            topic, captured_evidence, search_results_text
        )
        return report_path

    def _perform_structured_search(self, query: str) -> List[Dict[str, Any]]:
        """
        Uses explicit duckduckgo_search library to get structured results (URLs).
        Includes fallbacks for 0-result scenarios.
        Ref: installed via requirements.txt
        """
        from duckduckgo_search import DDGS

        results = []
        
        # Strategy 1: Direct Specific Search
        try:
            print(f"[CODEX] Strategy 1: Precise Search for '{query}'...")
            with DDGS() as ddgs:
                for r in ddgs.text(query, region="cl-es", timelimit="y", max_results=5):
                    results.append(r)
        except Exception as e:
            print(f"[CODEX] Strategy 1 failed: {e}")

        # Strategy 2: Broader Search (Key Terms only) if Strategy 1 empty
        if not results:
            # Extract key nouns/terms - simplified for now
            broader_query = " ".join(query.split()[:4]) # First 4 words as heuristic
            print(f"[CODEX] Strategy 2: Broader Search for '{broader_query}'...")
            try:
                with DDGS() as ddgs:
                    for r in ddgs.text(broader_query, region="cl-es", timelimit="y", max_results=5):
                        results.append(r)
            except Exception as e:
                print(f"[CODEX] Strategy 2 failed: {e}")

        # Strategy 3: LangChain Wrapper Fallback
        if not results:
             print("[CODEX] Strategy 3: LangChain Wrapper Fallback...")
             try:
                 # The wrapper is initialized in __init__
                 # We need to map the keys because LangChain returns 'link'/'snippet', DDGS returns 'href'/'body' -> we normalize to 'href'/'title'/'body'
                 lc_results = self.wrapper.results(query, max_results=5)
                 for item in lc_results:
                     results.append({
                         "href": item.get("link"),
                         "title": item.get("title"),
                         "body": item.get("snippet")
                     })
             except Exception as e:
                 print(f"[CODEX] Strategy 3 failed: {e}")

        return results

    def _generate_report(
        self, topic: str, evidence: List[Dict], summary_context: str
    ) -> str:
        """Writes the Markdown report."""
        report_filename = f"DR-{self.session_id}_Resumen.md"
        report_dir = Path("docs/research")
        report_dir.mkdir(parents=True, exist_ok=True)
        report_path = report_dir / report_filename

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

        # Basic File Type Detection for labeling
        for item in evidence:
            url_lower = item['url'].lower()
            if url_lower.endswith('.pdf'):
                item['type'] = 'PDF'
                item['icon'] = '📄'
            elif url_lower.endswith('.doc') or url_lower.endswith('.docx'):
                item['type'] = 'DOC'
                item['icon'] = '📝'
            else:
                item['type'] = 'WEB'
                item['icon'] = '🌐'

        md_content = f"""# Informe de Investigación Profunda: {topic}
**Folio Sesión:** {self.session_id}
**Agente:** Codex DeepResearcher
**Fecha:** {timestamp}

## 1. Resumen Ejecutivo
(Contexto preliminar recuperado)
{summary_context[:1500]}...

## 2. Inventario de Recursos (Descargas y Enlaces)
Este inventario consolida todos los activos digitales identificados durante la sesión de investigación.

| Tipo | Folio | Título (Clic para Descargar/Ver) | Fuente / Dominio |
|:----:|-------|----------------------------------|------------------|
"""

        for item in evidence:
            domain = item['url'].split('/')[2] if '//' in item['url'] else 'External'
            md_content += f"| {item['icon']} **{item['type']}** | `{item['folio']}` | [{item['title']}]({item['url']}) | {domain} |\n"

        md_content += f"""
## 3. Evidencia y Hallazgos Detallados
Análisis de contenido extraído de las fuentes recuperadas.

Se han archivado {len(evidence)} fuentes en la Bóveda de Conocimiento (Knowledge Vault).
"""

        for item in evidence:
            md_content += f"""
### {item['icon']} {item['title']}
**Folio:** `{item['folio']}` | **Fuente:** {item['url']}

> **Extracto Relevante:**
> {item['snippet']}

---
"""

        report_path.write_text(md_content, encoding="utf-8")
        print(f"\n[CODEX] Report Generated: {report_path}")
        return str(report_path)
