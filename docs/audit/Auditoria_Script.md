# PROMPT DE AUDITORÍA: Validación del Sistema Agéntico Multi-Vendor

> **INSTRUCCIÓN**: Ejecuta una auditoría completa del sistema agéntico configurado en este
> workspace. Verifica CADA punto de las 8 categorías siguientes. Para cada verificación,
> reporta ✅ (OK), ⚠️ (parcial/advertencia), o ❌ (falla). Al final genera un reporte
> consolidado con puntuación y acciones correctivas para cada falla encontrada.
> NO corrijas nada automáticamente — solo diagnostica y reporta.

---

## CATEGORÍA 1: ESTRUCTURA DE ARCHIVOS (Esqueleto del proyecto)

Verifica que TODOS estos archivos y directorios existan. Para cada uno, confirma existencia
y que NO esté vacío (tamaño > 0 bytes):

```bash
echo "══════════════════════════════════════════════"
echo "📁 CATEGORÍA 1: ESTRUCTURA DE ARCHIVOS"
echo "══════════════════════════════════════════════"

SCORE=0
TOTAL=0

check_file() {
    TOTAL=$((TOTAL + 1))
    if [ -f "$1" ]; then
        SIZE=$(wc -c < "$1")
        if [ "$SIZE" -gt 10 ]; then
            echo "  ✅ $1 ($SIZE bytes)"
            SCORE=$((SCORE + 1))
        else
            echo "  ⚠️ $1 (existe pero VACÍO o mínimo: $SIZE bytes)"
        fi
    else
        echo "  ❌ $1 NO EXISTE"
    fi
}

check_dir() {
    TOTAL=$((TOTAL + 1))
    if [ -d "$1" ]; then
        COUNT=$(ls -1 "$1" 2>/dev/null | wc -l)
        echo "  ✅ $1/ ($COUNT items)"
        SCORE=$((SCORE + 1))
    else
        echo "  ❌ $1/ NO EXISTE"
    fi
}

echo ""
echo "--- Raíz del proyecto ---"
check_file "GEMINI.md"
check_file "CLAUDE.md"
check_file "CHANGELOG.md"
check_file ".gitignore"

echo ""
echo "--- Gemini CLI ---"
check_file ".gemini/settings.json"
check_dir  ".gemini/agents"
check_dir  ".gemini/skills"
check_dir  ".gemini/scripts"
check_dir  ".gemini/rules"
check_dir  ".gemini/brain"

check_file ".gemini/agents/doc-writer.toml"
check_file ".gemini/agents/code-reviewer.toml"
check_file ".gemini/agents/test-writer.toml"
check_file ".gemini/agents/code-analyst.toml"
check_file ".gemini/agents/db-analyst.toml"
check_file ".gemini/agents/deployer.toml"

echo ""
echo "--- Codex CLI ---"
check_file ".codex/config.yaml"
check_dir  ".codex/agents"
check_dir  ".codex/skills"

check_file ".codex/agents/doc-writer.md"
check_file ".codex/agents/code-reviewer.md"
check_file ".codex/agents/test-writer.md"
check_file ".codex/agents/code-analyst.md"
check_file ".codex/agents/db-analyst.md"
check_file ".codex/agents/deployer.md"
check_file ".codex/agents/researcher.md"

echo ""
echo "--- Claude Code ---"
check_dir  ".claude/commands"
check_file ".claude/commands/project-status.md"
check_file ".claude/commands/project-review.md"
check_file ".claude/commands/project-document.md"

echo ""
echo "--- Sub-agentes Multi-vendor ---"
check_file ".subagents/manifest.json"
check_file ".subagents/dispatch.sh"
check_file ".gemini/rules/delegation-protocol.md"

echo ""
echo "--- Skills y Knowledge ---"
check_file ".gemini/skills/project-memory.md"
check_file ".gemini/skills/deep-research.md"

echo ""
echo "--- Biblioteca Central (si existe global-profile) ---"
if [ -d "_global-profile" ]; then
    check_dir  "_global-profile/.antigravity/library"
    check_file "_global-profile/.antigravity/library/catalog.json"
    check_dir  "_global-profile/.antigravity/library/agents"
    check_dir  "_global-profile/.antigravity/library/skills"
    check_dir  "_global-profile/.antigravity/library/scripts"
fi

echo ""
echo "--- Documentación ---"
check_file "docs/README.md"
check_file "docs/TODO.md"
check_file "docs/DEVLOG.md"
check_dir  "docs/research"

echo ""
echo "--- Directorios de código ---"
check_dir "src"
check_dir "tests"

echo ""
echo "📊 Resultado: $SCORE/$TOTAL archivos/directorios verificados"
echo "══════════════════════════════════════════════"
```

