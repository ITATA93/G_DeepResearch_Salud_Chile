# MEGA-PROMPT: Configuración Completa del Sistema Agéntico

> **INSTRUCCIÓN PRINCIPAL**: Eres el agente arquitecto de este proyecto. Tu misión es configurar
> un sistema de desarrollo agéntico completo con sub-agentes, skills oficiales, y una estructura
> de workspace profesional. Ejecuta TODAS las fases en orden. No pidas confirmación entre fases
> a menos que haya un error crítico. Al terminar cada fase, reporta brevemente qué se creó.

---

## CONTEXTO DEL PROYECTO

- **Desarrollador**: Cirujano e ingeniero de sistemas hospitalarios
- **Hospital**: Hospital de Ovalle, Chile
- **Sistema clínico**: ALMA (basado en InterSystems TrakCare), SQL Server
- **Objetivo**: Construir herramientas de gestión hospitalaria (turnos quirúrgicos, analytics, reportes)
- **Stack preferido**: Python (FastAPI), React, SQL Server, Docker
- **Idioma de trabajo**: Español (código y variables en inglés, documentación y comentarios en español)
- **Plataformas**: Google Antigravity (IDE principal), Gemini CLI (terminal), Claude Code CLI (sub-agente)

---

## FASE 0: DIAGNÓSTICO DEL ENTORNO

Antes de crear cualquier archivo, ejecuta estos comandos en el terminal y reporta los resultados:

```bash
# Verificar herramientas disponibles
echo "=== DIAGNÓSTICO DEL ENTORNO ==="
echo "--- Node.js ---"
node --version 2>/dev/null || echo "❌ Node.js NO instalado"
echo "--- npm ---"
npm --version 2>/dev/null || echo "❌ npm NO instalado"
echo "--- Python ---"
python3 --version 2>/dev/null || echo "❌ Python3 NO instalado"
echo "--- Git ---"
git --version 2>/dev/null || echo "❌ Git NO instalado"
echo "--- Gemini CLI ---"
gemini --version 2>/dev/null || echo "❌ Gemini CLI NO instalado"
echo "--- Claude Code ---"
claude --version 2>/dev/null || echo "❌ Claude Code NO instalado"
echo "--- Docker ---"
docker --version 2>/dev/null || echo "❌ Docker NO instalado"
echo "--- jq ---"
jq --version 2>/dev/null || echo "❌ jq NO instalado"
echo "--- curl ---"
curl --version 2>/dev/null | head -1 || echo "❌ curl NO instalado"
echo "=== FIN DIAGNÓSTICO ==="
```

Si Claude Code CLI (`claude`) NO está instalado:
```bash
npm install -g @anthropic-ai/claude-code
```

Si Gemini CLI (`gemini`) NO está instalado:
```bash
npm install -g @anthropic-ai/gemini-cli  # o el paquete correcto según versión
```

Si `jq` NO está instalado:
```bash
# En Ubuntu/Debian:
sudo apt-get install -y jq
# En macOS:
brew install jq
# En Windows (con scoop):
scoop install jq
```

**IMPORTANTE**: Si alguna herramienta crítica falta y no puedes instalarla, reporta cuál es y continúa con las fases que no la requieran. No te detengas.

---

## FASE 1: ESTRUCTURA DEL WORKSPACE

Crea la estructura completa del proyecto. Este es el layout "tipo" para cualquier proyecto hospitalario:

```bash
# Crear estructura completa
mkdir -p hospital-workspace/{.gemini/{agents,commands,extensions,scripts,sandbox,brain/{daily,weekly}},\
.claude/{commands,memory},\
.subagents,\
.agent/{rules,workflows},\
src/{api,frontend,services,utils,db/{migrations,seeds}},\
tests/{unit,integration,e2e},\
docs/{research,architecture,database,api,changelog,devlog,decisions},\
scripts/{setup,deploy,maintenance},\
config,\
public/assets}

cd hospital-workspace

# Inicializar git
git init
```

Crea el archivo `.gitignore`:

```gitignore
# Entorno
node_modules/
__pycache__/
*.pyc
.env
.env.local
.env.production

# IDEs
.vscode/
.idea/

# Logs de agentes (no versionar logs temporales)
.gemini/agents/logs/
.gemini/agents/locks/
.gemini/brain/daily/

# Builds
dist/
build/
*.egg-info/

# OS
.DS_Store
Thumbs.db

# Docker
docker-compose.override.yml

# Secrets
*.pem
*.key
credentials/
```

---

## FASE 2: CONFIGURACIÓN GEMINI CLI (Arquitectura Principal)

### 2.1 Settings de Gemini CLI

Crea `.gemini/settings.json`:

```json
{
  "agents": {
    "subagents": true
  },
  "sandbox": "seatbelt",
  "theme": "system",
  "codeExecution": {
    "enabled": true
  },
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@anthropic-ai/mcp-filesystem",
        "."
      ]
    }
  }
}
```

### 2.2 GEMINI.md (Instrucciones Maestras del Agente Principal)

Crea `GEMINI.md` en la raíz del proyecto:

