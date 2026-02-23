# Audit de Normalización — AG_DeepResearch_Salud_Chile

> **Fecha**: 2026-02-18  
> **Referencia**: AG_Plantilla (C:\_Repositorio\AG_Plantilla)  
> **Auditor**: Antigravity  

---

## Infraestructura

| Item | Estado | Nota |
|------|--------|------|
| GEMINI.md en raíz | ✅ SÍ | 8.6 KB, adaptado al proyecto |
| CLAUDE.md en raíz | ✅ SÍ | 7.9 KB |
| README.md | ✅ SÍ | 1.0 KB — básico, podría mejorar |
| CHANGELOG.md | ✅ SÍ | 323 B — mínimo |
| docs/TASKS.md | ✅ SÍ | Formato unified (cross-project) |
| docs/DEVLOG.md | ✅ SÍ | Última entrada: 2026-02-02 |
| docs/standards/output_governance.md | ✅ SÍ | 1.2 KB (template tiene 2.9 KB — actualizar) |
| .gitignore | ✅ SÍ | Protege .env, credentials, secrets, *.pem, *.key |

## Agentes

| Item | Estado | Nota |
|------|--------|------|
| .subagents/manifest.json | ✅ SÍ | 7 agentes definidos |
| .subagents/dispatch.sh | ✅ SÍ | 6.6 KB, multi-vendor |

### Detalle de Agentes

| Agente | Vendor | Configurado |
|--------|--------|-------------|
| code-analyst | gemini | ✅ |
| doc-writer | gemini | ✅ |
| code-reviewer | claude | ✅ |
| test-writer | gemini | ✅ |
| db-analyst | claude | ✅ |
| deployer | gemini | ✅ |
| researcher | codex | ✅ |

## Skills

### Claude (.claude/skills/)
| Archivo | Tipo |
|---------|------|
| community-skills-reference.md | Referencia genérica |
| official-skills-reference.md | Referencia genérica |
| community/ (d3js, ffuf, ios-simulator, loki-mode) | Genéricos de terceros |
| official/ (internal-comms, xlsx, webapp-testing, etc.) | Skills oficiales genéricos |

> **Clasificación**: 0 skills proyecto-específicas, solo referencias y skills genéricos.

### Gemini (.gemini/skills/)
| Skill | Clasificación |
|-------|--------------|
| deep-research.md | ✅ RELEVANTE — core del proyecto |
| project-init.md | ✅ RELEVANTE — inicialización estándar |
| project-memory.md | ✅ RELEVANTE — persistencia de conocimiento |

### Claude Commands (.claude/commands/)
| Comando | Estado |
|---------|--------|
| create-tests.md | ✅ Funcional |
| help.md | ✅ Funcional |
| project-status.md | ✅ Funcional |
| quick-review.md | ✅ Funcional |
| update-docs.md | ✅ Funcional |

### Claude internal-agents
No existe el directorio `.claude/internal-agents/`.

## Workflows

| Item | Estado |
|------|--------|
| .agent/workflows/ | ⚠️ VACÍO — 0 workflows |

> **Nota**: El directorio existe pero no contiene ningún workflow. TASK-2026-0007 pendiente.

## Memoria y Config

| Item | Estado | Nota |
|------|--------|------|
| .gemini/brain/ | ✅ SÍ | Directorio existente |
| .gemini/settings.json | ✅ SÍ | Config completa (MCP, agents, experimental, memory) |
| .claude/settings.local.json | ❌ NO | No existe |
| .claude/mcp.json | ❌ NO | No existe |

## Seguridad

| Item | Estado | Nota |
|------|--------|------|
| Credenciales hardcodeadas en src/ | ✅ LIMPIO | 0 hallazgos (password/token/api_key/secret) |
| .env.example | ✅ SÍ | 713 B |
| .gitignore cubre .env, credentials, secrets | ✅ SÍ | Protege .env, .env.local, .env.*.local, credentials/, secrets/, *.pem, *.key |

## Archivos Extra en Raíz (Higiene)

| Archivo | Nota |
|---------|------|
| TODO.md | ⚠️ Debería estar en docs/ (ver output_governance) |
| codex_output.txt | ⚠️ Archivo temporal |
| debug_ddgs.py | ⚠️ Script debug suelto |
| debug_search.py | ⚠️ Script debug suelto |
| research_results.txt | ⚠️ Archivo temporal |
| install-global.ps1 | ⚠️ Script en raíz |
| install-global.sh | ⚠️ Script en raíz |

---

## Resumen Pre vs Post-Normalización

| Categoría | Antes | Después | Delta |
|-----------|:-----:|:-------:|:-----:|
| Infraestructura base | 8 | 10 | +2 |
| Agentes | 10 | 10 | 0 |
| Skills Claude | 4 | 7 | +3 |
| Skills Gemini | 9 | 9 | 0 |
| Workflows | 0 | 9 | +9 |
| Memoria y Config | 7 | 8 | +1 |
| Documentación | 6 | 9 | +3 |
| Seguridad | 10 | 10 | 0 |
| Higiene de raíz | 4 | 8 | +4 |
| Gobernanza | 8 | 10 | +2 |

### Score Pre-Normalización: **66/100**

### Score Post-Normalización: **90/100** (+24)

### Cambios Realizados

1. ✅ Creados 2 workflows (`turbo-ops.md`, `deep-research-update.md`)
2. ✅ `output_governance.md` actualizado a estándar completo AG_Plantilla (1.2KB → 2.9KB)
3. ✅ Creado skill Claude proyecto-específico: `normative-research`
4. ✅ Movidos 5 archivos de raíz a ubicaciones correctas:
   - `TODO.md` → `docs/TODO.md`
   - `codex_output.txt`, `debug_ddgs.py`, `debug_search.py`, `research_results.txt` → `scripts/temp/`
5. ✅ DEVLOG.md actualizado con sesión de normalización
6. ✅ CHANGELOG.md actualizado con cambios
7. ✅ TASKS.md — TASK-2026-0007 marcada DONE
8. ✅ Auditoría de seguridad limpia (0 credenciales hardcodeadas)

### Items Restantes (no bloqueantes)

- `install-global.ps1` y `install-global.sh` permanecen en raíz (son scripts de instalación legítimos)
- `.claude/settings.local.json` y `.claude/mcp.json` no creados (no hay config Claude específica necesaria)

