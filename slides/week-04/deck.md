---
marp: true
theme: default
paginate: true
header: 'CMP-4004 · Semana 4 · Heurísticas y A*'
---

<!--
Semana 4, sesión A. Tiempo para la miniclase: 25 minutos.
Fuente: 02_Problem.pptx, diapositivas 11-16. Etapas según el plan de clase:
búsqueda informada (4) → A* (6) → PROPIEDADES DE LAS HEURÍSTICAS (10, la diapositiva vacía,
desarrollada) → demostración de optimalidad (5). Plan de clase: ../../weeks/week-04.md
-->

# Heurísticas y A*

## Hacer el problema tratable mediante conocimiento del dominio

**CMP-4004** · Semana 4

![bg right:35%](images/slide11-1.jpeg)

---

# Búsqueda informada

![bg right:30%](images/slide12-1.png)

A diferencia de la búsqueda ciega, utiliza **conocimiento adicional** sobre el problema para guiar
la exploración hacia el objetivo.

Ese conocimiento se representa mediante una **función heurística**:

- `h(n)` = costo estimado desde el nodo *n* hasta el objetivo
- `h(n) = 0` si *n* es el objetivo
- `h(n) ≥ 0` siempre

Una heurística **no garantiza** el camino correcto: es una estimación.
Una buena heurística reduce **drásticamente** los nodos explorados.

---

# Búsqueda voraz primero el mejor

![bg right:35%](images/slide13-1.png)

Siempre expande el nodo que *parece* estar más cerca del objetivo, usando solo `h(n)`.
**Frontera: cola de prioridad según `h(n)`.**

Es **voraz**: elige lo localmente óptimo en cada paso e ignora el costo acumulado.

- **Completa** solo cuando se controlan los estados repetidos
- **No es óptima** — no garantiza el camino de menor costo
- Puede quedar atrapada en caminos malos cuando la heurística es engañosa

<!--
4 min para búsqueda informada y voraz. Dibuja un mapa donde la búsqueda voraz avance con confianza
hacia un callejón sin salida. El fallo justifica el término g de la siguiente diapositiva, así que
muestra primero el fallo.
-->

---

# A*

![bg right:35%](images/slide14-1.png)

# `f(n) = g(n) + h(n)`

- `g(n)` — costo **real** acumulado desde el inicio hasta *n*
- `h(n)` — menor costo **estimado** desde *n* hasta el objetivo
- `f(n)` — costo total estimado del camino que **pasa por** *n*

Siempre expande el nodo con el menor `f(n)`.
**Frontera: cola de prioridad según `f(n)`.**

**La intuición en dos palabras:** *g* es lo que has gastado; *h* es lo que esperas
gastar. Minimizar la suma equilibra **avance** y **potencial**.

---

# A* — Propiedades

- **Completa** — siempre encuentra una solución si existe y `h` es admisible
- **Óptima** — garantiza el camino de menor costo si `h` es admisible/consistente
- **Espacio: O(bᵈ)** — conserva en memoria todos los nodos generados
- **Tiempo** — depende por completo de la **calidad de `h`**

Observa qué es condicional y qué no. Ambas garantías principales tienen una
hipótesis asociada, y la siguiente diapositiva trata sobre esa hipótesis.

<!--
6 min para las dos diapositivas de A*. La complejidad espacial es el principal obstáculo práctico y
los estudiantes la subestiman: en una instancia difícil, A* agota la memoria, no el tiempo.
-->

---

# Propiedades de las heurísticas

![bg left:25%](images/slide16-1.png)

<!--
==============================================================================
ESTA ES LA DIAPOSITIVA QUE ESTÁ VACÍA EN LA PRESENTACIÓN ORIGINAL.
La diapositiva 16 de 02_Problem.pptx tiene el título «Propiedades de las heurísticas» y no tiene contenido.
Se desarrolla en las cuatro diapositivas siguientes y constituye el núcleo de 10 minutos de la
semana. No lo comprimas. Todo lo que los estudiantes necesitan para el duelo 1 y el punto de control 1
está aquí.
==============================================================================
-->

### Las cuatro propiedades que importan

1. Admisibilidad
2. Consistencia
3. Dominancia
4. Factor de ramificación efectivo

### …y la idea que genera todas las heurísticas

5. Problemas relajados

---

# 1 · Admisible

## Admisible

# `h(n) ≤ h*(n)`

Nunca **sobreestima** el costo restante real. ⟹ **A\* es óptima en árboles.**

# 2 Consistente (monótona)

# `h(n) ≤ c(n, a, n′) + h(n′)`

La **desigualdad triangular** aplicada a la heurística. ⟹ **A\* es óptima en grafos**
*con* un conjunto de explorados.

**La consistencia implica admisibilidad. La recíproca no se cumple.**

