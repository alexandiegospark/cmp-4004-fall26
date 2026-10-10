# Semana 7 Studio — Un agente Wumpus sólido vs. un LLM

**Complemento de** [`../../weeks/week-07.md`](../../weeks/week-07.md) — Sesión B.
**Tiempo estimado:** Repaso 5 · Trabajo en grupos 45 · Demos 20 · Cierre 10 (80 min en total).
**Entregables:** todas las pruebas proporcionadas deben pasar y una tabla comparativa de solidez/completitud para la comparación con el LLM.

> **El Checkpoint 1 es esta semana** (libro cerrado, individual, 80 min, semanas 1–6). Se
> realiza en el *otro* bloque de sesión, no en este studio. Banco y clave de respuestas:
> [`../../projects/checkpoint-1-bank.md`](../../projects/checkpoint-1-bank.md).
> Este studio de la Sesión B corresponde al trabajo de DPLL / Wumpus descrito a continuación.

> **Repaso (5 min).** *Enuncia la identidad: `KB ⊨ α` sii `KB ∧ ¬α` es
> insatisfacible. ¿Por qué nos importa? Porque transforma una pregunta sobre* todos *los modelos
> en una* búsqueda *de uno — eso es lo que convierte a un solucionador SAT en un motor de razonamiento.*

## Archivos en esta carpeta

| Archivo | Propósito | ¿Lo editas? |
|---|---|---|
| [`dpll.py`](dpll.py) | Proporcionado: el solucionador DPLL, `entails` y la física de Wumpus 4×4 — sin cambios respecto al notebook | ❌ |
| [`instances.json`](instances.json) | Proporcionado: los escenarios de percepciones y ejemplos CNF, con los valores exactos del notebook | ❌ |
| [`starter.py`](starter.py) | **Tarea 1** — implementar el paso ASK y el agente sólido (más el deliberadamente no sólido) | ✅ |
| [`test_dpll.py`](test_dpll.py) | Pruebas proporcionadas, incluida `test_reckless_agent_is_unsound` | ❌ |

Tú **no** escribes un solucionador ni una transformación de Tseitin — los helpers de codificación
ya están proporcionados (`wumpus_physics`, `negate_cnf`, `entails`). Dedica tu tiempo al
*agente* y a la *comparación*.

## Tarea 1 — El agente sólido + pruebas proporcionadas (20 min)

Abre `starter.py`. Implementa cuatro funciones, cada una como una capa ligera sobre `entails`:

- `provably_safe(kb, x, y)` — ¿la KB demuestra `¬P(x,y)`? (`KB ⊨ ¬P(x,y)`)
- `provably_pit(kb, x, y)` — ¿la KB demuestra `P(x,y)`?
- `sound_frontier(kb, squares)` — devuelve únicamente las casillas **demostradas** como seguras; el agente
  se mueve solo a estas y devuelve `[]` (no adivina) cuando no se demuestra nada.
- `reckless_frontier(kb, squares)` — el error intencional: moverse a cualquier casilla **no
  demostrada como un pozo**, es decir, tratar UNKNOWN como seguro.

Luego ejecuta:

```bash
python3 test_dpll.py
```

Las seis pruebas deben pasar. La última — `test_reckless_agent_is_unsound` — es el
punto principal: verifica que `reckless_frontier` se mueva hacia una casilla que **no
está demostrada como segura**. Una prueba que espera que un agente *se comporte mal* no es un error;
observar al agente no sólido realizar el movimiento que el agente sólido estructuralmente no puede hacer
es la forma de saber que la solidez es una propiedad real y no una esperanza.

Con las percepciones base — `(1,1)` sin brisa, `(2,1)` con brisa — `(1,2)` es la única
casilla de frontera demostrablemente segura; `(2,2)`, `(3,1)`, `(1,3)` son UNKNOWN. Agrega "sin
brisa en `(1,2)`" y una percepción adicional resuelve dos casillas: `(2,2)` y
`(1,3)` se vuelven **SEGURAS**, y — como la brisa en `(2,1)` debe tener una explicación —
`(3,1)` se convierte en un **POZO demostrado**. Eso es razonamiento monotónico: agregar hechos verdaderos
nunca invalida una conclusión previa. (La semana 12 es donde se abandona esa garantía.)

Parejas que terminan rápido: **el agente queda bloqueado cuando todas las casillas de la frontera son UNKNOWN
(prueba `(4,4)` sin percepciones cercanas). ¿Qué debería hacer?** La lógica te dice qué
se deriva, no qué hacer cuando no se deriva nada. Ten preparada una respuesta de una sola frase —
te la preguntarán en la demo.

## Tarea 2 — El LLM como razonador (20 min)

