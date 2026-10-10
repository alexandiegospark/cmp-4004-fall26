---
marp: true
theme: default
paginate: true
header: 'CMP-4004 · Semana 7 · Lógica Proposicional y SAT'
---

<!--
Semana 7 Sesión A. Presupuesto de mini-clase: 25 minutos.
Fuente: 05_Planning.pptx diapositivas 1-9. Ritmo según el plan de clase: agentes con KB (4) →
sintaxis/semántica (5) → la identidad central (6) → reglas de inferencia (5) →
limitaciones (5). EL CHECKPOINT 1 ES ESTA SEMANA. Plan de clase: ../../weeks/week-07.md
-->

# Conocimiento, Razonamiento y Planificación

## Parte 1 — Lógica proposicional y SAT

**CMP-4004** · Semana 7

![bg right:35%](images/slide01-1.jpeg)

---

# ¿Por qué lógica?

![bg right:35%](images/slide02-1.jpeg)

## De la búsqueda al conocimiento

Los agentes de búsqueda tratan los estados como **cajas negras**: no entienden el mundo,
solo **navegan** a través de él.

Un **agente lógico** *representa* explícitamente conocimiento sobre el mundo y
**razona** a partir de él.

### La ventaja

El conocimiento es **reutilizable y generalizable** — una sola regla se aplica a infinitos
casos concretos.

Ninguna tabla de consulta tiene esa propiedad. Ninguna política entrenada indica qué casos cubre.

---

# La base de conocimiento

![bg right:35%](images/slide03-1.jpeg)

Un conjunto de oraciones que el agente **sabe que son verdaderas**, expresadas en un lenguaje formal.

| Operación | Significado |
|---|---|
| **TELL** | agregar nueva información a la KB |
| **ASK** | consultar si algo puede **derivarse** de la KB |

El agente ejecuta un ciclo: **percibir → TELL → ASK → actuar**

- **Inferencia** — el proceso de derivar nuevas oraciones a partir de las existentes
- **Regla de inferencia** — un mecanismo que garantiza que la conclusión es verdadera siempre que
  las premisas lo sean

<!--
4 min para las dos diapositivas anteriores. El contraste con las semanas 3-6 es el punto clave:
un agente de búsqueda NAVEGA por el mundo, un agente lógico lo DESCRIBE y deriva
consecuencias.
-->

---

# El vocabulario — esto debe quedar exactamente claro

![bg right:28%](images/slide04-1.png)

| Término | Definición |
|---|---|
| **Modelo** | una asignación de valores de verdad a **todas** las variables proposicionales — *"una posible forma en que podría ser el mundo"* |
| **Satisfacible** | verdadera en **al menos un** modelo |
| **Insatisfacible** | verdadera en **ningún** modelo |
| **Válida** (tautología) | verdadera en **todos** los modelos |
| **Implicación lógica** `α ⊨ β` | β es verdadera en **todo** modelo en el que α es verdadera |

La **inferencia correcta** garantiza que solo se deriven *consecuencias lógicas* de la KB.

<!--
5 min. Los estudiantes confunden estos conceptos constantemente y el Checkpoint 2 evalúa exactamente
esta tabla. Reforzarla. Preguntar la diferencia entre "válida" y "satisfacible" hasta
que alguien la explique correctamente.
-->

---

# La identidad central

# `KB ⊨ α`  sii  `KB ∧ ¬α` es **insatisfacible**

### Por qué esta es la ecuación más importante de la unidad

| Lado izquierdo | Lado derecho |
|---|---|
| una afirmación sobre **todos** los modelos | una **búsqueda** de un modelo |
| aparentemente requiere revisar todo | una comprobación de satisfacibilidad |
| no es directamente computable | **esto es lo que hace un solucionador SAT** |

La implicación lógica se convierte en satisfacibilidad. Esa transformación es lo que hace posible
el razonamiento automatizado — **y por eso un solucionador SAT es un motor de razonamiento
de propósito general**, no solamente una herramienta para resolver acertijos.

<!--
6 min. DERIVARLO, no solo afirmarlo. Si beta es verdadera en todo modelo de alpha, entonces
no existe ningún modelo donde alpha sea verdadera y beta falsa, por lo que alpha AND NOT-beta
no tiene ningún modelo.
Mostrar ambas direcciones.
-->

---

# Lógica proposicional

![bg right:35%](images/slide05-1.png)

- Una **proposición** es una afirmación que puede ser verdadera o falsa
- Los **símbolos proposicionales** representan hechos sobre el mundo
- Las **oraciones complejas** se construyen utilizando conectores lógicos

`¬` `∧` `∨` `→` `↔`

Ese es todo el lenguaje. Sus limitaciones son la razón por la que existe la semana 8.

---

# Semántica y tablas de verdad

![bg right:35%](images/slide06-1.png)

