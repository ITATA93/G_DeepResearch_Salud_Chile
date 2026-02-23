# Plan de Investigación: Normativa Oncológica SSCoquimbo y Ovalle

## Objetivo
Identificar el marco regulatorio, leyes, unidades responsables y flujos de derivación del proceso oncológico en el Servicio de Salud Coquimbo, con foco en el Hospital de Ovalle.

## Estrategia de Búsqueda
Ejecutaremos búsquedas secuenciales para cubrir los distintos niveles de información:

1.  **Nivel Nacional (Marco Legal General):** Leyes que rigen el cáncer en Chile (Ley Nacional del Cáncer).
2.  **Nivel Regional (Red SSCoquimbo):** Organización de la red oncológica regional, centro de referencia (La Serena vs Ovalle).
3.  **Nivel Local (Hospital de Ovalle):** Unidades específicas (Unidad de Quimioterapia, Cuidados Paliativos), resoluciones exentas locales.

## Comandos de Ejecución
```bash
# 1. Marco General y Ley del Cáncer
python main.py research "Ley Nacional del Cáncer Chile resumen implicancias hospitales"

# 2. Red Oncológica Coquimbo
python main.py research "Red oncológica Servicio Salud Coquimbo derivación pacientes"

# 3. Hospital de Ovalle Específico
python main.py research "Hospital de Ovalle unidad oncología cartera de servicios"

# 4. Protocolos y Guías Clínicas (GES)
python main.py research "Guías Clínicas GES Cáncer Chile 2024 2025"
```

## Resultados Esperados
- Identificación de la **Ley 21.258** (Ley Nacional del Cáncer).
- Confirmación del rol del **Hospital de La Serena** como centro de referencia suprarregional (probablemente) y el rol del **Hospital de Ovalle** (posiblemente quimioterapia ambulatoria o paliativos).
- Unidades clave: UPA (Unidad de Patología Mamaria), Cuidados Paliativos, Comité Oncológico.
