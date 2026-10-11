---
marp: true
theme: default
paginate: true
header: 'CMP-4004 · Semana 3 · Formulación de problemas y búsqueda no informada'
---

<!--
Semana 3, sesión A. Tiempo para la miniclase: 25 minutos.
Fuente: 02_Problem.pptx, diapositivas 1-10. Etapas según el plan de clase:
formulación (8) → grafo frente a árbol (7) → criterios (5) → algoritmos (5).
Plan de clase: ../../weeks/week-03.md
-->

# Resolución de problemas

## Formulación, espacios de estados y búsqueda ciega

**CMP-4004** · Semana 3

![bg right:35%](images/slide01-1.jpeg)

---

# Agentes que resuelven problemas

![bg right:38%](images/slide02-1.png)

Un **agente basado en objetivos** que planifica una secuencia de acciones para lograr su objetivo.

Opera en modo **buscar y después ejecutar**:

1. **Formular** el problema — *¿cuál es exactamente el problema?*
2. **Buscar** una secuencia de acciones que alcance el objetivo — *¿cuál es la mejor forma?*
3. **Ejecutar** el plan resultante

Supone un entorno **observable, determinista, discreto y estático**.

> La solución siempre es una **secuencia** de acciones, no una única acción.

<!--
Conecta explícitamente con la semana 2: este es el agente basado en objetivos de la
clasificación, y esas cuatro suposiciones corresponden a cuatro de los seis ejes fijados en su
caso sencillo. Cada semana posterior relaja una de ellas.
-->

---

# Formulación del problema: cinco componentes

![bg right:32%](images/slide03-1.jpeg)

| Componente | Definición |
|---|---|
| **Estado inicial** | El estado del que parte el agente |
| **Acciones** | El conjunto de acciones disponibles en cada estado |
| **Modelo de transición** | El resultado de aplicar una acción: `Result(s, a) → s'` |
| **Prueba de objetivo** | Una condición que determina si un estado es el objetivo |
| **Función de costo** | Costo numérico de cada acción; **define la calidad de la solución** |

Juntos definen el **espacio de estados**.

---

# La formulación es una decisión de diseño

## El rompecabezas de 8 fichas, de dos maneras

| | «Mover la ficha» | «Mover el espacio vacío» |
|---|---|---|
| Acciones | 4 direcciones × 8 fichas | arriba/abajo/izquierda/derecha sobre un espacio vacío |
| Factor de ramificación | hasta 32 nominales | **2–4** |
| ¿Mismo rompecabezas? | sí | sí |
| ¿Mismo costo de búsqueda? | **no: muy diferente** | |

> **La mitad de la IA aplicada consiste en elegir una buena representación antes de escribir cualquier
> algoritmo.**

<!--
8 min para la formulación, incluida esta diapositiva. Trabaja el rompecabezas de 8 fichas y la búsqueda de rutas
en paralelo; después haz esta comparación. Esta diapositiva justifica la tarea 1 del
taller, donde los estudiantes formulan el problema de misioneros y caníbales y discrepan sobre
dónde imponer las restricciones.
-->

---

# Espacio de estados

![bg right:35%](images/slide04-1.png)

El conjunto de todos los estados alcanzables desde el estado inicial mediante **cualquier** secuencia
de acciones.

Se representa como un **grafo**:

- Los **nodos** son estados del mundo
- Las **aristas** son acciones que permiten transitar entre estados
- Cada arista tiene un **costo** asociado

**Nunca se construye explícitamente**: en la práctica es demasiado grande. El agente
lo explora progresivamente durante la búsqueda.

---

# *Grafo* de estados frente a *árbol* de búsqueda

![bg right:40%](images/slide05-1.png)

| **Grafo de estados** | **Árbol de búsqueda** |
|---|---|
| Representa el **problema** | Representa el **proceso de búsqueda** |
| Cada estado aparece **una vez** | El mismo estado puede aparecer **muchas veces**, una por cada camino que llega a él |
| Finito (si el espacio es finito) | **Puede ser infinito incluso si el grafo es finito** |

Un grafo con un ciclo produce un árbol infinito. Expandirlo tres niveles a mano
lo hace evidente de una forma que la oración por sí sola no logra.

---

# Los estados repetidos no se detienen por sí solos

![bg right:35%](images/slide05-2.png)

Al expandir el árbol de búsqueda, el mismo estado puede generarse por
múltiples caminos, lo que causa **ciclos infinitos** si no se controla.

**Solución: mantener dos estructuras.**

- **Frontera** — estados generados, pero aún no explorados
- **Conjunto de explorados** — estados ya expandidos que no vuelven a generarse

Sin control de estados repetidos, el algoritmo **puede no terminar aunque exista una
solución.** Con control, cada estado se explora como máximo una vez.