La **semántica** define cuándo una oración es verdadera en un **modelo** determinado.
Las **tablas de verdad** enumeran todos los modelos posibles.

## La fila que todos se resisten a aceptar: `P → Q`

| P | Q | P → Q |
|---|---|---|
| V | V | **V** |
| V | F | **F** |
| F | V | **V** |
| F | F | **V** |

Es falsa **únicamente** cuando P es verdadera y Q es falsa. Si P es falsa, la implicación
es verdadera **sin importar Q**.

*"Si la Luna es de queso, yo soy el rey de España"* — verdadera.

<!--
Dar el ejemplo de verdad vacua y SEGUIR RÁPIDO. Discutir sobre la implicación material
consume cinco minutos y no convence a nadie. Es una definición.
-->

---

# Reglas de inferencia

![bg right:30%](images/slide08-1.png)

| Regla | Forma |
|---|---|
| **Modus ponens** | `α → β`, `α`  ⟹  `β` |
| **Modus tollens** | `α → β`, `¬β`  ⟹  `¬α` |
| **Eliminación de la conjunción** | `α ∧ β`  ⟹  `α` |
| **Resolución** | `α ∨ β`, `¬β ∨ γ`  ⟹  `α ∨ γ` |

Cada una **preserva la verdad**: si las premisas se cumplen en un modelo, también lo hace la conclusión.

### Y la que *no* es una regla

`α → β`, `β` ⟹ `α` — **afirmación del consecuente.** Esta es la encuesta de calentamiento,
y es inválida.

<!--
5 min. La comprobación de modelos mediante enumeración de tablas de verdad es correcta y completa, pero
O(2^n) — mencionar ese costo, porque DPLL en el bloque de programación en vivo es la respuesta
a ese problema.
-->

---

# Una nota sobre la presentación fuente: redes semánticas

![bg right:38%](images/slide07-1.png)

```
isa(bluebird, bird)        isa(bird, vertebrate)
hassize(bluebird, small)   hascovering(bird, feathers)
hascolor(bluebird, blue)   hasproperty(bird, flies)
```

Observa lo que quiere expresar y no puede expresar aquí:

> *Todo lo que es un ave tiene plumas.*

La lógica proposicional no puede expresar eso. Necesitarías una oración por cada ave.

**Volvemos exactamente a esta KB en la semana 8** y escribiremos la regla de herencia
en una sola línea de Prolog.

---

# Limitaciones de la lógica proposicional

![bg right:32%](images/slide09-1.jpeg)

La lógica proposicional es **decidible** y tiene una semántica clara. También es **poco
expresiva.** No puede representar:

- **Objetos y sus propiedades** — no existe una forma de decir "todos los pozos causan una brisa"
  sin enumerar cada caso
- **Relaciones entre objetos** — "John es el padre de Mary" necesita una proposición diferente
  para cada par
- **Cuantificadores** — "todo animal tiene un corazón" no puede expresarse

Con *n* objetos y relaciones de aridad *k* necesitas **O(nᵏ)** proposiciones.
**No escala.**

**Solución: Lógica de Primer Orden** — objetos, relaciones y cuantificadores. *(Semana 8.)*

<!--
5 min. Hacerlo concreto con Wumpus World: una cuadrícula 4x4 necesita docenas de
proposiciones para decir lo que FOL expresa en una sola línea. La tarea del estudio hace que los estudiantes
experimenten esto manualmente, así que introducir la idea aquí.
-->

---

# Siguiente: programación en vivo — DPLL (1962)

Búsqueda por backtracking sobre asignaciones, con **propagación unitaria**:

- una cláusula con un literal no asignado deja **sin elección** → asígnalo
- esto es el **forward checking** de la semana 6, especializado en dominios booleanos

Estructuralmente es lo mismo que tu solucionador CSP. Observa eso.

## Y la identidad, en código

```python
def entails(kb_clauses, alpha_clauses):
    """KB ⊨ α  sii  KB ∧ ¬α es insatisfacible."""
    return dpll(kb_clauses + negate_cnf(alpha_clauses)) is None
```

**Studio:** un agente de Wumpus World que se mueve únicamente a casillas que puede **demostrar**
que son seguras — luego, las mismas percepciones se entregan a un LLM, evaluado según **corrección lógica**,
no precisión.

<!--
En la KB de Wumpus, el contador muestra que la mayoría de las variables se asignan mediante propagación
con casi ninguna ramificación. La misma lección que en la semana 6: LA INFERENCIA SUPERA A LA BÚSQUEDA.
El límite importante que debe señalarse en el estudio: la lógica te dice qué se deriva, no qué
hacer cuando no se deriva nada. Esa es la motivación para la semana 12.
CHECKPOINT 1 ESTA SEMANA — cubre las semanas 1-6.
-->
