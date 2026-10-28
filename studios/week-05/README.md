# Taller de la semana 5 — El torneo de Conecta 4

**Complemento de** [`../../weeks/week-05.md`](../../weeks/week-05.md) — Sesión 5B.
**Distribución del tiempo:** Preparación 10 · Rondas y comentarios 35 · LLM retador 20 · Puesta en común 15 (80 min en total).
**Entregable:** un agente `choose_move` funcional, **entregado 24 h antes de la clase** para realizar una prueba básica.

> **Este taller es diferente.** La sesión 5B *es el torneo*: los 80 minutos
> se dedican a ejecutar y comentar las partidas de todos contra todos e incorporar al
> LLM retador. El agente con el que juegas se construye **antes** de la clase con este material.
> Lee primero «Construye tu agente» y hazlo en casa. Lleva `test_alphabeta.py` con sus pruebas superadas.

## Archivos de esta carpeta

| Archivo | Propósito | ¿Lo editas? |
|---|---|---|
| [`connect4.py`](connect4.py) | Proporcionado: el tablero, `minimax`, `alphabeta`, los órdenes estáticos y la función de enfrentamiento `play`, tomados literalmente del notebook | ❌ |
| [`starter.py`](starter.py) | **Tu agente** — `order_moves` y `choose_move(board, time_budget_ms)` con profundización iterativa | ✅ |
| [`test_alphabeta.py`](test_alphabeta.py) | Pruebas proporcionadas, incluidas las dos pruebas de *garantías* | ❌ |

## Construye tu agente en casa, antes de la sesión 5B

El torneo exige una interfaz y una restricción estricta:

```python
def choose_move(board, time_budget_ms) -> int: ...
```

**Reglas estrictas del plan:** 500 ms por jugada · sin procesos externos · sin
llamadas de red · sin un libro de aperturas de más de 20 posiciones. Superar el tiempo
permitido en una jugada implica perder la partida.

Abre `starter.py` y completa dos funciones:

- **`order_moves(board)`** — devuelve las columnas legales, de mejor a peor. El mejor caso O(b^(m/2))
  de α-β, que duplica la profundidad alcanzable, solo se obtiene si examinas primero
  las jugadas fuertes. El orden estático que empieza por el centro, `CENTER_FIRST` =
  `[3, 2, 4, 1, 5, 0, 6]`, ya proporcionado, es un buen comienzo.
- **`choose_move(board, time_budget_ms)`** — aplica **profundización iterativa** al
  `alphabeta` proporcionado: busca a profundidad 1, después 2, luego 3, etc.;
  conserva la mejor jugada de la última profundidad *completada* y detente cuando se
  agote el tiempo. El plan lo llama agente *con límite temporal que conserva una respuesta disponible*,
  y suele ser lo que decide el torneo: un agente de profundidad fija desperdicia tiempo
  o pierde por excederlo.

Después ejecuta:

```bash
python3 test_alphabeta.py
```

Las siete pruebas deben pasar. Cinco comprueban tu `choose_move` / `order_moves`:
legalidad, aprovechar una victoria inmediata, bloquear una amenaza inmediata y respetar
el tiempo permitido. Las otras dos usan el motor proporcionado y son el objetivo de la semana;
se explican abajo. Las pruebas que dependen de la plantilla muestran `not implemented yet`
mientras no completes las funciones; es lo esperado.

**Para las parejas que terminen pronto:** la mayor mejora de bajo costo es un orden *dinámico*:
prueba primero la mejor jugada de la iteración anterior. Añade una tabla de transposiciones después.
No compliques la evaluación antes de lograr profundidad: *a esta escala, la profundidad supera
al conocimiento* es un resultado que observarás en las partidas.

## Las dos pruebas de garantías y por qué importan

1. **`test_alphabeta_matches_minimax_value_with_fewer_nodes`** — α-β devuelve el valor
   **idéntico** al de minimax mientras visita **estrictamente menos** nodos.
   En la posición del notebook con dos fichas en la columna central:

   | profundidad | nodos de minimax | nodos de α-β | aceleración |
   |---|---|---|---|
   | 2 | 57 | 45 | 1.3× |
   | 4 | 2,801 | 1,002 | 2.8× |
   | 5 | 19,607 | 4,103 | 4.8× |
   | 6 | 132,179 | 17,030 | 7.8× |

   La poda **no** es una aproximación: descarta solo ramas demostrablemente irrelevantes.
   La misma respuesta, a una fracción del costo.