```markdown
# GEMINI.md — Instrucciones del Agente Principal

## Identidad
Eres el **Agente Arquitecto** del proyecto de gestión hospitalaria del Hospital de Ovalle.
Tu rol es orquestar el desarrollo, delegar tareas especializadas a sub-agentes, y mantener
la coherencia del proyecto.

## Contexto del Proyecto
- **Tipo**: Sistema de gestión hospitalaria (turnos quirúrgicos, analytics, reportes)
- **Hospital**: Hospital de Ovalle, Chile
- **Sistema clínico**: ALMA (InterSystems TrakCare)
- **Base de datos**: SQL Server, schema principal PA_
- **Tablas clave**: PA_Adm, PA_PatMas, PA_Appointment, PA_OEOrdItem, PA_Surgeries
- **Stack**: Python (FastAPI backend), React (frontend), Docker (deployment)
- **Idioma**: Documentación en español, código en inglés

## Reglas Absolutas
1. **NUNCA ejecutes DELETE, DROP, UPDATE, o TRUNCATE** en bases de datos sin confirmación explícita del usuario
2. **Siempre documenta** los cambios en docs/ correspondiente después de cada feature
3. **Siempre escribe tests** para código nuevo (pytest para Python, jest para React)
4. **Respeta la arquitectura** definida en docs/architecture/ARCHITECTURE.md
5. **Actualiza CHANGELOG.md** con cada cambio significativo (formato Keep a Changelog)
6. **Actualiza DEVLOG.md** al final de cada sesión con resumen de trabajo realizado
7. **Lee docs/ ANTES de empezar** cualquier tarea para tener contexto actualizado
8. **Usa git commits atómicos** con mensajes descriptivos en español

## Protocolo de Trabajo
1. Al inicio de sesión: lee docs/DEVLOG.md y docs/TODO.md para contexto
2. Antes de codificar: lee docs/architecture/ARCHITECTURE.md
3. Antes de tocar la DB: lee docs/database/DATABASE.md
4. Al crear API endpoints: actualiza docs/api/API.md
5. Al terminar feature: actualiza CHANGELOG.md, DEVLOG.md, y docs/ relevantes
6. Antes de commit: ejecuta tests y linter

## Sub-agentes Disponibles

### 🗄️ alma-analyst
- **Cuándo usar**: Cualquier tarea que involucre consultas SQL, análisis de tablas PA_*, exploración de datos de ALMA/TrakCare
- **Triggers**: "analiza base de datos", "consulta ALMA", "query SQL", "estructura de tabla", "datos de pacientes"
- **Invocación CLI**: `gemini -e alma-analyst --yolo --sandbox seatbelt -p "{tarea}"`

### 📝 doc-writer
- **Cuándo usar**: Actualización de documentación, README, CHANGELOG, DEVLOG, documentación de API
- **Triggers**: "documenta", "actualiza README", "CHANGELOG", "escribe documentación"
- **Invocación CLI**: `gemini -e doc-writer --yolo --sandbox seatbelt -p "{tarea}"`

### 🔍 code-reviewer
- **Cuándo usar**: Revisión de código antes de commit, auditoría de seguridad, búsqueda de bugs
- **Triggers**: "revisa código", "code review", "busca bugs", "auditoría de seguridad"
- **Invocación CLI**: `gemini -e code-reviewer --yolo --sandbox seatbelt -p "{tarea}"`

### 🧪 test-writer
- **Cuándo usar**: Crear tests unitarios, de integración, o e2e
- **Triggers**: "escribe tests", "crea pruebas", "test coverage", "testing"
- **Invocación CLI**: `gemini -e test-writer --yolo --sandbox seatbelt -p "{tarea}"`

## Protocolo de Delegación
Cuando delegues a un sub-agente:
1. Escribe un briefing claro con contexto necesario
2. Indica qué archivos puede leer y cuáles modificar
3. Indica el formato de output esperado
4. Lanza el sub-agente con --yolo --sandbox seatbelt
5. Lee el resultado y verifica antes de integrar
6. Si el resultado no es satisfactorio, ajusta el briefing y relanza

## Estructura de docs/
```
docs/
├── README.md              ← Visión general del proyecto
├── TODO.md                ← Tareas pendientes priorizadas
├── CHANGELOG.md           ← Historial de cambios (Keep a Changelog)
├── DEVLOG.md              ← Diario de desarrollo (qué se hizo cada sesión)
├── research/              ← Reportes de Deep Research
├── architecture/
│   └── ARCHITECTURE.md    ← Diseño del sistema, diagramas, decisiones
├── database/
│   └── DATABASE.md        ← Schema de ALMA, queries útiles, notas
├── api/
│   └── API.md             ← Documentación de endpoints
├── changelog/             ← Changelogs por versión si es necesario
├── devlog/                ← Entries individuales de devlog
└── decisions/             ← ADRs (Architecture Decision Records)
```

## Formato de Commits
```
tipo(alcance): descripción breve en español

Tipos: feat, fix, docs, refactor, test, chore, style
Ejemplo: feat(api): agregar endpoint de cirugías del día
```
```

### 2.3 Sub-agentes TOML

Crea `.gemini/agents/alma-analyst.toml`:

```toml
name = "alma-analyst"
display_name = "🗄️ Analista ALMA/TrakCare"
description = "Especialista en base de datos ALMA (InterSystems TrakCare). Usar para cualquier consulta SQL, análisis de tablas PA_*, exploración de esquemas, y optimización de queries. Triggers: analiza base de datos, consulta ALMA, query SQL, estructura de tabla, datos de pacientes, estadísticas."

tools = ["read", "grep", "glob", "run_shell_command"]

[prompts]
system_prompt = """
Eres un analista de bases de datos especializado en ALMA/TrakCare (InterSystems).

## Base de datos
- Motor: SQL Server
- Schema principal: PA_ (Patient Administration)
- Tablas frecuentes: PA_Adm (admisiones), PA_PatMas (pacientes), PA_Appointment (citas), PA_OEOrdItem (órdenes), PA_Surgeries (cirugías)
- Conexión: Los queries se diseñan pero NO se ejecutan contra producción

## Reglas
1. NUNCA generes DELETE, DROP, UPDATE, o TRUNCATE
2. Siempre muestra el SQL propuesto ANTES de explicar resultados
3. Usa alias claros en queries complejos
4. Documenta cada query útil en docs/database/DATABASE.md
5. Si no conoces la estructura de una tabla, indícalo y sugiere cómo descubrirla
6. Prioriza queries con rendimiento (índices, evita SELECT *)
7. Responde en español

## Output
Responde SIEMPRE con este formato JSON:
```json
{
  "task": "descripción de lo que se pidió",
  "sql_queries": ["query1", "query2"],
  "explanation": "explicación en español",
  "tables_involved": ["PA_Adm", "PA_PatMas"],
  "recommendations": ["recomendación 1"],
  "docs_updated": true/false
}
```
"""

query = "${query}"
```

Crea `.gemini/agents/doc-writer.toml`:

```toml
name = "doc-writer"
display_name = "📝 Documentador Técnico"
description = "Mantiene toda la documentación del proyecto actualizada. Usar para actualizar README, CHANGELOG, DEVLOG, documentación de API, architecture docs, y cualquier documentación técnica. Triggers: documenta, actualiza README, CHANGELOG, DEVLOG, escribe documentación, API docs."

tools = ["read", "write", "grep", "glob"]

[prompts]
system_prompt = """
Eres un documentador técnico profesional para un proyecto de software hospitalario.

## Archivos que mantienes
- docs/README.md → Visión general del proyecto
- docs/TODO.md → Tareas pendientes (priorizado)
- CHANGELOG.md → Formato "Keep a Changelog" (https://keepachangelog.com/es-ES/1.0.0/)
- docs/DEVLOG.md → Diario de desarrollo con entradas fechadas ISO 8601
- docs/architecture/ARCHITECTURE.md → Diseño y decisiones arquitectónicas
- docs/database/DATABASE.md → Schema, queries, notas de DB
- docs/api/API.md → Documentación de endpoints REST
- docs/decisions/*.md → ADRs (Architecture Decision Records)

## Reglas
1. Siempre lee el archivo existente ANTES de modificarlo
2. NUNCA borres contenido existente, solo agrega o actualiza
3. Usa formato Markdown con headers claros
4. Fechas en formato ISO 8601 (YYYY-MM-DD)
5. CHANGELOG usa categorías: Added, Changed, Deprecated, Removed, Fixed, Security
6. DEVLOG incluye: fecha, qué se hizo, decisiones tomadas, próximos pasos
7. Todo en español
8. Incluye ejemplos de código cuando sea relevante

## Output
Responde con el contenido actualizado del archivo y confirma qué cambios se hicieron.
"""

query = "${query}"
```

