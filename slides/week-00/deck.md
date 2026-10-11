---
marp: true
theme: default
paginate: true
header: 'CMP-4004 · Semana 0 · Preparación'
---

<!--
==============================================================================
SEMANA 0 — A TU PROPIO RITMO. ESTA PRESENTACIÓN ES PARA QUE LOS ESTUDIANTES LA LEAN SOLOS.
A diferencia de las presentaciones 01-14, esta NO es el guion de una mini clase. No hay una sesión en vivo
detrás de ella: la sesión A de la semana 1 es programa + presentaciones, y la sesión B es asincrónica
(el instructor estará viajando). Por eso, esta presentación está escrita en segunda persona, para
leerse sin narrador, y luego te dirige al notebook para realizar el trabajo.
Compártela como PDF o HTML antes de que comience el semestre.
Notebook: ../../notebooks/week-00-programming-with-llms.ipynb
Plan de la lección: ../../weeks/week-00.md
==============================================================================
-->

# Semana 0 — Preparación

## Programar *con* un LLM, no chatear con uno

**CMP-4004** · a tu propio ritmo · haz esto antes de nuestra primera clase

---

# Qué hace este curso

Durante catorce semanas construirás un algoritmo clásico de IA y luego **lo medirás
frente a un LLM realizando la misma tarea.**

| | |
|---|---|
| Semanas 3–11 | búsqueda, lógica, planificación, optimización — **con demostraciones** |
| Semanas 12–14 | probabilidad, modelos de secuencia, redes neuronales |
| **Cada semana** | **una comparación medida y una ficha de evaluación** |

El material clásico **no es historia**. Es el **grupo de control.**

> ## Este no es un curso anti-LLM ni un curso de exageración sobre los LLM.
> ## Es un curso sobre saber qué puedes demostrar.

---

# Por qué existe la Semana 0

La comparación solo tiene valor si **la parte del LLM se hace correctamente.**

| Chatear con un modelo | Programar con uno |
|---|---|
| interactivo | **por lotes** |
| tolerante | **analizado y validado** |
| irreproducible | **almacenado en caché y con semilla fija** |
| una respuesta | **120 instancias y una curva** |

Vas a poner números en un informe que alguien cuestionará. La Semana 0 es
donde construyes la infraestructura que hace que esos números sean defendibles.

**Tiempo estimado: 90–120 minutos, más el tiempo de descarga.**

---

# Lo que necesitas (y lo que *no*)

## Requerido

- **Python 3.10+** y aproximadamente 15 minutos de `pip install`
- Cualquier laptop. **4 núcleos y 8 GB de RAM son suficientes.**

## ⚠️ NO se requiere — nunca, para obtener la calificación completa

- Una GPU
- Una clave API pagada
- Una cuenta en la nube
- Una tarjeta de crédito

Cada laboratorio de este curso funciona en la máquina razonablemente más débil. Eso es una restricción
de diseño, no una aspiración.

---

# Tres backends de LLM. El tercero siempre funciona.

| Backend | Qué necesita | Velocidad |
|---|---|---|
| **`ollama`** | ~2 GB de descarga, 4 GB de RAM libre | 5–20 tokens/s en CPU |
| **`api`** | tu propia clave, si resulta que tienes una | rápido |
| **`manual`** | **cualquier interfaz de chat, en cualquier lugar** | lento pero universal |

## `LLM backend: manual` es APROBADO

Si Ollama no se instala en tu máquina, **no estás atrasado.** Pegarás
prompts en una ventana de chat, ejecutarás benchmarks más pequeños, indicarás el *n* reducido en tu
informe y **no perderás puntos por ello.**

Pide ayuda pronto si estás atascado. Un problema publicado el jueves le toma quince
minutos a alguien.

---

# Por qué un modelo local *pequeño* es mejor aquí

`qwen2.5:3b` no es muy bueno. **Ese es el punto.**

- Sus fallos son **frecuentes**, **visibles** e **instructivos**
- Cuando un modelo 3B fabrica una ruta A\* inválida, la lección queda clara
- Cuando un modelo de frontera lo hace correctamente, lo hace por razones que **no puedes
  inspeccionar** — y no aprendes nada sobre *por qué*

> ## Estás estudiando los modos de fallo de una clase de sistema.
> ## Un sistema que rara vez falla es un mal espécimen.

---

# ⚠️ La parte difícil: la prosa no son datos

Un LLM devuelve **texto**. Tu experimento necesita un **número**.

Las diez siguientes son respuestas razonables a *"what is 2+2?"*:

```
4                                    Four.
The answer is 4.                     ```\n4\n```
4.0                                  The answer is 4. Let me explain...
**4**                                Sure! 42 is the answer? No — 4.
I think it's 4, but it depends       (empty string)
```

`int(text.strip())` maneja **una** de ellas.

La brecha entre prosa y datos es donde viven los **errores silenciosos de medición** — y
el notebook hace que los experimentes antes de que puedan costarte una calificación.

---