Dale a un LLM las **mismas percepciones** en lenguaje natural y pregúntale qué casillas son
ciertamente seguras y ciertamente peligrosas. Usa el prompt exacto del plan
([`../../weeks/week-07.md`](../../weeks/week-07.md), Sesión B, Tarea 2):

```text
Estás en una cueva 4x4 en la casilla (1,1). Reglas:
- Una casilla con brisa es adyacente a por lo menos un pozo.
- Una casilla con hedor es adyacente al wumpus.
- Adyacente significa horizontal o verticalmente, no en diagonal.
Observaciones hasta ahora:
  (1,1): sin brisa, sin hedor
  (2,1): brisa, sin hedor
  (1,2): sin brisa, hedor
¿Qué casillas son ciertamente seguras? ¿Cuáles son ciertamente peligrosas?
Para cada respuesta, indica qué observaciones fuerzan tu conclusión.
```

```python
from aicourse.llm import LLM   # o tu propio cliente local
from dpll import kb_from_percepts, load_scenarios
import starter as s

model = LLM()
w = load_scenarios()["wumpus"]
kb = kb_from_percepts(w["base_percepts"])
frontier = [tuple(sq) for sq in w["frontier"]]
truth = set(s.sound_frontier(kb, frontier))   # verdad de referencia: demostradas como seguras
# ... parsea el conjunto "ciertamente seguro" del modelo y compáralo con `truth`
```

**Evalúa según solidez, no precisión** (los tres resultados):

| Resultado | Significado |
|---|---|
| correcto + demostrado | el caso bueno |
| **dice UNKNOWN cuando realmente es UNKNOWN** | ✅ **también es un caso bueno** — humildad epistémica |
| afirma con confianza algo que no puede demostrarse | ❌ **no sólido — el fallo que importa** |

Mide y registra en el Failure Atlas:

- **Tasa de solidez:** de las casillas que llama "ciertamente seguras", ¿cuántas realmente
  lo son (es decir, pertenecen a `sound_frontier`)? *Cualquier* afirmación no sólida es fatal — un agente
  que actúa basándose en ella muere.
- **Tasa de completitud:** de las casillas demostrablemente seguras, ¿cuántas encontró?
- **Justificación inválida, respuesta correcta:** casos donde el razonamiento declarado está roto
  aunque la conclusión sea correcta. Esta es la observación de mayor valor de
  la sesión — una respuesta correcta con razonamiento roto no generaliza a nada.
- **Escala a 5×5 y 6×6.** Observa el precipicio.

**Tarea 3 — Tabla comparativa (5 min).** Enfatiza la solidez. La garantía del agente DPLL
es la solidez: nunca se mueve a una casilla que no esté demostrada como segura. El LLM no tiene
ninguna propiedad de solidez — una diferencia *categórica*, no porcentual.

## Demos (20 min)

- Pide casos **no sólidos pero confiados** — el modelo afirmando seguridad cuando esta no está
  implicada. Tres parejas mostrando el mismo fallo deja de ser una anécdota.
- Luego presiona: *tu agente quedó bloqueado porque nada era demostrablemente seguro — ¿qué
  debería hacer?* Déjalos discutir. Alguien dirá "elige la casilla con menor probabilidad de
  tener un pozo". Respuesta: **esa oración no puede expresarse en lógica proposicional,
  y la semana 12 trata precisamente del lenguaje en el que sí puede expresarse.**

## Cierre (10 min)

- La lógica proporciona **solidez** — una propiedad que se cumple *antes* de ejecutar nada.
- Los errores del LLM reflejan la encuesta inicial: afirma consecuentes y trata
  "hay brisa en alguna casilla adyacente" como "hay brisa en una casilla específica", razonando bien en
  cuadrículas pequeñas y degradándose en las grandes.
- Stechly et al. (2024) predicen exactamente esto: las mejoras de CoT permanecen cerca de los ejemplos
  del prompt y caen a medida que aumenta el tamaño. La misma forma que el precipicio de la semana 4,
  en un dominio diferente.
- Si el LLM de una pareja se niega a comprometerse ("no puedo estar seguro"), ese es un **buen**
  resultado. La fiabilidad que no puedes predecir no es fiabilidad.

## Enlaces

- Notebook de la Sesión A — [`../../notebooks/week-07-dpll-sat.ipynb`](../../notebooks/week-07-dpll-sat.ipynb)
- Banco del Checkpoint 1 — [`../../projects/checkpoint-1-bank.md`](../../projects/checkpoint-1-bank.md)
- Tabla comparativa del Duelo — [`../../resources/duel-scorecard.md`](../../resources/duel-scorecard.md)
- Política de IA (`AI_LOG.md`) — [`../../resources/ai-policy.md`](../../resources/ai-policy.md)