2. **`test_horizon_effect_shallow_agent_loses`** — observa deliberadamente el *fallo* de una garantía.
   `play(2, 5)` → gana el jugador de profundidad 5; `play(6, 4)` → gana el de profundidad 6.
   El agente menos profundo no comete un error de cálculo: **cada jugada es óptima con respecto
   a su horizonte.** Simplemente no ve una amenaza que se resuelve una media jugada más allá
   de donde dejó de buscar. Ninguna función de evaluación soluciona esto; la profundidad sí.
   En el notebook, `play(5, 5)` también da la victoria al segundo jugador, pero es un *efecto particular*
   de `evaluate()` con igual profundidad, no el efecto horizonte. Por eso la prueba no exige
   ese resultado; pregúntate por qué antes de la clase.

## Sesión 5B — En clase (80 min)

**Preparación (10 min).** El programa de todos contra todos se ejecuta en vivo con el cuadro del torneo en pantalla.
Cada pareja juega contra todas las demás, con ambos colores. Mientras se ejecuta, cada pareja
describe su función de evaluación en 30 segundos.

**Rondas y comentarios (35 min).** Predigan los ganadores antes de cada partida; cuando un
agente pierda, sus autores explican qué ocurrió. Observa tres resultados recurrentes:
un agente *más simple* que busca dos medias jugadas más profundo vence a uno sofisticado;
un agente de profundidad fija agota el tiempo y **pierde por ello**, algo que busca evitar la profundización
iterativa; un agente más fuerte como MAX que como MIN tiene un error de asimetría.

**El LLM retador (20 min).** Un agente LLM entra al torneo con el prompt del plan:
`{board}` se obtiene mediante `Connect4.__str__` y `{legal}`, mediante `legal_moves()`.

```python
from aicourse.llm import LLM
model = LLM()
PROMPT = """Connect-4. You are 'X'. Columns numbered 0-6, left to right.
Board (bottom row last):
{board}
Legal columns: {legal}
Reply with one column number and nothing else."""
reply = model.complete(PROMPT.format(board=str(board), legal=board.legal_moves()))
```

Cabe esperar que haga jugadas legales *la mayor parte* del tiempo: valida y reintenta las restantes;
que **pierda oportunidades de victoria inmediata**, como no elegir la columna 3 cuando gana en ese momento,
porque no está buscando; que no bloquee amenazas inmediatas; y que tarde unas 100 veces más que el agente α-β.
Cada tablero con una victoria inmediata desaprovechada es una entrada del Atlas de Fallos:
registra el estado **exacto** para poder reproducirlo.

**Puesta en común (15 min).** α-β devuelve *exactamente* la respuesta de minimax explorando
mucho menos: la poda no es una aproximación. Ordenar jugadas es una heurística sobre el *orden*
de búsqueda y duplica la profundidad alcanzable. El LLM perdió contra un agente de 40 líneas en
un juego que ha visto miles de veces: **reconocer patrones en la descripción de un juego no equivale
a calcular sus jugadas.** Relaciona ese resultado con Ruoss y colaboradores (2024): ajedrez de nivel
gran maestro sin búsqueda durante la inferencia. La conclusión es que *la búsqueda no desapareció:
se trasladó al entrenamiento.*

## Enlaces

- Notebook de la sesión A — [`../../notebooks/week-05-minimax-alphabeta.ipynb`](../../notebooks/week-05-minimax-alphabeta.ipynb)
- Diapositivas — [`../../slides/week-05/deck.md`](../../slides/week-05/deck.md)
- Plan de clase y reglas del torneo, sección «Tarea» de la sesión 5A — [`../../weeks/week-05.md`](../../weeks/week-05.md)
- Política de IA (`AI_LOG.md`) — [`../../resources/ai-policy.md`](../../resources/ai-policy.md)
