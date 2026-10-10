# Semana 6 Studio — La inferencia supera a la búsqueda, y el solucionador posee la garantía

**Complemento de** [`../../weeks/week-06.md`](../../weeks/week-06.md) — Sesión 6B.
**Tiempo estimado:** Repaso 5 · Trabajo en grupos 45 · Demos 20 · Cierre 10 (80 min en total).
**Entregables:** todas las pruebas proporcionadas deben pasar, una tabla de ablación de la Tarea 1 para tu propio
horario, y la tabla comparativa de los tres enfoques (A / B / C) con la taxonomía de fallos del enfoque B.

> **Repaso (5 min).** *¿Qué produjo una mayor mejora — forward checking o MRV? ¿Por qué?*
> Pregunta directa. Si nadie responde: en el Sudoku HARD del notebook, forward checking
> **alcanza el timeout** y MRV marca la diferencia entre *resuelto* y *nunca termina*.
> El ordenamiento de variables busca **fallar rápido**; el ordenamiento de valores busca **tener éxito primero**.

> **El Duelo 1 (Búsqueda) fue entregado en la Sesión 6A.** Si tu pareja todavía no lo ha entregado,
> hagan eso primero — especificación en [`../../projects/duel-1-search.md`](../../projects/duel-1-search.md).

## Archivos en esta carpeta

| Archivo | Propósito | ¿Lo editas? |
|---|---|---|
| [`csp.py`](csp.py) | Proporcionado: `CSP`, `backtrack_search` (interruptores fc / mrv / lcv / ac3), `ac3`, y los Sudokus (`EASY`/`MED`/`HARD`) + instancias del mapa de Australia — sin cambios respecto al notebook | ❌ |
| [`logic_lm.py`](logic_lm.py) | Proporcionado: la infraestructura del enfoque B — `MODEL_PROMPT`, `parse_json`, `build_csp` (alldiff / neq / eq), `classify_arm_b`, problemas de ejemplo resueltos y `load_puzzles()` | ❌ (úsalo) |
| [`puzzles.json`](puzzles.json) | Proporcionado: banco de **20** problemas lógicos verificados en lenguaje natural (enunciado NL + especificación CSP + respuesta gold única). 5 están marcados como `worked_example` | ❌ (úsalo) |
| [`_verify_puzzles.py`](_verify_puzzles.py) | Proporcionado: verificación de corrección — cada problema se construye mediante `build_csp`, tiene una solución **única** que coincide con su gold y vuelve a resolverse con `backtrack_search` | ❌ (ejecútalo) |
| [`starter.py`](starter.py) | **Tareas 1–2** — modelar el CSP del horario y escribir el ciclo de refinamiento del enfoque B | ✅ |
| [`test_csp.py`](test_csp.py) | Pruebas proporcionadas, incluidas `test_lcv_can_hurt` y `test_plain_backtracking_blows_up` | ❌ |

El motor CSP no tiene un archivo `instances.json`: las instancias de búsqueda del notebook son cadenas fijas
(`HARD`/`EASY`/`MED`) y el mapa de Australia, por lo que se encuentran directamente en `csp.py`
exactamente como las define el notebook — no se genera nada aleatoriamente. El banco de problemas
de Logic-LM, en cambio, se distribuye como [`puzzles.json`](puzzles.json): 20 problemas escritos manualmente,
cada uno con una respuesta única verificada por el solucionador (ejecuta `python3 _verify_puzzles.py`
— imprime `ALL 20 PUZZLES SOUND`). Como `build_csp` solo admite `alldiff`,
`neq` y `eq`, cada problema es un pequeño problema de asignación (de 3 a 5 entidades) exactamente
con ese vocabulario.

## Tarea 1 — Resolver un CSP de horarios (15 min)

Abre `starter.py` y completa `scheduling_csp()`. Modela el problema del horario escolar
de la presentación: asigna a cada actividad un **periodo distinto** y respeta la única regla estricta
— **los deportes no pueden programarse después del almuerzo**.

