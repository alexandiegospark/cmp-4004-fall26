# Taller de la semana 1 — ELIZA frente al primer contacto con un modelo real


**Entregables:** todas las pruebas proporcionadas superadas; `eliza.py` ampliado con un fallo documentado; `first_contact.md` con ambas transcripciones y tres respuestas.

> **Repaso (5 min), con preguntas a estudiantes elegidos sin previo aviso.** *¿Por qué sustituyó Turing la pregunta «¿pueden pensar las máquinas?» y con qué la reemplazó?* (Respuesta que debes preparar: con un juego operativo y comprobable, el juego de imitación, porque la pregunta original es «demasiado carente de sentido como para merecer discusión».)

## Archivos de esta carpeta

| Archivo | Propósito | ¿Lo editas? |
|---|---|---|
| [`eliza.py`](eliza.py) | Proporcionado: el motor de ELIZA, igual que en el notebook de la sesión A (6 reglas, mapa de sustitución de pronombres y respuestas por defecto) | ❌ |
| [`prompts.json`](prompts.json) | Proporcionado: las entradas exactas del notebook. La conversación de demostración, los cuatro casos de prueba de fallos y el conjunto `first_contact` sin duplicados | ❌ |
| [`starter.py`](starter.py) | **Tarea 1:** añade tres reglas, una función de respuesta ampliada y un caso de fallo declarado | ✅ |
| [`test_eliza.py`](test_eliza.py) | Pruebas proporcionadas, incluida `test_declared_failure_is_hollow` (observa cómo falla una garantía) | ❌ |

Archivos nuevos que creas **tú**: `first_contact.md` (tarea 2) y `week01/eliza.py`, que debes guardar en un commit (documentación de la tarea 1).

## Tarea 0: Confirma tu backend (2 min)

Escribe una línea en el canal compartido: **¿qué backend usa tu pareja de trabajo: `ollama`, `api` o `manual`?**

```bash
python -m aicourse.llm --list-backends
```

## Tarea 1: Amplía ELIZA y ejecuta las pruebas proporcionadas (13 min)

Abre `starter.py`. Completa los tres TODO:

- `new_rules():` devuelve **al menos 3 reglas nuevas** `(pattern, [templates])`, con la misma estructura que `eliza.RULES`. No repitas patrones del motor base ni uses patrones que coincidan con una cadena vacía.
- `extended_respond(text):` aplica primero las reglas base, después las nuevas y finalmente una respuesta por defecto. Reutiliza `eliza.reflect` para sustituir los pronombres; no la vuelvas a implementar.
- `failure_case():` devuelve `(input_text, why_it_fails)` para **un fallo deliberado**: una oración compuesta `"<cláusula A> and <cláusula B>"` a la que ELIZA responda con fluidez mientras omite por completo la cláusula B. Conserva `and` en inglés para que la prueba reconozca la separación.

Después ejecuta:

```bash
python3 test_eliza.py
```

Las cinco pruebas deben pasar. Dos de ellas comprueban un *fallo*:

- `test_base_eliza_ignores_second_clause:` demuestra que el motor proporcionado omite la segunda cláusula del ejemplo compuesto del notebook (`"My mother is a doctor and my father is a lawyer"`, es decir, «Mi madre es médica y mi padre es abogado»). La primera coincidencia gana: ELIZA no tiene un modelo del resto de la entrada.
- `test_declared_failure_is_hollow:` exige que el fallo que **tú** declares reproduzca exactamente esa omisión. Una prueba que espera un fallo no es un error; la habilidad que debes adquirir es *predecir* dónde falla ELIZA.

**Guarda en un commit** tu trabajo como `week01/eliza.py`, con una cadena de documentación que describa el fallo (pega la cadena `why_it_fails` de `failure_case()`), tal como solicita el plan.

Para las parejas que terminen pronto: *ELIZA pareció plausible durante unos seis intercambios en la demostración. ¿Cuál de tus tres reglas nuevas resistiría un séptimo intercambio y cuál es la más frágil? Explica por qué en una oración.*

## Tarea 2: Primer contacto; los mismos prompts, dos sistemas (30 min)

Envía las **mismas** entradas a ELIZA y al modelo local. Están en `prompts.json`, bajo `first_contact`; reutilízalas literalmente para que toda la clase compare los mismos fallos.

```bash
python -m aicourse.llm --backend ollama --prompt "I am not feeling great about the exam"
```

Esquema (también aparece en `starter.py`):

```python
import json
from aicourse.llm import LLM
from starter import extended_respond

prompts = json.load(open("prompts.json"))["first_contact"]
llm = LLM(backend="ollama")          # o ejecuta con --backend manual
for p in prompts:
    print("you  >", p)
    print("ELIZA>", extended_respond(p))
    print("LLM  >", llm.complete(p).text, "\n")
```

Registra **ambas** transcripciones en `first_contact.md`. Si usas `manual`, limita el trabajo a los **3** primeros prompts e indícalo. Después responde, con dos o tres oraciones por pregunta:

1. ¿En qué casos el LLM supera **claramente** a ELIZA?
2. Encuentra **una** entrada para la que el fallo del LLM sea *reconociblemente similar al de ELIZA*: una respuesta fluida, pertinente y vacía. Esto es más difícil y es el objetivo.
3. ¿Qué sistema tiene fallos más fáciles de predecir **de antemano**? ¿Por qué importa si debes poner uno de ellos en producción?

## Puesta en común (10 min)

- **Ficha de evaluación del duelo** ([`../../resources/duel-scorecard.md`](../../resources/duel-scorecard.md)). Evalúen juntos y en voz alta a ELIZA frente al modelo local en los ocho ejes.