<!--
7 min para las diapositivas de grafo y árbol. Recorre un ciclo real en la pizarra. No dejes que
quede como algo abstracto: la prueba correspondiente de pytest es
test_dfs_terminates_on_cyclic_graph y falla realmente cuando omiten este control.
-->

---

# Búsqueda no informada

![bg right:32%](images/slide06-1.png)

Búsqueda **ciega**: el agente **no** tiene información sobre qué estados son más
prometedores.

Solo conoce:

- el estado inicial
- las acciones disponibles
- la prueba de objetivo

Explora el espacio **sistemáticamente**, sin favorecer ningún camino. Los algoritmos difieren
*solo* en el **orden en que expanden los nodos**.

---

# Cuatro criterios de evaluación

| Criterio | La pregunta | La trampa |
|---|---|---|
| **Completitud** | ¿Garantiza encontrar una solución si existe? | «si existe» |
| **Optimalidad** | ¿Garantiza encontrar la solución de **menor costo**? | casi siempre es **condicional** |
| **Complejidad temporal** | ¿Cuánto tarda? | se mide en **expansiones**, no en segundos |
| **Complejidad espacial** | ¿Cuánta memoria requiere? | suele ser la restricción limitante |

### Dilo con precisión

BFS es óptima **cuando los costos de cada paso son uniformes**, *no* en general.

<!--
5 min. Insiste en la condición. El punto de control 1 pide que los estudiantes indiquen qué
garantiza una técnica Y bajo qué condición; afirmar «BFS es óptima» sin precisar la condición
obtiene cero puntos, y deben escucharlo ahora.
-->

---

# Búsqueda en anchura

![bg right:38%](images/slide07-1.png)

Expande primero los nodos **menos profundos**, nivel por nivel.
**Frontera: cola FIFO.**

- **Completa** — siempre encuentra una solución si existe
- **Óptima** — menor número de pasos, *cuando los costos son uniformes*
- Tiempo: **O(bᵈ)**
- Espacio: **O(bᵈ)** ← la frontera crece exponencialmente con la profundidad

La memoria, no el tiempo, es lo que hace inviable BFS.

---

# Búsqueda en profundidad

![bg right:38%](images/slide09-1.png)

Expande primero los nodos **más profundos**, siguiendo una rama hasta el final.
**Frontera: pila LIFO.**

- **Completa** — *solo* si se controlan los estados repetidos y el espacio es finito
- **No es óptima** — no garantiza el camino más corto
- Tiempo: **O(bᵐ)**
- Espacio: **O(b·m)** ← la razón por la que se utiliza

---

# Los cuatro algoritmos en una tabla

| Algoritmo | Frontera | ¿Completo? | ¿Óptimo? | Tiempo | Espacio |
|---|---|---|---|---|---|
| **BFS** | cola FIFO | Sí | solo con costos uniformes | O(bᵈ) | **O(bᵈ)** |
| **DFS** | pila LIFO | espacios finitos con control de ciclos | No | O(bᵐ) | **O(bm)** |
| **UCS** | cola de prioridad según `g(n)` | Sí | **Sí** | O(b^(1+⌊C*/ε⌋)) | igual |
| **IDS** | LIFO, profundidad limitada | Sí | solo con costos uniformes | O(bᵈ) | **O(bd)** |

### La idea central

BFS tiene la garantía, pero consume memoria. DFS es económica, pero no tiene garantía.
**IDS obtiene la garantía de BFS con el consumo de memoria de DFS, a cambio de repetir trabajo.**

Para b = 10, d = 5, el sobrecosto de volver a expandir es aproximadamente **11 %**. Bajo.

<!--
5 min. Calcula el 11 % en la pizarra: sorprende a la gente y
justifica que la profundización iterativa sea la opción habitual en la búsqueda para juegos (semana 5).
-->

---

# A continuación: programación en vivo

## Una función de búsqueda, cuatro algoritmos

La única diferencia es la estructura de datos de la frontera.

**Dos cosas que haremos mal deliberadamente al principio:**

1. Aplicar la prueba de objetivo al **generar** en lugar de expandir → rompe la optimalidad de UCS.
   Construimos en vivo el contraejemplo de 3 nodos.
2. No contar las expansiones → nada que comparar. **Nunca escribas una búsqueda sin un
   contador.** Corresponde al eje 3 de la ficha de evaluación.

<!--
El código está en ../../weeks/week-03.md. La función de búsqueda genérica es el
recurso más reutilizado del curso: las semanas 4, 5, 6 y 9 se construyen sobre ella.
Esta semana no habrá comparación con un LLM, deliberadamente: no puedes evaluar a un competidor
hasta poder medir al sistema de referencia. Dilo en la puesta en común.
-->