---

## CATEGORÍA 2: INTEGRIDAD DE CONTENIDO (¿Los archivos tienen lo correcto?)

Para cada archivo crítico, verifica que contenga las secciones o claves esperadas:

```bash
echo "══════════════════════════════════════════════"
echo "📝 CATEGORÍA 2: INTEGRIDAD DE CONTENIDO"
echo "══════════════════════════════════════════════"

SCORE=0
TOTAL=0

check_content() {
    # $1 = archivo, $2 = texto a buscar, $3 = descripción
    TOTAL=$((TOTAL + 1))
    if [ -f "$1" ]; then
        if grep -q "$2" "$1" 2>/dev/null; then
            echo "  ✅ $1 contiene: $3"
            SCORE=$((SCORE + 1))
        else
            echo "  ❌ $1 NO contiene: $3"
        fi
    else
        echo "  ❌ $1 no existe (no se puede verificar: $3)"
    fi
}

echo ""
echo "--- GEMINI.md (instrucciones maestras) ---"
check_content "GEMINI.md" "doc-writer" "sub-agente doc-writer documentado"
check_content "GEMINI.md" "code-reviewer" "sub-agente code-reviewer documentado"
check_content "GEMINI.md" "test-writer" "sub-agente test-writer documentado"
check_content "GEMINI.md" "DEVLOG" "protocolo de documentación"

echo ""
echo "--- CLAUDE.md ---"
check_content "CLAUDE.md" "sub-agente\|subagent" "rol como sub-agente definido"

echo ""
echo "--- .gemini/settings.json ---"
check_content ".gemini/settings.json" "subagents\|agents" "sub-agentes habilitados"

echo ""
echo "--- .codex/config.yaml ---"
check_content ".codex/config.yaml" "effort\|model" "configuración de effort levels"

echo ""
echo "--- Sub-agentes Gemini TOML (estructura válida) ---"
for AGENT_FILE in .gemini/agents/*.toml; do
    if [ -f "$AGENT_FILE" ]; then
        AGENT_NAME=$(basename "$AGENT_FILE" .toml)
        check_content "$AGENT_FILE" "name" "$AGENT_NAME tiene campo name"
        check_content "$AGENT_FILE" "description" "$AGENT_NAME tiene description"
        check_content "$AGENT_FILE" "system_prompt" "$AGENT_NAME tiene system_prompt"
    fi
done

echo ""
echo "--- Sub-agentes Codex MD (estructura válida) ---"
for AGENT_FILE in .codex/agents/*.md; do
    if [ -f "$AGENT_FILE" ]; then
        AGENT_NAME=$(basename "$AGENT_FILE" .md)
        check_content "$AGENT_FILE" "Role\|Purpose\|##" "$AGENT_NAME tiene estructura markdown"
    fi
done

echo ""
echo "--- Manifest de sub-agentes (multi-vendor) ---"
check_content ".subagents/manifest.json" "doc-writer" "doc-writer registrado"
check_content ".subagents/manifest.json" "code-reviewer" "code-reviewer registrado"
check_content ".subagents/manifest.json" "test-writer" "test-writer registrado"
check_content ".subagents/manifest.json" "researcher" "researcher registrado"
check_content ".subagents/manifest.json" "vendor" "vendor definido"
check_content ".subagents/manifest.json" "supported_vendors" "multi-vendor configurado"
check_content ".subagents/manifest.json" "codex" "Codex como vendor"
check_content ".subagents/manifest.json" "gemini" "Gemini como vendor"
check_content ".subagents/manifest.json" "claude" "Claude como vendor"

echo ""
echo "--- Documentación (no tiene placeholders sin reemplazar) ---"
for DOC_FILE in docs/*.md CHANGELOG.md; do
    if [ -f "$DOC_FILE" ]; then
        TOTAL=$((TOTAL + 1))
        if grep -q "FECHA_HOY\|TODO_REPLACE\|PLACEHOLDER" "$DOC_FILE" 2>/dev/null; then
            echo "  ❌ $DOC_FILE tiene placeholders sin reemplazar"
        else
            echo "  ✅ $DOC_FILE sin placeholders pendientes"
            SCORE=$((SCORE + 1))
        fi
    fi
done

echo ""
echo "📊 Resultado: $SCORE/$TOTAL verificaciones de contenido"
echo "══════════════════════════════════════════════"
```

