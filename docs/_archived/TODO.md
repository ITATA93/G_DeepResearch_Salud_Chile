# Tareas Pendientes: Inicialización AG_DeepResearch_Salud_Chile

## 1. Configuración de Entorno (Prioridad Alta)
- [ ] **Crear entorno virtual:**
  ```bash
  python -m venv .venv
  .\.venv\Scripts\activate
  ```
- [ ] **Instalar Dependencias:**
  ```bash
  pip install -r requirements.txt
  ```
  *(Verificar instalación de duckduckgo-search y trafilatura)*

## 2. Verificación de Arquitectura
- [ ] **Test de Memoria:** Ejecutar el CLI por primera vez para inicializar la Bóveda.
  ```bash
  python main.py --help
  ```
  *Resultado esperado: Creación automática de `data/knowledge_vault.db` con tablas `sources_index` y `audit_log`.*

## 3. Pruebas Funcionales (Zero-Cost Stack)
- [ ] **Prueba de Auditoría (Mock):**
  ```bash
  python main.py audit "data/input/proceso_vacunas.txt"
  ```
- [ ] **Conexión de Herramientas:**
  - Editar `src/core/tools.py` para conectar `duckduckgo_search` con el agente.
  - Reemplazar los prints "MOCK" en `main.py` con la llamada real al agente.

## 4. Documentación
- [ ] Actualizar `README.md` del proyecto con instrucciones de uso específicas para la API gratuita.
