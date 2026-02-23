# Tasks -- AG_DeepResearch_Salud_Chile

> Cross-project task delegation board.
> Managed by `AG_Plantilla/scripts/cross_task.py`.
>
> **Agents**: Check this file on session start for pending incoming tasks.


## Local Tasks

(none)

## Incoming (tasks requested to this project)

(none)

## Outgoing (tasks delegated to other projects)

(none)

## Completed

### TASK-LOCAL-001: Archive dead FastAPI code ✅

- **Priority**: P2-Medium
- **Status**: DONE (2026-02-18)
- **Description**: Archived `src/main_fastapi.bak`, `src/services/agent_service.py`, `src/models/schemas.py` to `src/_archived/`. Updated module `__init__.py` files.

### TASK-LOCAL-002: Increase test coverage ✅

- **Priority**: P1-High
- **Status**: DONE (2026-02-18)
- **Description**: Created 3 new test files: `test_config.py` (3 tests), `test_tools.py` (2 tests), `test_researcher.py` (4 tests). Coverage now spans vault, config, tools, and researcher modules. All tests pass.

### TASK-LOCAL-003: Implement cmd_sync() ✅

- **Priority**: P3-Low
- **Status**: DONE (2026-02-18)
- **Description**: Replaced stub with functional vault status reporter (source/finding/log counts).

### TASK-LOCAL-004: Consolidate duplicate schemas ✅

- **Priority**: P2-Medium
- **Status**: DONE (2026-02-18)
- **Description**: Archived `src/models/schemas.py` (FastAPI-era). Active schemas remain in `src/schemas/agent.py`.

### TASK-LOCAL-005: Clean empty source directories ✅

- **Priority**: P3-Low
- **Status**: DONE (2026-02-18)
- **Description**: Removed empty `src/output_generators/` and `src/tools/` directories.

### TASK-LOCAL-006: Update requirements.txt ✅

- **Priority**: P2-Medium
- **Status**: DONE (2026-02-18)
- **Description**: Added `pydantic`, `pydantic-settings`, `structlog`. Removed unused `ddgs`. Created `requirements-dev.txt` with pytest/pytest-cov/pytest-asyncio.

### TASK-LOCAL-007: Consolidate docs/TODO.md ✅

- **Priority**: P3-Low
- **Status**: DONE (2026-02-18)
- **Description**: Archived `docs/TODO.md` to `docs/_archived/TODO.md`. All relevant items migrated to Local Tasks.

### TASK-LOCAL-008: Move install-global scripts ✅

- **Priority**: P3-Low
- **Status**: DONE (2026-02-18)
- **Description**: Moved `install-global.ps1` and `install-global.sh` from root to `scripts/`.

### TASK-LOCAL-009: Update README.md ✅

- **Priority**: P2-Medium
- **Status**: DONE (2026-02-18)
- **Description**: Rewrote README.md with CLI usage examples, architecture diagram, dependency table, installation instructions (~100 lines).

### TASK-LOCAL-010: Add research_topics.yaml config ✅

- **Priority**: P3-Low
- **Status**: DONE (2026-02-18)
- **Description**: Created `config/research_topics.yaml` with 5 Chilean health research domains (MINSAL, FONASA, ISP, Superintendencia, Ley 21.180).

### TASK-2026-0007: Create project-specific workflows ✅

- **From**: AG_Plantilla
- **Priority**: P3-Low
- **Status**: DONE
- **Created**: 2026-02-18
- **Completed**: 2026-02-18
- **Description**: Created `turbo-ops.md` and `deep-research-update.md` from AG_Plantilla template.

### [P2] EVALUATE AGENTS AND SKILLS ✅

- Status: **DONE** (2026-02-18)
- Source: AG_Plantilla (ecosystem consolidation 2026-02-18)
- All 7 agents relevant. 1 Claude skill + 3 Gemini skills kept. 2 workflows created.

### [NORMALIZATION] Full Normalization 2026-02-18 ✅

- Status: **DONE** (2026-02-18)
- Source: Manual execution from AG_Plantilla standard
- Pre-score: 66/100 → Post-score: 90/100
- Report: `docs/audit/audit_normalization_2026-02-18.md`