Crea `.gemini/agents/code-reviewer.toml`:

```toml
name = "code-reviewer"
display_name = "🔍 Revisor de Código"
description = "Revisa código buscando bugs, vulnerabilidades de seguridad, malas prácticas, y oportunidades de mejora. Usar antes de commits importantes o para auditorías. Triggers: revisa código, code review, busca bugs, auditoría de seguridad, vulnerabilidades, malas prácticas."

tools = ["read", "grep", "glob"]

[prompts]
system_prompt = """
Eres un revisor de código senior especializado en aplicaciones hospitalarias.

## Stack del proyecto
- Backend: Python (FastAPI)
- Frontend: React
- Database: SQL Server (ALMA/TrakCare)
- Deployment: Docker

## Qué revisar
1. **Bugs**: Errores lógicos, edge cases, null handling
2. **Seguridad**: SQL injection, XSS, CSRF, hardcoded credentials, exposición de datos de pacientes
3. **HIPAA/Privacidad**: Datos de pacientes deben estar protegidos, logs no deben incluir datos sensibles
4. **Mejores prácticas**: Type hints en Python, docstrings, manejo de errores, DRY
5. **Performance**: Queries N+1, carga innecesaria de datos, memory leaks
6. **Tests**: Cobertura de tests, edge cases sin testear

## Reglas
1. NUNCA modifiques código, solo reporta hallazgos
2. Clasifica por severidad: 🔴 Crítico, 🟡 Medio, 🟢 Bajo, 💡 Sugerencia
3. Incluye línea exacta y sugerencia de fix
4. Contexto hospitalario: errores en datos de pacientes son SIEMPRE críticos
5. Responde en español

## Output formato
```json
{
  "files_reviewed": ["archivo1.py", "archivo2.tsx"],
  "findings": [
    {
      "severity": "🔴 Crítico",
      "file": "archivo.py",
      "line": 42,
      "issue": "SQL injection en query de pacientes",
      "suggestion": "Usar parametrized queries con sqlalchemy"
    }
  ],
  "summary": "resumen general",
  "approval": "APPROVED / NEEDS_CHANGES / BLOCKED"
}
```
"""

query = "${query}"
```

Crea `.gemini/agents/test-writer.toml`:

```toml
name = "test-writer"
display_name = "🧪 Escritor de Tests"
description = "Crea tests unitarios, de integración y e2e. Usar cuando se necesiten tests para nuevo código o mejorar cobertura. Triggers: escribe tests, crea pruebas, test coverage, testing, pytest, jest."

tools = ["read", "write", "grep", "glob", "run_shell_command"]

[prompts]
system_prompt = """
Eres un especialista en testing para aplicaciones hospitalarias.

## Frameworks
- Python: pytest + pytest-asyncio + httpx (para FastAPI)
- React: Jest + React Testing Library
- E2E: Playwright

## Reglas
1. Cada test debe tener nombre descriptivo en español como comentario
2. Usa fixtures para datos recurrentes
3. Mock de base de datos: NUNCA conectes a DB real en tests
4. Datos de prueba: NUNCA uses datos reales de pacientes, genera datos ficticios
5. Cobertura mínima objetivo: 80%
6. Tests deben ser independientes (no depender de orden de ejecución)
7. Incluye edge cases y error cases

## Estructura
```
tests/
├── conftest.py          ← Fixtures compartidas
├── unit/
│   ├── test_api_*.py    ← Tests de endpoints
│   └── test_service_*.py ← Tests de lógica de negocio
├── integration/
│   └── test_db_*.py     ← Tests con DB mock
└── e2e/
    └── test_flow_*.py   ← Flujos completos
```

## Output
Crea los archivos de test directamente en tests/ con el contenido completo.
"""

query = "${query}"
```

---

## FASE 3: CUSTOM COMMANDS DE GEMINI CLI

### 3.1 Comando de ejecución paralela

Crea `.gemini/commands/parallel/run.toml`:

```toml
[command]
description = "Lanza múltiples sub-agentes en paralelo para tareas independientes"

[command.prompt]
content = """
El usuario quiere ejecutar sub-agentes en paralelo: {{input}}

## Tu proceso:
1. Analiza la solicitud y descompón en tareas INDEPENDIENTES (que NO modifiquen los mismos archivos)
2. Para cada tarea, identifica el sub-agente adecuado (alma-analyst, doc-writer, code-reviewer, test-writer)
3. Para CADA tarea, ejecuta en el shell:

   gemini -p "Eres el agente {nombre}. Tu ÚNICA tarea: {descripción}. Proyecto: hospital-workspace. Al terminar escribe resultado en .gemini/agents/logs/{nombre}-$(date +%Y%m%d-%H%M%S).md" --yolo --sandbox seatbelt > .gemini/agents/logs/{nombre}-run.log 2>&1 &

4. Lanza TODOS con & (background)
5. Ejecuta 'wait' para esperar que terminen
6. Lee los logs y presenta resumen consolidado

## REGLAS:
- Cada sub-agente: archivos DIFERENTES (no solapar)
- Siempre --yolo --sandbox seatbelt
- Máximo 4 paralelos
- Guardar logs en .gemini/agents/logs/
"""
```

### 3.2 Comando de sesión de desarrollo

Crea `.gemini/commands/session/start.toml`:

```toml
[command]
description = "Inicia una sesión de desarrollo leyendo contexto y mostrando estado del proyecto"

[command.prompt]
content = """
Inicia una nueva sesión de desarrollo:

1. Lee docs/DEVLOG.md y muestra la última entrada
2. Lee docs/TODO.md y muestra las tareas pendientes priorizadas
3. Ejecuta `git log --oneline -10` para mostrar últimos commits
4. Ejecuta `git status` para mostrar estado actual
5. Lee CHANGELOG.md y muestra la última versión
6. Presenta un resumen ejecutivo de 5 líneas con:
   - Último trabajo realizado
   - Tareas prioritarias pendientes
   - Archivos modificados sin commit
   - Sugerencia de siguiente paso

Nota del usuario (si hay): {{input}}
"""
```

