# Taller de la semana 2 — El mundo de la aspiradora: completar la clasificación

**Complemento de** [`../../weeks/week-02.md`](../../weeks/week-02.md) — Sesión B.
**Distribución del tiempo:** Repaso 5 · Trabajo en grupos 45 · Demostraciones 20 · Puesta en común 10 (80 min en total).
**Entregables:** todas las pruebas proporcionadas superadas, una tabla de puntuaciones del torneo para los cuatro
agentes clásicos, una ficha de evaluación del agente LLM (los ocho ejes) y una entrada en el Atlas de Fallos.

> **Repaso (5 min).** *Menciona algo que el agente basado en modelos pueda hacer y que el agente reactivo
> no pueda hacer de manera demostrable.* (Observarás el fallo de esta misma garantía en una prueba.)

## Archivos de esta carpeta

| Archivo | Propósito | ¿Lo editas? |
|---|---|---|
| [`vacuum.py`](vacuum.py) | Proporcionado: el mundo + `simple_reflex` + `model_based` + `run`, sin cambios respecto al notebook | ❌ |
| [`configs.json`](configs.json) | Proporcionado: las 8 configuraciones iniciales (2² estados de suciedad × 2 ubicaciones) | ❌ |
| [`tournament.py`](tournament.py) | Proporcionado: el modelo de costo energético + el evaluador `net_utility` + la función `tournament()` que imprime resultados | ❌ (úsalo) |
| [`starter.py`](starter.py) | **Tarea 1** — implementa `goal_based` y `utility_based` | ✅ |
| [`test_agents.py`](test_agents.py) | Pruebas proporcionadas, incluida `test_reflex_fails_under_partial_observability` | ❌ |
| [`_generate_configs.py`](_generate_configs.py) | Regenera `configs.json` mediante una enumeración determinista, sin semilla | ❌ |

## Tarea 1 — Completa la clasificación y ejecuta las pruebas proporcionadas (15 min)

Ya tienes dos de las cuatro arquitecturas (`simple_reflex`, `model_based`).
Abre `starter.py` y añade las otras dos:

- `goal_based` — planifica hacia un objetivo explícito (ambas habitaciones limpias) y después
  **se detiene** (`NoOp`). El agente reactivo oscila indefinidamente; el agente basado en objetivos
  sabe cuándo ha terminado, igual que el basado en modelos, pero lo plantea
  como *alcanzar un estado especificado* en lugar de reaccionar.
- `utility_based` — maximiza la **utilidad neta** paso a paso según el modelo de costo
  de `tournament.py`: moverse cuesta 1, `Suck` cuesta 2 y cada habitación limpia
  aporta 3 por paso. La función del agente solo ve la percepción actual:
  **no anticipa pasos futuros**, así que razona de forma voraz sobre el cambio neto inmediato.

Después ejecuta:

```bash
python3 test_agents.py
```

Las cinco pruebas deben pasar. Dos comprueban deliberadamente una propiedad *sorprendente*:

- `test_reflex_fails_under_partial_observability` — con el sensor de ubicación
  averiado (`BrokenSensorWorld`), `simple_reflex` deja una habitación sucia mientras
  `model_based` limpia ambas. **Es la pregunta del repaso convertida en una
  aserción.** Una prueba que espera que el agente reactivo *falle* no es un error;
  observar el fallo de una garantía *una vez* permite comprobar qué aporta
  el estado interno. (Solo usa los agentes proporcionados, así que pasa antes de que escribas
  código: es una referencia fija para comprobar tu entorno.)
- `test_utility_leaves_a_room_dirty` — tu agente racional `utility_based`
  deja al menos una habitación sucia en alguna de las 8 configuraciones. **No es un error.** Es
  racionalidad bajo un modelo de costo: pagar por desplazarse a una habitación cuyo beneficio
  no puede observar no compensa de inmediato. Repórtalo como un resultado.

Ahora ejecuta el torneo: los cuatro agentes, las 8 configuraciones y utilidad neta.

```python
from vacuum import simple_reflex, model_based
from tournament import tournament
from starter import goal_based, utility_based

tournament({
    "reflex":  lambda: simple_reflex,   # función directa: envuélvela en una fábrica
    "model":   model_based,
    "goal":    goal_based,
    "utility": utility_based,
})
```