---

## CATEGORÍA 3: HERRAMIENTAS DEL ENTORNO (¿Están instaladas y accesibles?)

```bash
echo "══════════════════════════════════════════════"
echo "🔧 CATEGORÍA 3: HERRAMIENTAS DEL ENTORNO"
echo "══════════════════════════════════════════════"

SCORE=0
TOTAL=0

check_tool() {
    # $1 = comando, $2 = nombre descriptivo, $3 = criticidad (CRITICAL/OPTIONAL)
    TOTAL=$((TOTAL + 1))
    if command -v "$1" &>/dev/null; then
        VERSION=$($1 --version 2>&1 | head -1)
        echo "  ✅ $2: $VERSION"
        SCORE=$((SCORE + 1))
    else
        if [ "$3" = "CRITICAL" ]; then
            echo "  ❌ $2: NO INSTALADO (CRÍTICO)"
        else
            echo "  ⚠️ $2: no instalado (opcional)"
            SCORE=$((SCORE + 1))  # No penalizar opcionales
        fi
    fi
}

echo ""
echo "--- Herramientas críticas ---"
check_tool "node" "Node.js" "CRITICAL"
check_tool "npm" "npm" "CRITICAL"
check_tool "git" "Git" "CRITICAL"

echo ""
echo "--- Agentes AI (Multi-vendor) ---"
check_tool "gemini" "Gemini CLI" "CRITICAL"
check_tool "claude" "Claude Code CLI" "CRITICAL"
check_tool "codex" "Codex CLI" "CRITICAL"

echo ""
echo "--- Herramientas auxiliares ---"
check_tool "jq" "jq (JSON processor)" "OPTIONAL"
check_tool "curl" "curl" "CRITICAL"
check_tool "docker" "Docker" "OPTIONAL"

echo ""
echo "--- Versiones mínimas recomendadas ---"
TOTAL=$((TOTAL + 1))
NODE_MAJOR=$(node --version 2>/dev/null | sed 's/v//' | cut -d. -f1)
if [ -n "$NODE_MAJOR" ] && [ "$NODE_MAJOR" -ge 18 ]; then
    echo "  ✅ Node.js >= 18 (tienes v$NODE_MAJOR)"
    SCORE=$((SCORE + 1))
elif [ -n "$NODE_MAJOR" ]; then
    echo "  ⚠️ Node.js $NODE_MAJOR (recomendado >= 18)"
else
    echo "  ❌ No se pudo verificar versión de Node.js"
fi

echo ""
echo "📊 Resultado: $SCORE/$TOTAL herramientas verificadas"
echo "══════════════════════════════════════════════"
```

---

## CATEGORÍA 4: PERMISOS Y EJECUTABILIDAD

```bash
echo "══════════════════════════════════════════════"
echo "🔐 CATEGORÍA 4: PERMISOS Y EJECUTABILIDAD"
echo "══════════════════════════════════════════════"

SCORE=0
TOTAL=0

check_executable() {
    TOTAL=$((TOTAL + 1))
    if [ -f "$1" ]; then
        if [ -x "$1" ]; then
            echo "  ✅ $1 es ejecutable"
            SCORE=$((SCORE + 1))
        else
            echo "  ❌ $1 existe pero NO es ejecutable (falta chmod +x)"
        fi
    else
        echo "  ❌ $1 no existe"
    fi
}

echo ""
echo "--- Scripts deben ser ejecutables ---"
for SCRIPT in .gemini/scripts/*.sh .subagents/*.sh; do
    if [ -f "$SCRIPT" ]; then
        check_executable "$SCRIPT"
    fi
done

echo ""
echo "--- Verificar shebang correcto ---"
for SCRIPT in .gemini/scripts/*.sh .subagents/*.sh; do
    if [ -f "$SCRIPT" ]; then
        TOTAL=$((TOTAL + 1))
        FIRST_LINE=$(head -1 "$SCRIPT")
        if echo "$FIRST_LINE" | grep -q "^#!/bin/bash\|^#!/usr/bin/env bash"; then
            echo "  ✅ $SCRIPT tiene shebang correcto"
            SCORE=$((SCORE + 1))
        else
            echo "  ❌ $SCRIPT shebang incorrecto: $FIRST_LINE"
        fi
    fi
done

echo ""
echo "--- Biblioteca central scripts (si existe) ---"
if [ -d "_global-profile/.antigravity/library/scripts" ]; then
    for SCRIPT in _global-profile/.antigravity/library/scripts/*.sh; do
        if [ -f "$SCRIPT" ]; then
            check_executable "$SCRIPT"
        fi
    done
fi

echo ""
echo "--- Directorios escribibles (para logs y outputs) ---"
for DIR in .gemini/agents/logs docs/research .gemini/brain; do
    TOTAL=$((TOTAL + 1))
    mkdir -p "$DIR" 2>/dev/null
    if [ -w "$DIR" ]; then
        echo "  ✅ $DIR es escribible"
        SCORE=$((SCORE + 1))
    else
        echo "  ❌ $DIR NO es escribible"
    fi
done

echo ""
echo "📊 Resultado: $SCORE/$TOTAL permisos verificados"
echo "══════════════════════════════════════════════"
```

