# Taller de la semana 4 — Heurísticas en una cuadrícula con costos de terreno

**Complemento de** [`../../weeks/week-04.md`](../../weeks/week-04.md) — Sesión B.
**Distribución del tiempo:** Repaso 5 · Trabajo en grupos 45 · Demostraciones 20 · Puesta en común 10 (80 min en total).
**Entregables:** todas las pruebas proporcionadas superadas y una gráfica de escalabilidad para el duelo con el LLM.

> **Actividad inicial (5 min).** *¿Por qué `h_bad` fue más rápida en el notebook? ¿A qué costo?*

## Archivos de esta carpeta

| Archivo | Propósito | ¿Lo editas? |
|---|---|---|
| [`gridworld.py`](gridworld.py) | Proporcionado: el motor A* y el problema de cuadrícula con costos de terreno, sin cambios respecto al notebook | ❌ |
| [`instances.json`](instances.json) | Proporcionado: 40 cuadrículas generadas con semilla fija, 10 de cada tamaño: 5×5, 8×8, 12×12 y 16×16 (semilla 20260807) | ❌ |
| [`starter.py`](starter.py) | **Tarea 1** — completa cuatro heurísticas: tres admisibles y una deliberadamente incorrecta | ✅ |
| [`test_heuristics.py`](test_heuristics.py) | Pruebas proporcionadas, incluida `test_inadmissible_heuristic_returns_suboptimal_path` | ❌ |
| [`duel.py`](duel.py) | **Tarea 2** — verificador, categorías de evaluación y el prompt exacto del plan | ❌ (úsalo) |
| [`_generate_instances.py`](_generate_instances.py) | Regenera `instances.json`; solo es necesario si cambias la semilla | ❌ |

## Tarea 1 — Heurísticas y pruebas proporcionadas (15 min)

Abre `starter.py`. Implementa:

- `h_manhattan` — distancia de Manhattan sin escalar, admisible **aquí** porque `MIN_COST == 1`; pregúntate cuándo deja de ser admisible.
- `h_manhattan_scaled` — Manhattan × `MIN_COST`, la heurística admisible correcta en general.
- `h_euclidean_scaled` — distancia euclidiana × `MIN_COST`, admisible pero menos informada en una cuadrícula con cuatro direcciones de movimiento.
- `h_bad` — **no admisible** deliberadamente. Forma sugerida: `MAX_COST × Manhattan`, es decir, `8 × Manhattan`: sobreestima un camino que pasa principalmente por celdas baratas.

Después ejecuta:

```bash
python3 test_heuristics.py
```

Las cinco pruebas deben pasar. La última, `test_inadmissible_heuristic_returns_suboptimal_path`, es el objetivo: comprueba que `h_bad` rompe la optimalidad en **al menos una** de las 40 instancias. Una prueba que espera un *fallo* no es un error; observar el fallo de una garantía *una vez* permite comprender su importancia.

Para las parejas que terminen pronto: **Si `MIN_COST` fuera 2 en lugar de 1, ¿seguiría siendo admisible Manhattan sin escalar? ¿La dominaría `h_manhattan_scaled`?** Deben poder explicar por qué en una oración.

## Tarea 2 — El duelo: LLM frente a A* (25 min)

Dale al LLM las mismas cuadrículas que A* acaba de resolver. `duel.py` contiene el prompt exacto del plan y un verificador que clasifica cada respuesta en **cuatro categorías**; no las confundas:

1. **illegal** — el camino sale de los límites o no es contiguo.
2. **suboptimal** — el camino es legal, pero su costo total supera el óptimo de A*.
3. **wrong_cost** — el camino es legal y óptimo, pero el costo declarado por el modelo es incorrecto (⚠️ esta es la categoría interesante).
4. **correct** — se cumplen las tres condiciones.

**Protocolo del plan, obligatorio para obtener una curva de escalabilidad válida:**

- **Cuatro tamaños:** 5×5, 8×8, 12×12 y 16×16, con 10 instancias de cada uno.
- Evalúa cada respuesta con `duel.score_llm_reply()`. **No** creas el costo declarado por el modelo: vuelve a calcularlo con el verificador.
- Si usas el backend manual, limita el trabajo a **5 instancias por tamaño** e indícalo (eje 6 de la ficha de evaluación).

Esquema:

```python
from aicourse.llm import LLM   # o tu propio cliente local
from duel import prompt_for, parse_reply, score_llm_reply
from gridworld import load_instances

model = LLM()  # el backend que hayas configurado
bank = load_instances()
rows = []
for size in [5, 8, 12, 16]:
    for grid in bank[size]:
        reply = model.complete(prompt_for(grid))
        path, cost = parse_reply(reply)
        rows.append((size, score_llm_reply(grid, path, cost).category))
```

**Tarea 3 — Gráfica (5 min).** Tasa de optimalidad (`correct / n`) frente al tamaño de la cuadrícula. Dos líneas: A* en el 100 % y el LLM descendiendo. Esta gráfica se incluye en el duelo 1.

## Demostraciones (20 min)

- Pide específicamente las gráficas de escalabilidad. La forma característica, A* estable y el LLM con una caída abrupta, se comprende mejor cuando los estudiantes la descubren y ven que se *reproduce* en toda la clase. Tres parejas que muestran la misma caída dejan de ser una anécdota.
- Pregunta: *¿el LLM de alguien devolvió un camino más corto que el óptimo de A*?* Si ocurrió, es **illegal** o **wrong_cost**: una oportunidad de depurar en vivo.

## Puesta en común (10 min)

- A* es óptima **porque** se cumple una propiedad demostrable. `h_bad` permite observar deliberadamente el fallo de esa propiedad.
- El LLM no tiene esa propiedad. Su desempeño es un promedio empírico sobre tu distribución y no dice nada sobre la instancia n.º 31.
- Mala práctica que debes señalar: **usar el modelo como su propio oráculo** («¿parece correcto tu camino?»). Valida siempre con el verificador. Corresponde al eje 3 de la ficha de evaluación.
- **El duelo 1 ya está disponible.** Consulta [`../../projects/duel-1-search.md`](../../projects/duel-1-search.md).

## Enlaces

- Notebook de la sesión A — [`../../notebooks/week-04-astar-heuristics.ipynb`](../../notebooks/week-04-astar-heuristics.ipynb)
- Especificación del duelo 1 — [`../../projects/duel-1-search.md`](../../projects/duel-1-search.md)
- Ficha de evaluación del duelo — [`../../resources/duel-scorecard.md`](../../resources/duel-scorecard.md)
- Política de IA (`AI_LOG.md`) — [`../../resources/ai-policy.md`](../../resources/ai-policy.md)