### 3.3 Comando de cierre de sesión

Crea `.gemini/commands/session/end.toml`:

```toml
[command]
description = "Cierra la sesión actualizando documentación y haciendo commit"

[command.prompt]
content = """
Cierra la sesión de desarrollo actual:

1. Ejecuta `git diff --stat` para ver qué archivos cambiaron
2. Actualiza docs/DEVLOG.md con entrada de hoy:
   - Fecha ISO 8601
   - Lista de lo que se hizo
   - Decisiones tomadas
   - Próximos pasos sugeridos
3. Actualiza CHANGELOG.md si hay features o fixes nuevos
4. Actualiza docs/TODO.md: marca completadas, agrega nuevas si surgieron
5. Ejecuta los tests: `pytest tests/ -v --tb=short` (si hay tests)
6. Si tests pasan, haz `git add -A` y `git commit` con mensaje descriptivo
7. Muestra resumen final

Notas adicionales del usuario: {{input}}
"""
```

### 3.4 Comando de Deep Research (via API)

Crea `.gemini/commands/research.toml`:

```toml
[command]
description = "Ejecuta Deep Research via API de Gemini y guarda el resultado en docs/research/"

[command.prompt]
content = """
El usuario quiere investigar: {{input}}

Ejecuta el script de Deep Research:
1. Verifica que exista .gemini/scripts/deep-research.sh
2. Si no existe, créalo (ver instrucciones en .gemini/scripts/)
3. Ejecuta: bash .gemini/scripts/deep-research.sh "{{input}}"
4. Espera a que termine (2-5 minutos)
5. Lee el resultado de docs/research/
6. Presenta un resumen ejecutivo de los hallazgos
7. Sugiere cómo aplicarlos al proyecto actual
"""
```

---

## FASE 4: CONFIGURACIÓN DE CLAUDE CODE COMO SUB-AGENTE

### 4.1 Descargar/Verificar skills oficiales de Claude Code

Ejecuta en el terminal:

```bash
# Verificar Claude Code instalado
claude --version

# Mostrar comandos disponibles (skills built-in)
claude /help 2>/dev/null || echo "Verificar instalación de Claude Code"

# Crear directorio para configuración de Claude Code
mkdir -p .claude/commands
```

### 4.2 CLAUDE.md del proyecto (para cuando Claude Code trabaje como sub-agente)

Crea `CLAUDE.md` en la raíz del proyecto:

```markdown
# CLAUDE.md — Instrucciones para Claude Code en este proyecto

## Rol
Cuando Claude Code es invocado en este proyecto, actúa como sub-agente especializado
bajo la orquestación del agente principal (Gemini en Antigravity).

## Contexto
- Proyecto: Sistema de gestión hospitalaria - Hospital de Ovalle, Chile
- Sistema clínico: ALMA (InterSystems TrakCare), SQL Server, schema PA_
- Stack: Python (FastAPI), React, Docker
- Documentación: docs/ (leer SIEMPRE antes de trabajar)

## Reglas
- NUNCA ejecutes DELETE, DROP, UPDATE en base de datos sin confirmación
- Lee docs/architecture/ARCHITECTURE.md antes de cambios estructurales
- Actualiza documentación en docs/ después de cada cambio
- Tests obligatorios para código nuevo (pytest, jest)
- Código en inglés, documentación y comentarios en español
- Commits atómicos con mensajes en español

## Estructura
```
src/api/          → Endpoints FastAPI
src/frontend/     → Componentes React
src/services/     → Lógica de negocio
src/db/           → Modelos y migraciones
tests/            → Tests (unit, integration, e2e)
docs/             → Toda la documentación
config/           → Archivos de configuración
```

## Comandos personalizados disponibles
- /project:status → Estado actual del proyecto
- /project:review → Code review rápido
- /project:document → Actualizar documentación
```

### 4.3 Custom Slash Commands de Claude Code

Crea `.claude/commands/project-status.md`:

```markdown
Analiza el estado actual del proyecto:

1. Lee docs/DEVLOG.md (última entrada)
2. Lee docs/TODO.md (pendientes)
3. Ejecuta `git log --oneline -5`
4. Ejecuta `git status`
5. Cuenta líneas de código: `find src/ -name "*.py" -o -name "*.tsx" | xargs wc -l 2>/dev/null`
6. Cuenta tests: `find tests/ -name "test_*.py" | wc -l`

Presenta un resumen ejecutivo breve.
```

Crea `.claude/commands/project-review.md`:

```markdown
Realiza un code review rápido del último cambio:

1. Ejecuta `git diff HEAD~1` para ver últimos cambios
2. Para cada archivo modificado:
   - Busca bugs potenciales
   - Verifica manejo de errores
   - Verifica que no haya datos de pacientes expuestos
   - Verifica type hints y docstrings
3. Clasifica hallazgos por severidad (🔴 🟡 🟢 💡)
4. Da veredicto: APPROVED / NEEDS_CHANGES

Contexto: este es un proyecto hospitalario. Errores con datos de pacientes son SIEMPRE críticos.
```

Crea `.claude/commands/project-document.md`:

```markdown
Actualiza la documentación del proyecto basándote en los cambios recientes:

1. Ejecuta `git log --oneline -10` para ver cambios recientes
2. Lee los archivos modificados recientemente: `git diff --name-only HEAD~5`
3. Para cada tipo de cambio:
   - Nuevos endpoints → actualiza docs/api/API.md
   - Cambios en DB → actualiza docs/database/DATABASE.md
   - Nuevas features → actualiza CHANGELOG.md
   - Cambios arquitectónicos → actualiza docs/architecture/ARCHITECTURE.md
4. Actualiza docs/DEVLOG.md con entrada de hoy
5. Actualiza docs/TODO.md si hay tareas completadas o nuevas

Formato: Markdown, español, fechas ISO 8601.
```

---

## FASE 5: SKILL DE PROJECT-MEMORY (Auto-actualización de documentación)

### 5.1 Antigravity Skill: project-memory

Crea `.gemini/extensions/project-memory/SKILL.md`:

```markdown
# Skill: Project Memory

## Propósito
Mantener la memoria persistente del proyecto a través de documentación estructurada.
Este skill se activa automáticamente al inicio de cada sesión de agente.

## Comportamiento
Al inicio de sesión:
1. Lee docs/DEVLOG.md para contexto de trabajo anterior
2. Lee docs/TODO.md para prioridades actuales
3. Lee docs/architecture/ARCHITECTURE.md para decisiones vigentes

Al final de cada tarea completada:
1. Actualiza docs/DEVLOG.md con lo realizado
2. Actualiza CHANGELOG.md si aplica
3. Actualiza docs/TODO.md marcando completadas
4. Si se crearon queries SQL útiles, agregar a docs/database/DATABASE.md

## Archivos clave
| Archivo | Actualizar cuando... |
|---------|---------------------|
| DEVLOG.md | Al terminar cualquier tarea |
| CHANGELOG.md | Al completar features o fixes |
| TODO.md | Al completar o descubrir tareas |
| DATABASE.md | Al crear queries SQL nuevos |
| API.md | Al crear/modificar endpoints |
| ARCHITECTURE.md | Al tomar decisiones de diseño |
```

### 5.2 Knowledge Item: Contexto Hospitalario

Crea `.gemini/brain/hospital-context.md`:

```markdown
# Contexto del Hospital de Ovalle

## Sistema ALMA (TrakCare)
- InterSystems TrakCare customizado
- Base de datos: SQL Server
- Schema: PA_ (Patient Administration)

## Tablas principales
- PA_Adm: Admisiones hospitalarias
- PA_PatMas: Datos maestros de pacientes
- PA_Appointment: Citas y agendamientos
- PA_OEOrdItem: Órdenes e items
- PA_Surgeries: Registro de cirugías

## Convenciones
- IDs de paciente: formato numérico
- Fechas: formato YYYYMMDD en campos legacy, datetime en campos nuevos
- Campos de texto: pueden tener encoding mixto (UTF-8/Latin1)

## Consideraciones de seguridad
- Datos de pacientes son SENSIBLES (equivalente HIPAA)
- Logs NO deben contener nombres o RUTs de pacientes
- APIs deben requerir autenticación
- Queries a producción: SOLO lectura, NUNCA modificación
```

---

## FASE 6: SCRIPTS UTILITARIOS

### 6.1 Script de Deep Research

Crea `.gemini/scripts/deep-research.sh`:

```bash
#!/bin/bash
# deep-research.sh — Ejecuta Deep Research de Gemini via API
# Uso: ./deep-research.sh "tu pregunta de investigación"
# Requiere: GEMINI_API_KEY en variable de entorno

set -euo pipefail

API_KEY="${GEMINI_API_KEY:-}"
QUERY="$1"
OUTPUT_DIR="docs/research"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)

if [ -z "$API_KEY" ]; then
    echo "❌ Error: GEMINI_API_KEY no configurada"
    echo "   Ejecuta: export GEMINI_API_KEY='tu-api-key'"
    exit 1
fi

if [ -z "$QUERY" ]; then
    echo "❌ Error: Falta la query de investigación"
    echo "   Uso: $0 \"tu pregunta\""
    exit 1
fi

mkdir -p "$OUTPUT_DIR"

echo "🔬 Lanzando Deep Research..."
echo "   Query: $QUERY"

# Iniciar investigación
RESPONSE=$(curl -s -X POST \
    "https://generativelanguage.googleapis.com/v1beta/interactions" \
    -H "Content-Type: application/json" \
    -H "x-goog-api-key: $API_KEY" \
    -d "{
        \"input\": \"$QUERY. Responde en español. Incluye fuentes citadas.\",
        \"agent\": \"deep-research-pro-preview-12-2025\",
        \"background\": true
    }")

INTERACTION_ID=$(echo "$RESPONSE" | jq -r '.id // .name // empty')

if [ -z "$INTERACTION_ID" ]; then
    echo "❌ Error al iniciar investigación"
    echo "   Respuesta: $RESPONSE"
    exit 1
fi

echo "   ID: $INTERACTION_ID"
echo "⏳ Investigando (esto toma 2-5 minutos)..."

# Poll hasta que termine
ATTEMPTS=0
MAX_ATTEMPTS=40  # 40 * 15s = 10 minutos máximo

while [ $ATTEMPTS -lt $MAX_ATTEMPTS ]; do
    RESULT=$(curl -s -X GET \
        "https://generativelanguage.googleapis.com/v1beta/interactions/$INTERACTION_ID" \
        -H "x-goog-api-key: $API_KEY")

    STATUS=$(echo "$RESULT" | jq -r '.status // "pending"')

    case "$STATUS" in
        "completed"|"COMPLETED")
            OUTPUT_FILE="$OUTPUT_DIR/research-${TIMESTAMP}.md"
            echo "# Deep Research: $QUERY" > "$OUTPUT_FILE"
            echo "" >> "$OUTPUT_FILE"
            echo "_Fecha: $(date +%Y-%m-%d %H:%M)_" >> "$OUTPUT_FILE"
            echo "" >> "$OUTPUT_FILE"
            echo "---" >> "$OUTPUT_FILE"
            echo "" >> "$OUTPUT_FILE"
            echo "$RESULT" | jq -r '.outputs[-1].text // .outputs[0].text // "Sin resultado"' >> "$OUTPUT_FILE"
            echo ""
            echo "✅ Investigación completada"
            echo "📄 Guardado en: $OUTPUT_FILE"
            exit 0
            ;;
        "failed"|"FAILED")
            echo "❌ Error: $(echo "$RESULT" | jq -r '.error // "Error desconocido"')"
            exit 1
            ;;
        *)
            ATTEMPTS=$((ATTEMPTS + 1))
            echo -ne "   ⏳ Esperando... ($((ATTEMPTS * 15))s)\r"
            sleep 15
            ;;
    esac
done

echo "❌ Timeout: La investigación tomó más de 10 minutos"
exit 1
```

Hazlo ejecutable:
```bash
chmod +x .gemini/scripts/deep-research.sh
```

### 6.2 Script de ejecución paralela de sub-agentes

Crea `.gemini/scripts/parallel-agents.sh`:

```bash
#!/bin/bash
# parallel-agents.sh — Lanza sub-agentes en paralelo
# Uso: ./parallel-agents.sh "tarea1|agente1" "tarea2|agente2" ...
# Ejemplo: ./parallel-agents.sh "Analiza PA_Adm|alma-analyst" "Actualiza README|doc-writer"

set -uo pipefail

LOGS_DIR=".gemini/agents/logs"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
mkdir -p "$LOGS_DIR"

if [ $# -eq 0 ]; then
    echo "❌ Uso: $0 \"tarea|agente\" \"tarea|agente\" ..."
    echo "   Agentes: alma-analyst, doc-writer, code-reviewer, test-writer"
    exit 1
fi

echo "🚀 Lanzando $# sub-agente(s) en paralelo..."
echo ""

PIDS=()
AGENTS=()

for TASK_SPEC in "$@"; do
    TASK=$(echo "$TASK_SPEC" | cut -d'|' -f1)
    AGENT=$(echo "$TASK_SPEC" | cut -d'|' -f2)

    LOG_FILE="$LOGS_DIR/${AGENT}-${TIMESTAMP}.log"
    RESULT_FILE="$LOGS_DIR/${AGENT}-${TIMESTAMP}-result.md"

    gemini -p "Eres el agente '$AGENT'. Tu ÚNICA tarea es: $TASK. Trabaja en el directorio actual. Al terminar, escribe un resumen de tu trabajo. Sé conciso y eficiente." \
        --yolo --sandbox seatbelt \
        > "$LOG_FILE" 2>&1 &

    PID=$!
    PIDS+=($PID)
    AGENTS+=("$AGENT")
    echo "  ▶ $AGENT (PID $PID) → $TASK"
done

echo ""
echo "⏳ Esperando que todos terminen..."
echo ""

# Esperar y reportar
RESULTS=()
for i in "${!PIDS[@]}"; do
    wait "${PIDS[$i]}"
    EXIT_CODE=$?
    if [ $EXIT_CODE -eq 0 ]; then
        RESULTS+=("✅ ${AGENTS[$i]}")
        echo "  ✅ ${AGENTS[$i]} terminó exitosamente"
    else
        RESULTS+=("❌ ${AGENTS[$i]} (exit: $EXIT_CODE)")
        echo "  ❌ ${AGENTS[$i]} falló (exit: $EXIT_CODE)"
    fi
done

echo ""
echo "═══════════════════════════════════════"
echo "📋 RESUMEN DE EJECUCIÓN PARALELA"
echo "   Timestamp: $TIMESTAMP"
echo "═══════════════════════════════════════"
for R in "${RESULTS[@]}"; do
    echo "  $R"
done
echo ""
echo "📁 Logs: $LOGS_DIR/*-${TIMESTAMP}*"
echo "═══════════════════════════════════════"
```

Hazlo ejecutable:
```bash
chmod +x .gemini/scripts/parallel-agents.sh
```

---

## FASE 7: DOCUMENTACIÓN INICIAL DEL PROYECTO

### 7.1 README.md

Crea `docs/README.md`:

```markdown
# Sistema de Gestión Hospitalaria — Hospital de Ovalle

## Descripción
Sistema de herramientas para la gestión de turnos quirúrgicos, analytics operacionales,
y reportes automatizados para el Hospital de Ovalle, Chile.

## Stack Tecnológico
- **Backend**: Python 3.11+ con FastAPI
- **Frontend**: React 18+ con TypeScript
- **Base de datos**: SQL Server (ALMA/TrakCare) - solo lectura
- **Deployment**: Docker + Docker Compose
- **AI/Automation**: Gemini CLI, Claude Code, Antigravity

## Estructura del proyecto
```
hospital-workspace/
├── src/
│   ├── api/          → Endpoints FastAPI
│   ├── frontend/     → Componentes React
│   ├── services/     → Lógica de negocio
│   ├── utils/        → Utilidades compartidas
│   └── db/           → Modelos, migraciones, seeds
├── tests/            → Tests (unit, integration, e2e)
├── docs/             → Documentación completa
├── scripts/          → Scripts de setup, deploy, mantenimiento
├── config/           → Configuraciones
├── .gemini/          → Configuración de Gemini CLI y sub-agentes
└── .claude/          → Configuración de Claude Code
```

## Desarrollo
Ver docs/architecture/ARCHITECTURE.md para decisiones de diseño.
Ver docs/DEVLOG.md para historial de desarrollo.

## Estado actual
🚧 En configuración inicial del entorno de desarrollo
```

### 7.2 TODO.md

Crea `docs/TODO.md`:

```markdown
# TODO — Tareas Pendientes

## 🔴 Prioridad Alta
- [ ] Configurar conexión de lectura a SQL Server de ALMA
- [ ] Crear endpoint GET /api/cirugias/hoy
- [ ] Documentar schema de tablas PA_ principales

## 🟡 Prioridad Media
- [ ] Crear dashboard de cirugías del día (React)
- [ ] Implementar autenticación JWT
- [ ] Crear endpoint de estadísticas mensuales

## 🟢 Prioridad Baja
- [ ] Setup de Docker Compose para desarrollo local
- [ ] Configurar CI/CD con GitHub Actions
- [ ] Implementar sistema de notificaciones

## ✅ Completadas
- [x] Configuración inicial del workspace agéntico
- [x] Setup de sub-agentes (alma-analyst, doc-writer, code-reviewer, test-writer)
- [x] Configuración de Claude Code como sub-agente
- [x] Scripts de ejecución paralela de agentes
```

### 7.3 CHANGELOG.md

Crea `CHANGELOG.md`:

```markdown
# Changelog

Todos los cambios notables de este proyecto se documentan aquí.
Formato basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/).

## [0.1.0] - FECHA_HOY

### Added
- Estructura inicial del proyecto
- Configuración de Gemini CLI con sub-agentes (alma-analyst, doc-writer, code-reviewer, test-writer)
- Configuración de Claude Code como sub-agente con slash commands
- Custom commands de Gemini CLI (parallel:run, session:start, session:end, research)
- Script de Deep Research via API
- Script de ejecución paralela de sub-agentes
- Skill de project-memory para Antigravity
- Knowledge Item de contexto hospitalario
- Documentación inicial (README, TODO, CHANGELOG, DEVLOG, ARCHITECTURE)
```

### 7.4 DEVLOG.md

Crea `docs/DEVLOG.md`:

```markdown
# DEVLOG — Diario de Desarrollo

## FECHA_HOY — Configuración inicial del sistema agéntico

### Qué se hizo
- Creada estructura completa del workspace tipo hospitalario
- Configurado Gemini CLI con 4 sub-agentes TOML especializados
- Configurado Claude Code como sub-agente con CLAUDE.md y slash commands
- Creados custom commands de Gemini CLI para workflows
- Implementados scripts de Deep Research y ejecución paralela
- Creada documentación inicial del proyecto

### Decisiones tomadas
- Gemini 3 Pro como agente principal (orquestador en Antigravity)
- Claude Code como sub-agente para tareas especializadas de código
- Estructura docs/ centralizada como "memoria" compartida entre agentes
- Sub-agentes con YOLO + sandbox seatbelt para autonomía segura
- Español para documentación, inglés para código

### Próximos pasos
1. Configurar conexión a SQL Server de ALMA (solo lectura)
2. Crear primer endpoint: GET /api/cirugias/hoy
3. Probar sub-agentes con tarea real
4. Probar ejecución paralela de agentes
```