---

## CATEGORÍA 5: VALIDACIÓN DE SINTAXIS (¿Los archivos de configuración son válidos?)

```bash
echo "══════════════════════════════════════════════"
echo "✏️  CATEGORÍA 5: VALIDACIÓN DE SINTAXIS"
echo "══════════════════════════════════════════════"

SCORE=0
TOTAL=0

echo ""
echo "--- JSON válido ---"
for JSON_FILE in .gemini/settings.json .subagents/manifest.json; do
    TOTAL=$((TOTAL + 1))
    if [ -f "$JSON_FILE" ]; then
        if jq empty "$JSON_FILE" 2>/dev/null; then
            echo "  ✅ $JSON_FILE es JSON válido"
            SCORE=$((SCORE + 1))
        else
            echo "  ❌ $JSON_FILE tiene JSON INVÁLIDO"
            jq empty "$JSON_FILE" 2>&1 | head -3 | sed 's/^/     /'
        fi
    else
        echo "  ❌ $JSON_FILE no existe"
    fi
done

echo ""
echo "--- Biblioteca central catalog.json ---"
if [ -f "_global-profile/.antigravity/library/catalog.json" ]; then
    TOTAL=$((TOTAL + 1))
    if jq empty "_global-profile/.antigravity/library/catalog.json" 2>/dev/null; then
        echo "  ✅ catalog.json es JSON válido"
        SCORE=$((SCORE + 1))
    else
        echo "  ❌ catalog.json tiene JSON INVÁLIDO"
    fi
fi

echo ""
echo "--- YAML válido (.codex/config.yaml) ---"
TOTAL=$((TOTAL + 1))
if [ -f ".codex/config.yaml" ]; then
    # Verificación básica de YAML
    if grep -q "^[a-zA-Z]" ".codex/config.yaml" 2>/dev/null; then
        echo "  ✅ .codex/config.yaml tiene estructura YAML"
        SCORE=$((SCORE + 1))
    else
        echo "  ⚠️ .codex/config.yaml puede tener problemas de formato"
    fi
else
    echo "  ❌ .codex/config.yaml no existe"
fi

echo ""
echo "--- TOML básico (sub-agentes Gemini) ---"
for TOML_FILE in .gemini/agents/*.toml; do
    TOTAL=$((TOTAL + 1))
    if [ -f "$TOML_FILE" ]; then
        HAS_NAME=$(grep -c "^name" "$TOML_FILE" 2>/dev/null)
        HAS_DESC=$(grep -c "^description" "$TOML_FILE" 2>/dev/null)
        HAS_PROMPT=$(grep -c "system_prompt" "$TOML_FILE" 2>/dev/null)

        if [ "$HAS_NAME" -gt 0 ] && [ "$HAS_DESC" -gt 0 ] && [ "$HAS_PROMPT" -gt 0 ]; then
            echo "  ✅ $TOML_FILE estructura TOML correcta"
            SCORE=$((SCORE + 1))
        else
            echo "  ⚠️ $TOML_FILE faltan campos (name:$HAS_NAME desc:$HAS_DESC prompt:$HAS_PROMPT)"
        fi
    fi
done

echo ""
echo "--- Bash syntax check ---"
for SCRIPT in .gemini/scripts/*.sh .subagents/*.sh; do
    if [ -f "$SCRIPT" ]; then
        TOTAL=$((TOTAL + 1))
        if bash -n "$SCRIPT" 2>/dev/null; then
            echo "  ✅ $SCRIPT sintaxis bash válida"
            SCORE=$((SCORE + 1))
        else
            echo "  ❌ $SCRIPT tiene errores de sintaxis:"
            bash -n "$SCRIPT" 2>&1 | head -3 | sed 's/^/     /'
        fi
    fi
done

echo ""
echo "--- Markdown (sin caracteres rotos) ---"
for MD_FILE in GEMINI.md CLAUDE.md CHANGELOG.md docs/README.md docs/DEVLOG.md; do
    TOTAL=$((TOTAL + 1))
    if [ -f "$MD_FILE" ]; then
        if file "$MD_FILE" | grep -q "text"; then
            echo "  ✅ $MD_FILE es texto válido"
            SCORE=$((SCORE + 1))
        else
            echo "  ⚠️ $MD_FILE encoding sospechoso: $(file "$MD_FILE")"
        fi
    else
        echo "  ❌ $MD_FILE no existe"
    fi
done

echo ""
echo "📊 Resultado: $SCORE/$TOTAL validaciones de sintaxis"
echo "══════════════════════════════════════════════"
```

