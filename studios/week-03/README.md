# Taller de la semana 3 — Una función de búsqueda, cuatro algoritmos

**Complemento de** [`../../weeks/week-03.md`](../../weeks/week-03.md) — Sesión 3B.
**Distribución del tiempo:** Repaso 5 · Trabajo en grupos 45 · Demostraciones 20 · Puesta en común 10 (80 min en total).
**Entregables:** todas las pruebas proporcionadas superadas, una formulación del problema que puedas defender y una
gráfica de escalabilidad en escala logarítmica.

> **Repaso (5 min).** *¿Por qué la prueba de objetivo se realiza al **expandir**, no al generar?*
> Pregunta a estudiantes sin previo aviso. Si nadie responde, vuelve a dibujar el grafo de 3 nodos (`TinyGraph` en `search.py`):
> `start→A` cuesta 10; `start→B→A` cuesta 2. Comprobar al generar devuelve 10.

## Archivos de esta carpeta

| Archivo | Propósito | ¿Lo editas? |
|---|---|---|
| [`search.py`](search.py) | Proporcionado: `Problem`, `Node`, `Frontier`, la función genérica `search()` y los problemas de ejemplo `EightPuzzle` / `TinyGraph`, sin cambios respecto al notebook | ❌ |
| [`instances.json`](instances.json) | Proporcionado: 40 instancias del rompecabezas de 8 fichas, 10 por profundidad óptima 4, 8, 12 y 16 (semilla 20260807; profundidades verificadas mediante BFS exhaustiva) | ❌ |
| [`starter.py`](starter.py) | **Tareas 1–3** — formula misioneros y caníbales, implementa los cuatro algoritmos y mide | ✅ |
| [`test_search.py`](test_search.py) | Pruebas proporcionadas, incluida `test_bfs_suboptimal_nonuniform_cost` | ❌ |
| [`_generate_instances.py`](_generate_instances.py) | Regenera `instances.json` (solo si cambias la semilla) | ❌ |

La interfaz `search()` es el **recurso más reutilizado** del curso: A\* de la semana 4
requiere cambiar unas 10 líneas, y el planificador de la semana 9 la importa sin cambios. Hazlo
bien y las semanas siguientes serán mucho más rápidas.

## Tarea 1 — Formula misioneros y caníbales (10 min)

Abre `starter.py` y completa `MissionariesAndCannibals(Problem)`: estado inicial,
`actions`, `result` e `is_goal`. **Todavía no hagas búsquedas**: es la formulación de cinco componentes
de las diapositivas expresada en código.

Tres misioneros, tres caníbales y un bote que lleva 1 o 2 personas, nunca vacío. Si
los caníbales **superan en número** a los misioneros en *cualquiera* de las orillas, incluida la que
acaba de dejar el bote, los misioneros son devorados. Lleva a todos al otro lado.

Cada año surgen dos cuestiones, y ambas son parte del objetivo:

1. La restricción se aplica a **ambas** orillas, *incluida la que acabas de dejar*.
2. ¿Excluyes los estados ilegales en `actions()` o en `result()`? **Ambos diseños son
   legítimos.** Elige uno y prepárate para *defenderlo* en la demostración: esa
   argumentación es la habilidad central de la semana. *La mitad de la IA aplicada consiste en elegir una buena
   representación antes de escribir cualquier algoritmo.*

Se evalúa la formulación, no solo el código.

## Tarea 2 — Implementa los cuatro algoritmos (25 min)

En el mismo `starter.py`, completa `bfs`, `dfs`, `ucs` e `ids`.

Tres de ellos requieren **una línea cada uno**: esa es la idea de la semana. BFS, DFS
y UCS son el *mismo* bucle `search()` con distinta disciplina de frontera:

| Algoritmo | `frontier_kind` | ¿Completo? | ¿Óptimo? | Espacio |
|---|---|---|---|---|
| BFS | `"fifo"` | Sí | **solo** con costos uniformes | O(b^d) |
| DFS | `"lifo"` | Espacios finitos con control de ciclos | No | O(bm) |
| UCS | `"priority"` | Sí | **Sí** (costos no negativos) | O(b^(1+⌊C\*/ε⌋)) |
| IDS | profundidad limitada, repetida | Sí | solo con costos uniformes | **O(bd)** |