<!--
¿Por qué funciona una subestimación y no una sobreestimación? Explica la intuición en la
pizarra: el OPTIMISMO evita descartar prematuramente el camino barato. Una h pesimista
puede hacer que A* ignore la ruta que realmente era la mejor.
-->

---

# 3 · Dominancia

Si `h₂(n) ≥ h₁(n)` para todo *n*, y **ambas son admisibles**, entonces h₂ **domina**
a h₁, y A* con h₂ **no expande más nodos** que A* con h₁.

> ## Una heurística mejor es estrictamente mejor.
> ## Más informada nunca es peor.

Esto es inusual y merece una pausa. La mayoría de las decisiones de ingeniería implican concesiones.
Esta no: dentro de la admisibilidad, acercarse a `h*` no cuesta nada.

---

# 4 · Factor de ramificación efectivo `b*`

El factor de ramificación *b* que necesitaría un **árbol uniforme de profundidad d** para
contener la cantidad de nodos que A* realmente expandió.

`N + 1 = 1 + b* + (b*)² + … + (b*)ᵈ`

La medida práctica de la calidad heurística. **Cuanto más cerca de 1, mejor.**

| Heurística en el rompecabezas de 8 fichas, d = 12 | `b*` (típico) |
|---|---|
| `h = 0` (es decir, UCS) | ~2.8 |
| Fichas mal colocadas | ~1.5 |
| Distancia de Manhattan | **~1.3** |

Pequeños cambios en `b*` producen enormes cambios en el trabajo, porque se eleva a una potencia.

---

# 5 · De dónde vienen las heurísticas: problemas relajados

![bg right:30%](images/slide16-2.png)

## Toda heurística admisible es la solución *exacta* de un problema más sencillo.

| Heurística | La relajación que resuelve exactamente |
|---|---|
| **Fichas mal colocadas** | una ficha puede teletransportarse a cualquier lugar en un movimiento |
| **Distancia de Manhattan** | las fichas pueden pasar **a través** de otras |
| **Distancia en línea recta** | puedes conducir a través de edificios |

Elimina una restricción → resuelve exactamente el problema más sencillo → ese valor nunca puede
superar el costo real → **admisible por construcción**.

<!--
Esta es la idea más productiva de la unidad. Enseña a los estudiantes cómo
INVENTAR heurísticas en lugar de recordarlas, y es la habilidad que evalúa el duelo 1.
Expresa la receta explícitamente: enumera las restricciones, elimina una y resuelve lo que
queda. Eso es una heurística.
-->

---

# Optimalidad de A* — La demostración

![bg right:28%](images/slide15-1.png)

**Afirmación.** Con una `h` admisible, A* devuelve una solución óptima.

**Supongamos que no.** A* devuelve un objetivo subóptimo `G₂` aunque existe un objetivo óptimo `G` de costo `C*`
alcanzable.

1. Cuando se seleccionó `G₂`, algún nodo `n` del camino óptimo hacia `G` estaba en la
   frontera.
2. Por admisibilidad: `f(n) = g(n) + h(n) ≤ g(n) + h*(n) = C*`
3. Como `G₂` es subóptimo: `f(G₂) = g(G₂) > C*`
4. Por tanto, `f(n) < f(G₂)`, así que A* habría seleccionado `n` **primero**.

## Contradicción. ∎

<!--
5 min. Hazlo rigurosamente en la pizarra. Es la única demostración formal del curso,
muestra a los estudiantes qué significa «garantía» en el eje 2 de la ficha de evaluación y
se pide en el punto de control 1.
-->

---

# A continuación: programación en vivo — A* requiere cambiar 10 líneas

Reutiliza `search` de la semana 3. Ordena la frontera por `f` en lugar de `g`.

Después ejecuta **cuatro** heurísticas sobre la misma instancia de profundidad 16:

| Heurística | Expansiones | Longitud de la solución | ¿Óptima? |
|---|---|---|---|
| `h_zero` (= UCS) | ~50,000 | 16 | ✔ |
| `h_misplaced` | ~1,500 | 16 | ✔ |
| `h_manhattan` | ~200 | 16 | ✔ |
| `h_bad = 3 × manhattan` | **~40** | **20** | ✘ |

> **`h_bad` es la más rápida y es incorrecta.**
>
> Siempre puedes ganar velocidad renunciando a la garantía; si no mides
> la calidad de la solución, no lo notarás.

**Esa oración conecta con cada comparación con LLM de este curso.**

<!--
Esta tabla reúne toda la clase en un solo recurso. Si falta tiempo, elimina el bosquejo de la
demostración antes que la tabla, pero intenta conservar ambos.
EL DUELO 1 COMIENZA ESTA SEMANA: ../../projects/duel-1-search.md
-->