---

## CATEGORÍA 6: CONECTIVIDAD Y AUTENTICACIÓN

```bash
echo "══════════════════════════════════════════════"
echo "🌐 CATEGORÍA 6: CONECTIVIDAD Y AUTENTICACIÓN"
echo "══════════════════════════════════════════════"

SCORE=0
TOTAL=0

echo ""
echo "--- Gemini CLI autenticado ---"
TOTAL=$((TOTAL + 1))
if command -v gemini &>/dev/null; then
    GEMINI_AUTH=$(timeout 30 gemini -p "Responde solo: OK" --non-interactive 2>&1 | head -5)
    if echo "$GEMINI_AUTH" | grep -qi "ok\|OK\|gemini"; then
        echo "  ✅ Gemini CLI responde (autenticado)"
        SCORE=$((SCORE + 1))
    elif echo "$GEMINI_AUTH" | grep -qi "auth\|login\|credential\|error"; then
        echo "  ❌ Gemini CLI: problema de autenticación"
        echo "     $GEMINI_AUTH" | head -2 | sed 's/^/     /'
    else
        echo "  ⚠️ Gemini CLI: respuesta inesperada"
    fi
else
    echo "  ❌ Gemini CLI no instalado"
fi

echo ""
echo "--- Claude Code autenticado ---"
TOTAL=$((TOTAL + 1))
if command -v claude &>/dev/null; then
    CLAUDE_AUTH=$(timeout 30 claude -p "Responde solo: OK" --no-input 2>&1 | head -5)
    if echo "$CLAUDE_AUTH" | grep -qi "ok\|OK\|claude"; then
        echo "  ✅ Claude Code responde (autenticado)"
        SCORE=$((SCORE + 1))
    elif echo "$CLAUDE_AUTH" | grep -qi "auth\|login\|key\|error"; then
        echo "  ❌ Claude Code: problema de autenticación"
        echo "     $CLAUDE_AUTH" | head -2 | sed 's/^/     /'
    else
        echo "  ⚠️ Claude Code: respuesta inesperada"
    fi
else
    echo "  ❌ Claude Code CLI no instalado"
fi

echo ""
echo "--- Codex CLI autenticado ---"
TOTAL=$((TOTAL + 1))
if command -v codex &>/dev/null; then
    # Codex puede verificarse con un comando simple
    CODEX_AUTH=$(timeout 30 codex --version 2>&1 | head -3)
    if echo "$CODEX_AUTH" | grep -qi "codex\|version\|[0-9]"; then
        echo "  ✅ Codex CLI disponible: $CODEX_AUTH"
        SCORE=$((SCORE + 1))
    else
        echo "  ⚠️ Codex CLI: respuesta inesperada"
    fi
else
    echo "  ❌ Codex CLI no instalado"
fi

echo ""
echo "--- Git configurado ---"
TOTAL=$((TOTAL + 1))
if git rev-parse --is-inside-work-tree &>/dev/null; then
    COMMIT_COUNT=$(git rev-list --count HEAD 2>/dev/null || echo "0")
    BRANCH=$(git branch --show-current 2>/dev/null || echo "desconocida")
    echo "  ✅ Git repo activo (rama: $BRANCH, commits: $COMMIT_COUNT)"
    SCORE=$((SCORE + 1))
else
    echo "  ⚠️ No es un repositorio Git"
fi

echo ""
echo "📊 Resultado: $SCORE/$TOTAL verificaciones de conectividad"
echo "══════════════════════════════════════════════"
```