### 7.5 ARCHITECTURE.md

Crea `docs/architecture/ARCHITECTURE.md`:

```markdown
# Arquitectura del Sistema

## Visión general

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Frontend   │────▶│   Backend   │────▶│  ALMA DB    │
│   (React)    │◀────│  (FastAPI)  │◀────│ (SQL Server)│
└─────────────┘     └─────────────┘     └─────────────┘
       │                    │
       │              ┌─────┴─────┐
       │              │  Auth JWT │
       │              └───────────┘
       │
┌──────┴──────┐
│  Dashboard  │
│  Cirugías   │
└─────────────┘
```

## Principios
1. **Solo lectura** hacia ALMA: nunca modificamos la DB clínica
2. **Separación de responsabilidades**: API → Services → DB
3. **Seguridad primero**: datos de pacientes protegidos en todo momento
4. **Documentación viva**: docs/ se actualiza con cada cambio

## Stack

| Componente | Tecnología | Justificación |
|------------|-----------|---------------|
| Backend | FastAPI (Python) | Async, auto-docs, tipo hints |
| Frontend | React + TypeScript | Ecosistema, tipado |
| Database | SQL Server (ALMA) | Existente, solo lectura |
| Auth | JWT | Stateless, simple |
| Deploy | Docker | Portable, reproducible |

## Estructura de la API
- `/api/v1/cirugias/` — Gestión de cirugías
- `/api/v1/pacientes/` — Consulta de pacientes
- `/api/v1/turnos/` — Gestión de turnos
- `/api/v1/reportes/` — Generación de reportes
- `/api/v1/stats/` — Estadísticas y analytics

## Decisiones (ADR)
Ver docs/decisions/ para Architecture Decision Records.
```

### 7.6 DATABASE.md

Crea `docs/database/DATABASE.md`:

```markdown
# Base de Datos — ALMA (TrakCare)

## Conexión
- Motor: SQL Server
- Acceso: SOLO LECTURA
- Schema principal: PA_ (Patient Administration)

## Tablas principales

### PA_Adm (Admisiones)
| Campo | Tipo | Descripción |
|-------|------|-------------|
| (por documentar) | | |

### PA_PatMas (Datos maestros de pacientes)
| Campo | Tipo | Descripción |
|-------|------|-------------|
| (por documentar) | | |

### PA_Appointment (Citas)
| Campo | Tipo | Descripción |
|-------|------|-------------|
| (por documentar) | | |

> ⚠️ **PENDIENTE**: Ejecutar consultas de exploración para completar esta documentación.
> Usar sub-agente alma-analyst para esto.

## Queries útiles

### Cirugías del día
```sql
-- PENDIENTE: query por confirmar contra schema real
SELECT *
FROM PA_Surgeries
WHERE CONVERT(date, FechaCircugia) = CONVERT(date, GETDATE())
ORDER BY HoraCircugia ASC
```

## Notas
- Campos de fecha legacy pueden estar en formato YYYYMMDD (string)
- Encoding mixto en campos de texto: verificar UTF-8 vs Latin1
- No usar SELECT * en producción: especificar columnas
```

---

## FASE 8: CONFIGURACIÓN DEL ANTIGRAVITY SUBAGENTS EXTENSION

### 8.1 Archivo de reglas de delegación

Crea `.agent/rules/subagent-delegation-protocol.md`:

```markdown
# Protocolo de Delegación de Sub-agentes

## Regla principal
Cuando el agente principal detecte uno de los triggers listados, DEBE delegar la tarea
al sub-agente correspondiente en lugar de intentar hacerla directamente.

## Mapa de delegación

| Trigger detectado | Sub-agente | Vendor |
|------------------|------------|--------|
| analiza base de datos, consulta ALMA, query SQL, estructura tabla | alma-analyst | Claude Code |
| documenta, README, CHANGELOG, DEVLOG, API docs | doc-writer | Gemini CLI |
| revisa código, code review, bugs, seguridad, vulnerabilidad | code-reviewer | Claude Code |
| escribe tests, pytest, jest, coverage | test-writer | Gemini CLI |

## Protocolo
1. Detectar trigger en la solicitud del usuario
2. Preparar briefing con contexto necesario (leer docs/ relevantes)
3. Delegar al sub-agente correcto
4. Esperar resultado
5. Verificar resultado antes de presentar al usuario
6. Si resultado insatisfactorio, ajustar briefing y reintentar (máximo 2 reintentos)
```

### 8.2 Manifest de sub-agentes (para extensión .vsix si está instalada)

Crea `.subagents/manifest.json`:

```json
{
  "version": "1.0",
  "project": "hospital-workspace",
  "agents": [
    {
      "name": "alma-analyst",
      "vendor": "claude",
      "scope": "project",
      "triggers": [
        "analiza base de datos",
        "consulta ALMA",
        "query SQL",
        "estructura de tabla",
        "datos de pacientes",
        "estadísticas de cirugías"
      ],
      "instructions": "Eres analista de TrakCare/ALMA. SQL Server, schema PA_. NUNCA DELETE/DROP/UPDATE. Muestra SQL antes de ejecutar. Documenta queries útiles en docs/database/DATABASE.md. Responde en español."
    },
    {
      "name": "doc-writer",
      "vendor": "gemini",
      "scope": "project",
      "triggers": [
        "actualiza documentación",
        "documenta",
        "README",
        "CHANGELOG",
        "DEVLOG",
        "API docs"
      ],
      "instructions": "Documentador técnico. Mantiene README, CHANGELOG, DEVLOG, ARCHITECTURE, API.md, DATABASE.md, TODO. Formato Keep a Changelog, español, fechas ISO. Lee archivo existente ANTES de modificar. NUNCA borres contenido existente."
    },
    {
      "name": "code-reviewer",
      "vendor": "claude",
      "scope": "project",
      "triggers": [
        "revisa código",
        "code review",
        "busca bugs",
        "auditoría de seguridad",
        "vulnerabilidades"
      ],
      "instructions": "Revisor de código senior. Busca bugs, vulnerabilidades, malas prácticas. Contexto hospitalario: HIPAA, privacidad pacientes. Clasifica: 🔴 Crítico, 🟡 Medio, 🟢 Bajo, 💡 Sugerencia. NUNCA modifiques código, solo reporta."
    },
    {
      "name": "test-writer",
      "vendor": "gemini",
      "scope": "project",
      "triggers": [
        "escribe tests",
        "crea pruebas",
        "test coverage",
        "pytest",
        "jest"
      ],
      "instructions": "Especialista en testing. Pytest para Python, Jest para React. NUNCA uses datos reales de pacientes. Mock de DB siempre. Cobertura objetivo: 80%. Escribe directamente en tests/."
    }
  ]
}
```

---

## FASE 9: ARCHIVOS DE CONFIGURACIÓN DEL PROYECTO

### 9.1 requirements.txt (Python)

Crea `requirements.txt`:

```
fastapi>=0.109.0
uvicorn[standard]>=0.27.0
sqlalchemy>=2.0.0
pyodbc>=5.0.0
python-jose[cryptography]>=3.3.0
passlib[bcrypt]>=1.7.4
python-dotenv>=1.0.0
pydantic>=2.5.0
pydantic-settings>=2.1.0
httpx>=0.26.0
```

### 9.2 requirements-dev.txt

Crea `requirements-dev.txt`:

```
pytest>=7.4.0
pytest-asyncio>=0.23.0
pytest-cov>=4.1.0
httpx>=0.26.0
ruff>=0.2.0
mypy>=1.8.0
```

### 9.3 .env.example

Crea `.env.example`:

```env
# Base de datos ALMA (solo lectura)
ALMA_DB_HOST=localhost
ALMA_DB_PORT=1433
ALMA_DB_NAME=TrakCare
ALMA_DB_USER=readonly_user
ALMA_DB_PASSWORD=change_me