# La solución, en orden de prioridad

## 1 · Restringe el formato en el prompt

La opción más barata y efectiva. `"Reply with exactly: ANSWER: <number>"`

## 2 · Analiza de forma defensiva

Devuelve `(value, failure_mode)`. Ten un resultado explícito de **"no se pudo analizar"**.

## 3 · ⚠️ Nunca hagas coerción silenciosa

> Un `None` que **contaste** es un punto de datos.
> Un `0` que **inventaste** es una mentira en tu tabla de resultados.

### El caso que más enseña

`"42 is the answer to 2+2? No — 4."` → dos números, sin marcador.

Los analizadores del primer número y del último número **no coinciden**, y ambos son suposiciones disfrazadas de
mediciones. La respuesta honesta es `ambiguous`, y pertenece a tu
columna de **modo de fallo**, no a tu columna de precisión.

---

# La caché no es una optimización

Cada llamada se almacena, con una clave `SHA-256(backend, model, prompt, temperature, seed)`.

| Razón | Por qué forma parte del contenido del curso |
|---|---|
| **Reproducibilidad** | una afirmación evaluada debe poder volver a derivarse |
| **Costo** | reescribirás tu análisis diez veces; la inferencia es lenta |
| **Honestidad** | hace que *"ejecutamos 30 instancias"* sea **verificable** |

## Haces commit de `.llm_cache/` en tu repo

Son **datos crudos**, no salida de compilación. Es la evidencia detrás de tus afirmaciones.

---

# ⚠️ Tu parser forma parte de tu experimento

Dos formas de hacer trampa accidentalmente, ambas comunes y ambas fáciles de evitar:

## Ajustar el parser hasta que el LLM se vea bien

Entonces has medido **tu parser**. Escríbelo *antes* de ver los resultados y
reporta cuántas salidas no pudo analizar.

## Probar cuatro prompts y reportar el mejor

Eso es **p-hacking**. Procedimiento legítimo:

1. Elige tu prompt usando un pequeño **conjunto de desarrollo**
2. **Congélalo**
3. *Luego* ejecuta el benchmark
4. Indica en el informe qué prompt usaste y cómo lo elegiste

**Da a ambos lados el mismo cuidado.** Una hora ajustando el prompt y una heurística
por defecto no es una comparación justa.

---

# El verificador — la verdadera lección de hoy

Tu primera comparación es **ordenar una lista de enteros**: trivial de forma clásica,
**exactamente verificable** y escalable.

El verificador comprueba tres cosas **por separado**:

| Comprobación | Modo de fallo | Qué significa |
|---|---|---|
| se puede analizar | `malformed` | la salida no era una lista |
| mismo multiconjunto | `invalid` | **eliminó o inventó números** |
| no decreciente | `wrong-but-confident` | números correctos, orden incorrecto |

Agrupar todo esto como "incorrecto" elimina la parte más interesante de tus
datos. Un modelo que elimina un elemento tiene un problema **diferente** al de uno que
ordena mal.

---

# ⚠️ Prueba el verificador antes de confiar en él

El notebook lo verifica con cinco casos cuyas respuestas se conocen **antes** de usarlo
sobre una sola salida del modelo.

> ## Un verificador roto no se bloquea.
> ## Produce silenciosamente un número plausible que luego publicas.

Encontrarás exactamente esta misma lección dos veces más:

| Semana | El verificador |
|---|---|
| **0** | tu comprobador de ordenamiento |
| **9** | un validador de planes correcto — *la piedra angular del curso* |
| **14** | comprobación de gradientes de tu propia retropropagación |

---

# El patrón que usarás catorce veces

```
        ┌─────────────┐
        │  instances  │   several sizes, fixed seed
        └──────┬──────┘
      ┌────────┴────────┐
      ▼                 ▼
┌───────────┐    ┌─────────────┐
│ classical │    │ LLM + parse │  ← prose becomes data here
└─────┬─────┘    └──────┬──────┘
      └────────┬────────┘
               ▼
        ┌─────────────┐
        │  VERIFIER   │  ← sound, tested, trusts nobody
        └──────┬──────┘
               ▼
   scorecard + scaling curve + honesty section
```

Cada duelo es este diagrama con una caja diferente en el medio.

---

# Un punto no es una curva

La ficha de evaluación tiene ocho ejes. **El eje 6 es donde este curso hace énfasis.**

```
solve rate
  100% |●———●———●———●     ← classical (flat: cost grows, correctness doesn't)
       |     ○———○
   50% |          ╲○
       |            ╲
    0% |              ○   ← LLM (the cliff)
       +——————————————————
        4    8   12   16    problem size
```

**Mínimo para cada duelo: cuatro tamaños de problema, diez instancias cada uno.**

Si tu gráfico **no** muestra un precipicio, ese es un resultado interesante — pero debes mostrar
el gráfico.

---

# El eje que los estudiantes subestiman

## Eje 2 — Garantía

Estas **no** son el mismo tipo de afirmación:

> `sorted()` devuelve una permutación de su entrada en orden no decreciente, para
> **toda** entrada, en O(n log n). **Sin condición.**

> El LLM produjo un ordenamiento correcto en 12/20 instancias.
> **No se hace ninguna afirmación sobre la número 21.**

Distinguir estas dos cosas es el tema completo de este curso.

Expresa cada garantía como una **condicional**: *A\* es óptimo **siempre que** `h` nunca
sobreestime.*

---

# Evaluamos el experimento, no el veredicto

| Puntuación | Significado |
|---|---|
| 0 | no abordado |
| 1 | afirmado ("fue más rápido") |
| 2 | medido una vez |
| 3 | medido en varias instancias, con una estadística |
| 4 | **en varias instancias *y* tamaños, con varianza y una limitación indicada** |

> ## Un estudio cuidadoso que concluya "el LLM ganó" obtiene mayor puntuación que un estudio descuidado
> ## que concluya "ganó el método clásico."

### Y cada informe tiene una sección titulada *"Where we may have been unfair"*

Da puntos reales. **Un estudiante que encuentra una falla genuina en su propio
experimento ha aprendido lo que este curso realmente está enseñando.**

---

# Tu entrega de la Semana 0

En `week00/` de tu repo del curso, antes de nuestra primera clase:

| # | Archivo | Qué |
|---|---|---|
| 1 | `doctor.txt` | salida de `python -m aicourse.doctor` |
| 2 | `first_comparison.md` | tu tabla + ficha de evaluación, **los cuatro TODO completados** |
| 3 | *(foro)* | **una** entrada en el Failure Atlas, en el formato requerido |
| 4 | *(foro)* | **una** respuesta a un compañero, mencionando algo específico |
| 5 | `AI_LOG.md` | iniciado — ¿usaste un asistente? regístralo. Está permitido. |

Poco puntaje. Principalmente significa que **tu cadena de herramientas funciona antes de que importe**, y
nunca gastamos tiempo del laboratorio en problemas de `PATH`.

---

# Formato de entrada del Failure Atlas

Copia esta estructura exactamente. Escribirás una cada semana.

```markdown
### [Wk0] LLM drops an element when sorting 40 integers
**Setup:** qwen2.5:3b, temp 0, "reply with only the sorted list"
**Classical:** sorted() — correct, O(n log n), 0.00002 s
**LLM:** returned 39 of the 40 numbers, correctly ordered.
  Missing: 491. No hedging, no mention of uncertainty.
**Category:** invalid
**Why it matters:** The output LOOKS right. Sorted order is the thing you'd
  eyeball, and it was fine — only a multiset check catches this. Any pipeline
  consuming this output silently loses data.
```

**"Why it matters" es la parte que cuenta.** Una oración: ¿qué se rompería si
lo pusieras en producción?

---

# Si algo está roto

| Síntoma | Solución |
|---|---|
| `ModuleNotFoundError: aicourse` | ejecuta Jupyter desde `course-en/`, o `pip install -e .` |
| ollama: `connection refused` | `ollama serve` en otra terminal |
| ollama: `model not found` | `ollama pull qwen2.5:3b` (o `:1.5b` si tienes ≤ 8 GB de RAM) |
| insoportablemente lento | usa `:1.5b`; reduce las instancias; la caché significa que pagas **una vez** |
| nada funciona | `LLM(backend="manual")` — **una opción compatible** |

## Pide ayuda pronto

Un problema de la cadena de herramientas publicado el **jueves** le toma a alguien quince minutos.
El mismo problema a las **11 pm antes del Duelo 1** te cuesta una calificación.

---

# Empieza la descarga del modelo *ahora*

`qwen2.5:3b` ocupa aproximadamente **2 GB**.

No esta noche. No antes de clase. **Ahora**, mientras lees el resto de esto.

```bash
ollama pull qwen2.5:3b
```

---

# Lo que viene

## Sesión 1A — ¿Qué es la inteligencia?

El artículo de Turing de 1950, la historia que dio origen a este campo y **ELIZA en 40 líneas
de Python**. Un programa de 1966 sin un modelo de nada, que resulta inquietantemente
convincente — y que luego romperás a propósito.

## Sesión 1B — asincrónica

Tus publicaciones del foro de la Semana 0. Detalles en el anuncio.

---

# Lleva una cosa a la Sesión 1A

> # ¿Cuál ganará más de los catorce duelos: el algoritmo clásico o el LLM?

**Escribe tu respuesta.** Comprométete con un número.

Lo revisaremos en la **semana 14**, junto a la predicción sellada que escribirás en
la Sesión 1A.

> ## Estar equivocado en público, dejarlo registrado y tener datos — ese es el trabajo.

<!--
Establece aquí el tono deliberadamente. Los estudiantes llegan esperando una clase anti-IA
o una clase de exageración pro-IA. Ninguna de las dos se ofrece, y decirlo en la semana 0
evita dos tipos diferentes de desconexión.
-->