---

## CATEGORÍA 7: TEST FUNCIONAL DE SUB-AGENTES

```bash
echo "══════════════════════════════════════════════"
echo "🤖 CATEGORÍA 7: TEST FUNCIONAL DE SUB-AGENTES"
echo "══════════════════════════════════════════════"
echo ""
echo "⚠️  Estos tests invocan agentes reales (consumen cuota)."
echo "    Ejecutar solo si Categorías 1-6 pasaron bien."
echo ""

SCORE=0
TOTAL=0
```

Para esta categoría, ejecuta cada test UNO POR UNO y reporta el resultado.
No ejecutes todos de golpe. Espera que cada uno termine.

### Test 7.1: Sub-agente doc-writer (Gemini CLI)

```bash
echo ""
echo "--- Test 7.1: doc-writer via Gemini CLI ---"
TOTAL=$((TOTAL + 1))

RESULT=$(timeout 120 gemini -p "Eres doc-writer. Genera una entrada de DEVLOG para hoy que diga: 'Se completó la auditoría del sistema agéntico'. Formato Keep a Changelog, en español. Solo responde con el texto markdown." --yolo 2>&1 | tail -20)

if echo "$RESULT" | grep -qi "auditoría\|agéntico\|DEVLOG\|##"; then
    echo "  ✅ doc-writer respondió correctamente"
    SCORE=$((SCORE + 1))
else
    echo "  ❌ doc-writer no respondió como esperado"
    echo "     Output: $(echo "$RESULT" | tail -3)"
fi
```

### Test 7.2: Claude Code como sub-agente

```bash
echo ""
echo "--- Test 7.2: Claude Code CLI ---"
TOTAL=$((TOTAL + 1))

if command -v claude &>/dev/null; then
    RESULT=$(timeout 120 claude -p "Responde brevemente: ¿Qué archivo deberías leer primero al trabajar en este proyecto? (pista: CLAUDE.md)" --no-input 2>&1 | tail -10)

    if echo "$RESULT" | grep -qi "CLAUDE\|claude\|proyecto\|documentación"; then
        echo "  ✅ Claude Code respondió correctamente"
        SCORE=$((SCORE + 1))
    else
        echo "  ⚠️ Claude Code respondió pero sin contexto del proyecto"
        echo "     Output: $(echo "$RESULT" | tail -3)"
    fi
else
    echo "  ❌ Claude Code no disponible (no instalado)"
fi
```

### Test 7.3: Codex CLI (researcher agent)

```bash
echo ""
echo "--- Test 7.3: Codex CLI ---"
TOTAL=$((TOTAL + 1))

if command -v codex &>/dev/null; then
    # Test básico de Codex
    RESULT=$(timeout 120 codex exec "Responde solo: OK" 2>&1 | tail -10)

    if echo "$RESULT" | grep -qi "ok\|OK"; then
        echo "  ✅ Codex CLI respondió correctamente"
        SCORE=$((SCORE + 1))
    else
        echo "  ⚠️ Codex CLI: respuesta inesperada"
        echo "     Output: $(echo "$RESULT" | tail -3)"
    fi
else
    echo "  ❌ Codex CLI no disponible"
fi
```

### Test 7.4: Dispatcher multi-vendor

```bash
echo ""
echo "--- Test 7.4: Verificación de dispatcher multi-vendor ---"
TOTAL=$((TOTAL + 1))

if [ -x ".subagents/dispatch.sh" ]; then
    echo "  ✅ dispatch.sh existe y es ejecutable"
    SCORE=$((SCORE + 1))

    # Verificar que soporte los 3 vendors
    TOTAL=$((TOTAL + 1))
    if grep -q "gemini\|claude\|codex" .subagents/dispatch.sh 2>/dev/null; then
        echo "  ✅ dispatch.sh soporta múltiples vendors"
        SCORE=$((SCORE + 1))
    else
        echo "  ⚠️ dispatch.sh puede no soportar todos los vendors"
    fi
else
    echo "  ❌ dispatch.sh no existe o no es ejecutable"
fi
```