`ids` es el interesante y **no** llama a `search()`. Escribe una función recursiva
`depth_limited(problem, limit)` que devuelva `(node, expansions, hit_limit)` y luego
aumenta el límite desde 0. IDS obtiene la completitud de BFS con el consumo de memoria de DFS
repitiendo el trabajo de los niveles superficiales. La redundancia es un *factor constante*, no
exponencial (≈11 % con b≈10). Es un costo bajo.

Después ejecuta:

```bash
python3 test_search.py
```

Las cinco pruebas deben pasar. Lee con atención
`test_bfs_suboptimal_nonuniform_cost`: **comprueba que BFS devuelve el camino incorrecto de
costo 10** en `TinyGraph`. La prueba no está defectuosa. La optimalidad de BFS tiene una
condición: costos uniformes por paso. Esta instancia la incumple. Una garantía cuyo fallo no puedes
observar es una garantía que no has comprendido. Las otras cuatro:

- `test_bfs_optimal_uniform_cost` — en el rompecabezas de 8 fichas, cada movimiento cuesta 1 y BFS *sí es* óptima.
- `test_dfs_terminates_on_cyclic_graph` — DFS en un ciclo de 3 nodos **termina** solo
  porque `search()` mantiene un conjunto de explorados. Si lo eliminas, la búsqueda no termina.
- `test_ucs_optimal_nonuniform_cost` — UCS devuelve el camino de costo 2 en `TinyGraph`. Esta
  es *la razón por la que existe UCS*.
- `test_ids_matches_bfs_solution_length` — IDS encuentra una solución de la misma longitud que BFS
  con memoria O(bd).

## Tarea 3 — Mide (10 min)

Ejecuta los cuatro algoritmos sobre el banco proporcionado: profundidades 4, 8, 12 y 16, con diez instancias
por profundidad. `starter.measure()` proporciona el bucle. Produce:

- **Tabla:** expansiones y longitud de la solución; puedes añadir el tamaño máximo de frontera y el tiempo real.
- **Gráfica:** expansiones frente a profundidad, con **eje y logarítmico**.

La gráfica logarítmica es *el* entregable. Las líneas rectas en un eje logarítmico indican
crecimiento exponencial: verlo en tus propios datos permite comprender por fin la encuesta
inicial. Nunca escribas una búsqueda sin el contador `expansions`: es la única
unidad con la que se pueden comparar estos cuatro algoritmos (eje 3 de la ficha de evaluación).

## Demostraciones (20 min)

Dos parejas. Una presenta la **discrepancia de formulación** de la tarea 1 (`actions()`
frente a `result()`: pide que defiendan su elección). Otra presenta la **gráfica de escalabilidad**. Sobre la
gráfica, pregunta: *extrapola a profundidad 24; ¿será suficiente tu portátil?* (No. Por eso
existe la semana 4.)

## Puesta en común (10 min)

- La búsqueda no informada es **completa, pero ciega**. Todas nuestras garantías cuestan
  recursos exponenciales.
- DFS *encontró* un objetivo en las instancias profundas: uno terrible, a cientos de movimientos.
  La optimalidad no es un detalle opcional que puedas estimar a simple vista.
- **Esta semana no hay comparación con LLM, deliberadamente:** no puedes evaluar a un competidor
  hasta poder medir el sistema de referencia. La semana 4 será el primer duelo.
- Conserva este código. La próxima semana añade una heurística y A\* requiere cambiar unas 10 líneas.

> **Entrega de la entrada del Atlas de Fallos.** Los fallos clásicos cuentan: una explosión exponencial es un
> fallo que merece documentarse.

## Enlaces

- Notebook de la sesión 3A — [`../../notebooks/week-03-uninformed-search.ipynb`](../../notebooks/week-03-uninformed-search.ipynb)
- Taller de la semana 4 (A\* sobre esta interfaz) — [`../week-04/`](../week-04/)
- Especificación del duelo 1 (usa `search()`) — [`../../projects/duel-1-search.md`](../../projects/duel-1-search.md)
- Política de IA (`AI_LOG.md`) — [`../../resources/ai-policy.md`](../../resources/ai-policy.md)