Ambas partes se traducen directamente a la clase `CSP` del notebook:

- *All-different* → convierte cada actividad en **vecina** de todas las demás actividades
  (un grafo completo). La comprobación `consistent` del motor ya implementa all-different, por lo que
  el grafo completo constituye toda la codificación.
- *No deportes después del almuerzo* → restringe previamente el **dominio** de `Sports` a los periodos
  de la mañana (`1..LUNCH_AFTER`). Todas las demás actividades pueden tomar cualquier periodo.

Luego ejecuta:

```bash
python3 test_csp.py
```

`test_scheduling_is_valid_timetable` y `test_scheduling_sports_before_lunch`
comprueban que tu modelo produce un horario completo, con todos los periodos distintos y con deportes
en la mañana. Reporta la ablación para **tu propia** instancia utilizando `run_ablation` — las mismas
cuatro configuraciones del notebook, aplicadas a tu horario.

Las otras tres pruebas no requieren código adicional de tu parte — representan el punto principal
de la semana y se ejecutan sobre el Sudoku HARD del notebook:

- `test_ac3_prunes_hard_sudoku` — AC-3 reduce los dominios *antes de realizar cualquier suposición*.
- `test_plain_backtracking_blows_up` — el backtracking simple es **completo**, por lo que
  "debería" resolver cualquier problema que tenga solución. En HARD agota un presupuesto
  de 300 000 llamadas y nunca termina, mientras que fc + MRV + AC-3 lo resuelve en ~34 000.
  "Completo" no dice nada sobre *cuándo* terminará.
- `test_lcv_can_hurt` — LCV significa *least constraining value*; se supone que debe ayudar.
  En HARD hace que la búsqueda sea **estrictamente peor** (34,478 → 56,813 llamadas de backtracking).
  Una prueba que afirma que una heurística *falla* no es un error — el ordenamiento de valores es una apuesta
  cuyo costo pagas en cada rama, y debes reportar lo que realmente mides, no lo que el libro de texto sugiere.

## Tarea 2 — El experimento de tres enfoques (25 min)

Este es el experimento central del curso; vuelve a aparecer en las semanas 8, 9 y en el proyecto final.
Mismos problemas, tres pipelines:

| Enfoque | Pipeline |
|---|---|
| **A — Modelado manual** | tú escribes el CSP a mano → tu solucionador |
| **B — Híbrido (Logic-LM)** | el LLM escribe el CSP → tu solucionador |
| **C — LLM de extremo a extremo** | el LLM lee el problema y responde directamente |

El enfoque B contiene la parte de ingeniería. La infraestructura ya está proporcionada en `logic_lm.py` —
el `MODEL_PROMPT` exacto del plan, un `parse_json` tolerante, `build_csp` (que transforma la
especificación JSON en un CSP que resuelve tu *mismo* `backtrack_search`) y `classify_arm_b`,
que clasifica cada respuesta en las cuatro categorías del plan:

1. **`malformed_json`** — la respuesta no pudo parsearse (o la especificación está estructuralmente dañada)
2. **`valid_json_wrong_model`** — el solucionador devuelve una solución, pero es la solución incorrecta
3. **`valid_no_solution`** — sobre-restringido: un error de traducción que el solucionador rechaza
4. **`timeout`** — el solucionador alcanzó su límite de llamadas

Lo que **tú** escribes en `starter.py`: `solve_arm_b_with_refinement()` — la conexión del prompt
con tu modelo local **y el ciclo de auto-refinamiento**. Cuando el solucionador indique que no hay solución
o el JSON no pueda parsearse, devuelve el error al modelo y vuelve a intentarlo (máximo 3 intentos).
Reporta la tasa de resolución **con y sin** refinamiento — esa diferencia representa la contribución
real de Logic-LM y normalmente es grande.

