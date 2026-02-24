# G_DeepResearch_Salud_Chile

> Satellite project in the Antigravity ecosystem — Gemini CLI variant.

**Domain:** `01_HOSPITAL_PRIVADO`
**Status:** Active
**Orchestrator:** GEN_OS
**Prefix:** G_
**AG Counterpart:** `AG_DeepResearch_Salud_Chile`

## Proposito

Agente de investigacion profunda sobre regulaciones y normativas del sistema de
salud chileno (MINSAL, FONASA, ISP, Superintendencia de Salud).

- Busqueda normativa focalizada en fuentes regulatorias chilenas
- Auditoria de procesos contra normativa vigente
- Knowledge Vault con persistencia SQLite y trazabilidad (folio)
- Generacion de reportes foliados con fuentes citadas

## Arquitectura

```
G_DeepResearch_Salud_Chile/
├── .gemini/              # Configuracion Gemini CLI
├── .claude/              # Configuracion Claude Code + skills
├── .subagents/           # Dispatch multi-vendor
├── src/                  # Codigo fuente
│   ├── agents/           # Agentes de investigacion (CodexResearcher)
│   ├── core/             # Tools (DuckDuckGo) y Vault (SQLite)
│   ├── prompts/          # System prompts para agentes
│   └── schemas/          # Pydantic schemas
├── config/               # Registro del proyecto y topics
├── data/                 # Input, knowledge_vault.db, output
├── tests/                # Tests unitarios
├── docs/                 # Documentacion y estandares
└── exports/              # Exportaciones de sesion
```

## Uso con Gemini CLI

```bash
# Investigacion rapida de normativa
gemini "Busca la norma tecnica de cadena de frio MINSAL vigente"

# Auditoria de proceso contra normativa
gemini "Audita el proceso de vacunacion contra normativa MINSAL 2026"

# Investigacion profunda
gemini "Investiga guia clinica de vacunacion Chile 2026 con fuentes"

# Estado del vault
gemini "Muestra el estado actual del knowledge vault y hallazgos recientes"
```

## Scripts

| Script | Ubicacion | Funcion |
|--------|-----------|---------|
| `main.py` | Raiz | Punto de entrada CLI (audit, research, sync) |
| `researcher.py` | `src/agents/` | Deep Research Loop |
| `tools.py` | `src/core/` | Herramientas de busqueda (DuckDuckGo) |
| `vault.py` | `src/core/` | Knowledge Vault SQLite foliado |

## Configuracion

- `GEMINI.md` -- Perfil del proyecto para Gemini CLI
- `CLAUDE.md` -- Instrucciones para Claude Code
- `config/research_topics.yaml` -- Temas de investigacion programados
- `requirements.txt` -- Dependencias Python (langchain, trafilatura, structlog)

## Dependencias Principales

| Paquete | Proposito |
|---------|-----------|
| langchain | Framework de agentes |
| duckduckgo-search | Busqueda gratuita (sin API key) |
| trafilatura | Extraccion de texto web |
| pydantic | Validacion de datos |
| structlog | Logging estructurado |

## Proyectos Relacionados

| Proyecto | Sinergia |
|----------|----------|
| `G_Informatica_Medica` | Estandares de salud y normativa |
| `G_Hospital` | Procesos hospitalarios documentados |
| `G_Consultas` | Datos clinicos para contexto |