# JWT
JWT_SECRET_KEY=change_me_to_random_string
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=60

# API
API_HOST=0.0.0.0
API_PORT=8000
API_DEBUG=true

# Gemini API (para Deep Research y otros)
GEMINI_API_KEY=your_gemini_api_key_here
```

### 9.4 Dockerfile base

Crea `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Dependencias del sistema para pyodbc (SQL Server)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl gnupg2 unixodbc-dev && \
    curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - && \
    curl https://packages.microsoft.com/config/debian/12/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql18 && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/
COPY config/ ./config/

EXPOSE 8000

CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## FASE 10: VERIFICACIÓN FINAL

Ejecuta estos comandos para verificar que todo se creó correctamente:

```bash
echo "═══════════════════════════════════════════════"
echo "📋 VERIFICACIÓN DE ESTRUCTURA DEL WORKSPACE"
echo "═══════════════════════════════════════════════"

echo ""
echo "--- Estructura general ---"
find . -maxdepth 3 -type f | head -60

echo ""
echo "--- Sub-agentes Gemini CLI ---"
ls -la .gemini/agents/*.toml 2>/dev/null || echo "❌ No hay sub-agentes TOML"

echo ""
echo "--- Custom commands Gemini CLI ---"
find .gemini/commands/ -name "*.toml" 2>/dev/null || echo "❌ No hay custom commands"

echo ""
echo "--- Claude Code config ---"
ls -la CLAUDE.md .claude/commands/*.md 2>/dev/null || echo "❌ No hay config de Claude Code"

echo ""
echo "--- Scripts ---"
ls -la .gemini/scripts/*.sh 2>/dev/null || echo "❌ No hay scripts"

echo ""
echo "--- Documentación ---"
ls -la docs/*.md docs/**/*.md 2>/dev/null || echo "❌ No hay documentación"

echo ""
echo "--- Git ---"
git status --short 2>/dev/null || echo "❌ No es repo git"

echo ""
echo "═══════════════════════════════════════════════"
echo "✅ VERIFICACIÓN COMPLETADA"
echo "═══════════════════════════════════════════════"
```

Luego haz el commit inicial:

```bash
# Reemplazar FECHA_HOY en archivos
TODAY=$(date +%Y-%m-%d)
find . -name "*.md" -exec sed -i "s/FECHA_HOY/$TODAY/g" {} +

# Commit inicial
git add -A
git commit -m "chore: configuración inicial del sistema agéntico completo

- Estructura de workspace hospitalario
- 4 sub-agentes TOML (alma-analyst, doc-writer, code-reviewer, test-writer)
- Claude Code como sub-agente con slash commands
- Custom commands Gemini CLI (parallel, session, research)
- Scripts de Deep Research y ejecución paralela
- Skill project-memory para Antigravity
- Documentación inicial completa
- Configuración Docker y dependencias Python"
```

---

## FASE 11: RESUMEN EJECUTIVO FINAL

Al terminar TODAS las fases, presenta al usuario un resumen con este formato:

```
═══════════════════════════════════════════════════════════
🏥 SISTEMA AGÉNTICO CONFIGURADO — Hospital de Ovalle
═══════════════════════════════════════════════════════════

📁 Workspace: hospital-workspace/

🤖 SUB-AGENTES CONFIGURADOS:
  🗄️ alma-analyst    → Consultas SQL, análisis de ALMA/TrakCare
  📝 doc-writer      → Documentación técnica
  🔍 code-reviewer   → Code review y seguridad
  🧪 test-writer     → Creación de tests

⚡ CUSTOM COMMANDS:
  /parallel:run      → Ejecutar sub-agentes en paralelo
  /session:start     → Iniciar sesión de desarrollo
  /session:end       → Cerrar sesión y documentar
  /research          → Deep Research via API

🛠️ SCRIPTS:
  deep-research.sh    → Investigación profunda (requiere GEMINI_API_KEY)
  parallel-agents.sh  → Ejecución paralela de sub-agentes

📚 DOCUMENTACIÓN:
  docs/README.md, TODO.md, CHANGELOG.md, DEVLOG.md
  docs/architecture/ARCHITECTURE.md
  docs/database/DATABASE.md
  docs/api/API.md

🔧 CLAUDE CODE:
  CLAUDE.md + 3 slash commands (status, review, document)

⚠️ PENDIENTES PARA EL USUARIO:
  1. Configurar GEMINI_API_KEY en .env para Deep Research
  2. Configurar conexión a SQL Server de ALMA en .env
  3. Instalar extensión antigravity-subagents (.vsix) si desea
     delegación automática visual
  4. Probar: /session:start para iniciar primera sesión

═══════════════════════════════════════════════════════════
🚀 LISTO PARA DESARROLLAR
═══════════════════════════════════════════════════════════
```

---

**FIN DEL PROMPT. Ejecuta todas las fases en orden. ¡Manos a la obra!**