### Test 7.5: Biblioteca central scripts

```bash
echo ""
echo "--- Test 7.5: Biblioteca central (si existe) ---"
if [ -d "_global-profile/.antigravity/library/scripts" ]; then
    for SCRIPT in enable.sh disable.sh list.sh; do
        TOTAL=$((TOTAL + 1))
        if [ -x "_global-profile/.antigravity/library/scripts/$SCRIPT" ]; then
            echo "  ✅ $SCRIPT existe y es ejecutable"
            SCORE=$((SCORE + 1))
        else
            echo "  ❌ $SCRIPT no existe o no es ejecutable"
        fi
    done
else
    echo "  ⚠️ Biblioteca central no configurada (opcional)"
fi
```

```bash
echo ""
echo "📊 Resultado: $SCORE/$TOTAL tests funcionales"
echo "══════════════════════════════════════════════"
```

---

## CATEGORÍA 8: COHERENCIA Y CROSS-REFERENCES

Verifica que los archivos se referencien correctamente entre sí:

```bash
echo "══════════════════════════════════════════════"
echo "🔗 CATEGORÍA 8: COHERENCIA Y CROSS-REFERENCES"
echo "══════════════════════════════════════════════"

SCORE=0
TOTAL=0

echo ""
echo "--- GEMINI.md referencia todos los sub-agentes Gemini ---"
for AGENT_FILE in .gemini/agents/*.toml; do
    if [ -f "$AGENT_FILE" ]; then
        AGENT_NAME=$(basename "$AGENT_FILE" .toml)
        TOTAL=$((TOTAL + 1))
        if grep -q "$AGENT_NAME" GEMINI.md 2>/dev/null; then
            echo "  ✅ GEMINI.md menciona $AGENT_NAME"
            SCORE=$((SCORE + 1))
        else
            echo "  ❌ GEMINI.md NO menciona $AGENT_NAME"
        fi
    fi
done

echo ""
echo "--- manifest.json referencia todos los sub-agentes ---"
# Verificar agentes Gemini
for AGENT_FILE in .gemini/agents/*.toml; do
    if [ -f "$AGENT_FILE" ]; then
        AGENT_NAME=$(basename "$AGENT_FILE" .toml)
        TOTAL=$((TOTAL + 1))
        if grep -q "$AGENT_NAME" .subagents/manifest.json 2>/dev/null; then
            echo "  ✅ manifest.json registra $AGENT_NAME"
            SCORE=$((SCORE + 1))
        else
            echo "  ❌ manifest.json NO registra $AGENT_NAME"
        fi
    fi
done

# Verificar researcher (Codex)
TOTAL=$((TOTAL + 1))
if grep -q "researcher" .subagents/manifest.json 2>/dev/null; then
    echo "  ✅ manifest.json registra researcher"
    SCORE=$((SCORE + 1))
else
    echo "  ❌ manifest.json NO registra researcher"
fi

echo ""
echo "--- Agentes Codex tienen equivalente en manifest ---"
for AGENT_FILE in .codex/agents/*.md; do
    if [ -f "$AGENT_FILE" ]; then
        AGENT_NAME=$(basename "$AGENT_FILE" .md)
        TOTAL=$((TOTAL + 1))
        if grep -q "$AGENT_NAME" .subagents/manifest.json 2>/dev/null; then
            echo "  ✅ Codex agent $AGENT_NAME está en manifest"
            SCORE=$((SCORE + 1))
        else
            echo "  ⚠️ Codex agent $AGENT_NAME no está explícito en manifest"
        fi
    fi
done

echo ""
echo "--- Multi-vendor configurado correctamente ---"
TOTAL=$((TOTAL + 1))
VENDORS_COUNT=$(grep -o "supported_vendors" .subagents/manifest.json 2>/dev/null | wc -l)
if [ "$VENDORS_COUNT" -gt 3 ]; then
    echo "  ✅ Multi-vendor configurado ($VENDORS_COUNT agentes)"
    SCORE=$((SCORE + 1))
else
    echo "  ⚠️ Solo $VENDORS_COUNT agentes tienen supported_vendors"
fi

echo ""
echo "--- Docs referenciados existen ---"
for DOC in "docs/DEVLOG.md" "docs/TODO.md" "docs/README.md" "docs/research" "CHANGELOG.md"; do
    TOTAL=$((TOTAL + 1))
    if [ -e "$DOC" ]; then
        echo "  ✅ $DOC existe"
        SCORE=$((SCORE + 1))
    else
        echo "  ❌ $DOC NO existe"
    fi
done

echo ""
echo "--- .gitignore cubre archivos sensibles ---"
TOTAL=$((TOTAL + 1))
IGNORE_CHECKS=0
grep -q ".env" .gitignore 2>/dev/null && IGNORE_CHECKS=$((IGNORE_CHECKS + 1))
grep -q "node_modules" .gitignore 2>/dev/null && IGNORE_CHECKS=$((IGNORE_CHECKS + 1))
grep -q "__pycache__" .gitignore 2>/dev/null && IGNORE_CHECKS=$((IGNORE_CHECKS + 1))
if [ "$IGNORE_CHECKS" -ge 2 ]; then
    echo "  ✅ .gitignore cubre archivos sensibles ($IGNORE_CHECKS/3 patterns)"
    SCORE=$((SCORE + 1))
else
    echo "  ⚠️ .gitignore incompleto ($IGNORE_CHECKS/3 patterns)"
fi

echo ""
echo "📊 Resultado: $SCORE/$TOTAL verificaciones de coherencia"
echo "══════════════════════════════════════════════"
```