```python
from aicourse.llm import LLM        # o tu propio cliente local
from logic_lm import load_puzzles, worked_examples
from starter import solve_arm_b_with_refinement

model = LLM()
for ex in worked_examples():        # los 5 ejemplos completamente resueltos, cada uno con un `gold`
    cat, sol, tries = solve_arm_b_with_refinement(model, ex["puzzle"], gold=ex["gold"])
    print(ex["id"], ex["puzzle"][:40], "->", cat, f"({tries} intentos)")

# luego ejecuta sobre los 20 problemas:
for p in load_puzzles():
    cat, sol, tries = solve_arm_b_with_refinement(model, p["puzzle"], gold=p["gold"])
```

La ejecución completa utiliza los **20** problemas lógicos en lenguaje natural de
[`puzzles.json`](puzzles.json), cargados mediante `load_puzzles()`. **Cinco están marcados
como `worked_example`** (`worked_examples()`) — los tres que siempre estuvieron directamente en
`logic_lm.py` (`p01`–`p03`) más otros dos (`p04`–`p05`) — completamente resueltos para que puedas
inspeccionar la transformación NL → especificación → gold y utilizarlos como ejemplos few-shot;
ejecuta los enfoques sobre los otros 15 y reporta cuántos resolviste en la tabla comparativa.
La respuesta gold de cada problema es única y ha sido verificada por el solucionador (`_verify_puzzles.py`),
por lo que las respuestas de los enfoques A / C pueden evaluarse contra ella sin ambigüedad.
Los modelos locales pequeños tienen dificultades para producir JSON válido; eso es realista —
mejora el prompt o utiliza decodificación restringida en lugar de recurrir a un modelo más grande.

**Tarea 3 — Tabla comparativa (5 min).** Esta vez utiliza tres columnas: A, B, C.
Reporta la tasa de resolución de cada enfoque, además de la taxonomía de fallos del enfoque B.

## Demos (20 min)

Pregunta específicamente por las taxonomías de fallos del enfoque B. El descubrimiento más importante
de la clase: **los fallos del enfoque B son visibles y los del enfoque C no lo son.**
Cuando el LLM escribe un CSP incorrecto, el solucionador frecuentemente *te lo dice*
(no hay solución, o existe un error de parseo). Cuando el LLM responde directamente y está equivocado,
no hay ninguna señal que lo indique. Haz que un estudiante lo diga explícitamente; si nadie lo hace,
pregunta: *"¿qué enfoque preferirían desplegar y cómo sabrían que falló?"*

## Cierre (10 min)

- El enfoque A es el mejor en términos de corrección, pero el peor en esfuerzo humano por problema.
- El enfoque C es el más sencillo y el menos confiable — con fallos **silenciosos**.
- El enfoque B normalmente se acerca al enfoque A en corrección mientras puede manejar lenguaje natural
  desordenado, y sus errores son **visibles**. Esa combinación es la razón por la que este patrón importa.
- **La garantía está en el solucionador.** Una vez que el modelo formal representa fielmente el problema,
  la corrección puede *demostrarse* (recuerda la prueba de inexistencia en el problema de coloreo de mapas
  dentro de `csp.py` — una capacidad categórica que no tiene equivalente directo en un LLM).
  El riesgo restante se concentra en la traducción, que es donde debes enfocar tus esfuerzos de verificación.
- Adelanto: las semanas 7–9 aplicarán este patrón a lógica y planificación, utilizando solucionadores
  progresivamente más potentes.

## Enlaces

- Notebook de la Sesión 6A — [`../../notebooks/week-06-csp.ipynb`](../../notebooks/week-06-csp.ipynb)
- Especificación del Duelo 1 (entregado esta semana) — [`../../projects/duel-1-search.md`](../../projects/duel-1-search.md)
- Tabla comparativa del Duelo — [`../../resources/duel-scorecard.md`](../../resources/duel-scorecard.md)
- Política de IA (`AI_LOG.md`) — [`../../resources/ai-policy.md`](../../resources/ai-policy.md)