El **descubrimiento esperado**: el total del agente basado en utilidad no es el mayor porque
desaprovecha valor. Debes poder explicar, en una oración, *por qué la interfaz
(`percept → action`, sin horizonte) obliga al comportamiento voraz*: esa es la justificación
de la búsqueda y la planificación en las semanas 3–9.

Para las parejas que terminen pronto: **amplíen `VacuumWorld` a n habitaciones.** ¿Qué agentes siguen
funcionando sin cambios y cuáles necesitan reescribirse? (Es la pregunta sobre representación atómica → factorizada
de las diapositivas, presentada como una refactorización.)

## Tarea 2 — Un LLM como función del agente (20 min)

Conecta un modelo de lenguaje a la **misma** interfaz `percept → action`. `starter.py`
contiene el esquema y el prompt exacto del plan. Tú proporcionas la llamada al modelo mediante
`aicourse.llm.LLM`; la abstracción de 1995 hace el resto.

Requisitos, cada uno con una enseñanza:

- `parse_action` debe manejar respuestas como `"Suck."`, `"I would suck"` o
  un párrafo de razonamiento. **Registra cada fallo de análisis**: una salida mal formada es un
  tipo de fallo sin equivalente clásico y debe aparecer en la ficha de evaluación
  (eje 8).
- Ejecuta las mismas **8 configuraciones** y compara con los cuatro agentes clásicos.
- Ejecuta **una** configuración **cinco veces** y cuenta las secuencias de acciones distintas.
  Es una demostración directa de la reproducibilidad (eje 5). *Conserva esta ejecución*: importa más
  que cubrir muchos casos.
- **Si Ollama es lento, limita la tarea 2 a 3 configuraciones** e indícalo. Conserva
  en cualquier caso las cinco repeticiones para medir reproducibilidad.

**No** dejes que el modelo sea su propio oráculo («¿parece correcta tu acción?»).
Evalúa cada episodio con el mismo código de `vacuum`/`tournament` con el que se evaluaron
los agentes clásicos.

## Tarea 3 — Ficha de evaluación (10 min)

Completa los **ocho** ejes para `utility_based` frente a `llm_agent`. Esta es tu primera
ficha completa; es normal que sea débil: el espacio de demostración servirá para mejorarla.
Cuenta específicamente *cuántas líneas de código defensivo necesitó el agente LLM que
los agentes clásicos no necesitaron*: un analizador, un reintento, una respuesta por defecto. Esa proporción es un
dato real de ingeniería.

## Demostraciones (20 min)

- Una pareja presenta el resultado de **utilidad que deja suciedad**: pregunta si alguien
  lo reportó inicialmente como un error y luego interprétalo como racionalidad bajo un modelo de costo.
- Una pareja presenta su **fallo de análisis de respuesta del LLM más interesante**. Pregunta: *¿cuántas
  líneas de código defensivo necesitó el agente LLM que los agentes clásicos
  no necesitaron?*
- Solicita el conteo de reproducibilidad de las cinco repeticiones. Obtener secuencias distintas con la misma
  entrada demuestra el eje 5 en vivo.

## Puesta en común (10 min)

1. El agente LLM **no** es una arquitectura nueva. Es una política conectada a la
   misma interfaz `percept → action`. La abstracción de 1995 sigue vigente.
2. El agente LLM necesitó un analizador, un reintento y una respuesta por defecto. Los agentes clásicos
   no necesitaron ninguno. **El costo se esconde en la ingeniería de fiabilidad.**
3. En un mundo de 2 habitaciones, el LLM es caro y peor. Pregunta: *¿cuándo se invierte esa situación?*
   Respuesta: cuando el espacio de estados es enorme, informal y lingüístico; cuando escribir
   las reglas es la parte difícil. Ese argumento a favor de los agentes LLM aparece en la
   semana 9.

**Entrega de la entrada del Atlas de Fallos**: registra tu mejor fallo de análisis de respuesta (consulta la carpeta de recursos).

## Enlaces

- Notebook de la sesión A — [`../../notebooks/week-02-vacuum-world.ipynb`](../../notebooks/week-02-vacuum-world.ipynb)
- Plan de clase — [`../../weeks/week-02.md`](../../weeks/week-02.md)
- Diapositivas — [`../../slides/week-02/deck.md`](../../slides/week-02/deck.md)
- Artículo: ReAct (Yao y colaboradores, 2022) — [arXiv:2210.03629](https://arxiv.org/abs/2210.03629)
- Política de IA (`AI_LOG.md`) — [`../../resources/ai-policy.md`](../../resources/ai-policy.md)