---

## REPORTE FINAL CONSOLIDADO

Al terminar TODAS las categorías, genera este reporte:

```bash
echo ""
echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║      REPORTE DE AUDITORÍA — SISTEMA AGÉNTICO MULTI-VENDOR   ║"
echo "║                $(date +%Y-%m-%d\ %H:%M)                            ║"
echo "╠══════════════════════════════════════════════════════════════╣"
echo "║                                                              ║"
echo "║  Cat. 1: Estructura de archivos    → __/__ (___%)            ║"
echo "║  Cat. 2: Integridad de contenido   → __/__ (___%)            ║"
echo "║  Cat. 3: Herramientas del entorno  → __/__ (___%)            ║"
echo "║  Cat. 4: Permisos y ejecutabilidad → __/__ (___%)            ║"
echo "║  Cat. 5: Validación de sintaxis    → __/__ (___%)            ║"
echo "║  Cat. 6: Conectividad y auth       → __/__ (___%)            ║"
echo "║  Cat. 7: Tests funcionales         → __/__ (___%)            ║"
echo "║  Cat. 8: Coherencia y cross-refs   → __/__ (___%)            ║"
echo "║                                                              ║"
echo "║  TOTAL GENERAL:  ___/___ (___%)                              ║"
echo "║                                                              ║"
echo "║  VENDORS VERIFICADOS:                                        ║"
echo "║    • Gemini CLI:  [OK/FAIL]                                  ║"
echo "║    • Claude Code: [OK/FAIL]                                  ║"
echo "║    • Codex CLI:   [OK/FAIL]                                  ║"
echo "║                                                              ║"
echo "║  VEREDICTO:                                                  ║"
echo "║    >= 90%  → ✅ SISTEMA LISTO PARA PRODUCCIÓN                ║"
echo "║    70-89%  → ⚠️  FUNCIONAL CON ADVERTENCIAS                  ║"
echo "║    < 70%   → ❌ REQUIERE CORRECCIONES                        ║"
echo "║                                                              ║"
echo "╠══════════════════════════════════════════════════════════════╣"
echo "║  ACCIONES CORRECTIVAS REQUERIDAS:                            ║"
echo "║                                                              ║"
echo "║  (Lista aquí cada ❌ encontrada con su fix)                  ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
```

**INSTRUCCIONES PARA EL REPORTE FINAL:**

1. Reemplaza los `__` con los números reales de cada categoría
2. Calcula porcentajes reales
3. Para CADA ❌ encontrada, escribe:
   - Qué falló
   - Comando exacto para corregirlo
   - Prioridad (CRÍTICO / MEDIO / BAJO)
4. Para CADA ⚠️, indica si requiere acción o es aceptable
5. Da un veredicto final honesto
6. Si el score es < 90%, pregunta al usuario si quiere que corrijas las fallas automáticamente

---

**FIN DEL PROMPT DE AUDITORÍA MULTI-VENDOR. Ejecuta categoría por categoría y genera el reporte final consolidado.**
