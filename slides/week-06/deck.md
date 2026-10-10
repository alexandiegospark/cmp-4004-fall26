---
marp: true
theme: default
paginate: true
header: 'CMP-4004 · Semana 6 · Satisfacción de Restricciones'
---

<!--
Semana 6, Sesión A. Duración de la mini-clase: 25 minutos.
Fuente: 02_Problem.pptx diapositivas 23-25 (solo tres diapositivas — la mayor parte de esta presentación
fue creada para completar el contenido faltante). Ritmo según el plan de clase: cambio de representación (5) →
definición formal (4) → backtracking (4) → inferencia (7) → ordenamiento (5).
EL DUELO 1 SE ENTREGA EN ESTA SESIÓN. Plan de clase: ../../weeks/week-06.md
-->

# Problemas de Satisfacción de Restricciones

## Abriendo la caja negra

**CMP-4004** · Semana 6

![bg right:35%](images/slide23-1.jpeg)

---

# Un cambio de representación

![bg right:35%](images/slide23-2.jpeg)

En la búsqueda estándar, los estados son **cajas negras** — lo único que importa es alcanzar la meta.

En un CSP, los estados tienen **estructura interna**: variables con valores que deben
satisfacer restricciones.

Un CSP se resuelve cuando se encuentra una asignación de valores **completa y consistente**
para todas las variables.

### Por qué esto importa

La estructura permite realizar **inferencia**. Puedes razonar sobre una asignación *parcial* —
algo que es imposible cuando los estados son atómicos.

*Esta es la ventaja de pasar de representaciones atómicas a representaciones factorizadas (semana 2).*

<!--
5 min. Conectar explícitamente con la diapositiva de la semana 2 sobre representaciones
atómicas/factorizadas/estructuradas.
Las semanas 3-5 fueron atómicas. Esta semana es factorizada. Las semanas 8-9 son estructuradas.
-->

---

# Dos ejemplos

![bg right:30%](images/slide24-1.png)

## Sudoku

**Restricción** — los números no pueden repetirse en ninguna fila, columna o bloque 3×3.

## Horario escolar

**Restricción** — los deportes no pueden programarse después del almuerzo.

En el fondo, ambos son el mismo tipo de objeto: variables, dominios y restricciones sobre
combinaciones.

---

# Definición formal ⟨X, D, C⟩

| | |
|---|---|
| **Variables** | `X = {X₁, X₂, …, Xₙ}` — lo que debe asignarse |
| **Dominios** | `D = {D₁, D₂, …, Dₙ}` — valores posibles para cada variable |
| **Restricciones** | `C` — las condiciones que deben satisfacer las asignaciones |

- Una asignación **consistente** no viola ninguna restricción
- Una asignación **completa** asigna un valor a cada variable
- Una **solución** es completa **y** consistente

### Un hecho estructural con una gran consecuencia

Los CSP son **conmutativos** respecto al orden de asignación: el conjunto de soluciones no depende
del orden en que se asignen las variables. **Por lo tanto, puedes elegir cualquier orden que
quieras — y elegir bien representa gran parte de la ventaja.**

<!--
4 min. El punto de la conmutatividad es lo que permite utilizar las heurísticas de ordenamiento
que aparecen cinco diapositivas más adelante. Explicarlo aquí o MRV parecerá arbitrario después.
-->

---

# Búsqueda por backtracking

![bg right:32%](images/slide25-1.png)

Búsqueda en profundidad sobre asignaciones **parciales**, rechazando temprano las que son
inconsistentes.

```
function BACKTRACK(asignacion, csp):
    if asignacion esta completa: return asignacion
    var ← SELECCIONAR-VARIABLE-NO-ASIGNADA(csp, asignacion)
    for each valor in ORDENAR-VALORES-DOMINIO(var, asignacion, csp):
        if valor es consistente con asignacion:
            agregar {var = valor} a asignacion
            resultado ← BACKTRACK(asignacion, csp)
            if resultado ≠ fallo: return resultado
            eliminar {var = valor}
    return fallo
```

**Contraste con generar-y-probar:** backtracking comprueba las restricciones en *cada* asignación,
no solamente al final. Esa es la diferencia entre 10⁷⁷ posibilidades y un problema tratable.

---

# Inferencia: reduce los dominios antes de buscar

## Forward checking

Cuando asignas `X`, elimina los valores conflictivos de los dominios de sus
**vecinos no asignados**. Es barato. Detecta fallos **un paso** antes.

## Consistencia de arcos / AC-3 (Mackworth 1977)

Propaga utilizando una **cola de arcos hasta alcanzar un punto fijo**. Un arco `(Xᵢ, Xⱼ)` es consistente
cuando cada valor de `Dᵢ` tiene *algún* valor compatible en `Dⱼ`.

Es más potente — detecta fallos que forward checking no detecta. Incluso puede demostrar
que un problema no tiene solución **antes de que comience la búsqueda**.

> AC-3 **no es un solucionador.** Es un preprocesador y un mecanismo de poda durante la búsqueda. Normalmente
> todavía deja un problema de búsqueda por resolver.

<!--
7 min. Mostrar una instancia de coloreo de mapas donde forward checking no detecta NADA y AC-3
detecta inmediatamente que el problema no tiene solución. Ese contraste es lo que justifica el
costo adicional de AC-3; sin él, los estudiantes pueden concluir que forward checking es suficiente.
Destacar el punto local/global del artículo: la consistencia de arcos es una propiedad LOCAL, entre pares,
que produce una reducción GLOBAL. La propagación local es barata; la consistencia global no lo es.
-->

---

# Heurísticas de ordenamiento

| Heurística | Regla | Por qué |
|---|---|---|
| **MRV** — mínimo de valores restantes | asignar primero la variable **más restringida** | **fallar rápido** |
| **Grado** | desempatar MRV usando la variable involucrada en **más restricciones** | reducir ramificaciones futuras |
| **LCV** — valor menos restrictivo | probar el valor que elimina **menos opciones** de los vecinos | **tener éxito primero** |

## La asimetría

> **El ordenamiento de variables busca fallar rápido. El ordenamiento de valores busca tener éxito primero.**

Elegir una variable significa decidir dónde *descubrir* un callejón sin salida — conviene hacerlo lo más temprano
y barato posible. Elegir un valor significa decidir qué rama *recorrer* — conviene recorrer primero
la que tenga mayor probabilidad de funcionar.

<!--
5 min. Los estudiantes suelen encontrar confusa la inversión fallar-rápido/tener-éxito-primero hasta que se
explica en voz alta exactamente con esas palabras. Decirlo.
-->

---

# La tabla de ablación

Misma instancia de Sudoku. Mismo algoritmo de búsqueda en todos los casos.

| Configuración | Llamadas a backtracking | Tiempo |
|---|---|---|
| Backtracking simple | ~120,000 | 8.2 s |
| + forward checking | ~9,000 | 0.9 s |
| + MRV | ~400 | 0.05 s |
| + preprocesamiento AC-3 | **~60** | **0.02 s** |

**Tres órdenes de magnitud de mejora con aproximadamente 30 líneas de código.**

> Este es el *mismo* algoritmo de búsqueda. Toda la mejora provino de la **inferencia y el
> ordenamiento** — de pensar mejor sobre el problema, no de usar más capacidad computacional.

Los estudiantes que interiorizan esto entienden por qué "simplemente usar un modelo más grande" no siempre
es la respuesta.

---

# Logic-LM: la arquitectura del resto del curso

![bg right:28%](images/slide23-1.jpeg)

Pan et al. (2023). El patrón:

```
lenguaje natural
      │
      ▼  LLM  ← bueno interpretando texto ambiguo
especificación formal (CSP / SAT / PDDL)
      │
      ▼  SOLUCIONADOR SIMBÓLICO  ← proporciona la garantía
respuesta
      │
      └── ¿error? devolverlo y volver a traducir  (auto-refinamiento)
```

- El LLM hace aquello en lo que realmente es bueno: **interpretar lenguaje ambiguo**
- El solucionador hace aquello en lo que realmente es bueno: **ejecutar de forma confiable
  un procedimiento combinatorio**
- **La garantía está en el solucionador.** Si el modelo formal representa fielmente el problema, la respuesta es
  *demostrablemente* correcta.

---

# El modo de fallo cambia — y ese es precisamente el punto

| Arquitectura | Modo de fallo | ¿Puedes detectarlo? |
|---|---|---|
| LLM de extremo a extremo | respuesta incorrecta | **sin señal** |
| LLM + solucionador | **modelo incorrecto, correctamente resuelto** | frecuentemente **sí** — puede no parsearse, el solucionador puede indicar *insatisfacible*, o puedes comparar el modelo con el texto original |

> ## Un generador poco confiable más un verificador sólido puede producir un sistema confiable.

Esta oración es la tesis de este curso. Aparece nuevamente en las semanas 7, 8, 9
y en tu proyecto final.

<!--
Esta es la diapositiva clave del semestre. En el estudio, los estudiantes construyen los tres enfoques
(modelado manual / híbrido / extremo a extremo) y el descubrimiento esperado es exactamente el de la columna derecha:
los fallos del enfoque B son EVIDENTES y los del enfoque C son SILENCIOSOS.
No darles esa conclusión aquí — preparar el escenario y dejar que los datos la demuestren.
Preguntar en las demostraciones: "¿qué enfoque preferirían desplegar y cómo sabrían que falló?"
-->

---

# Siguiente

## Programación en vivo — un solucionador CSP con ablaciones activables

## Estudio — el experimento de tres enfoques

| Enfoque | Pipeline |
|---|---|
| **A — Modelado manual** | tú escribes el CSP → tu solucionador |
| **B — Híbrido** | el LLM escribe el CSP → tu solucionador |
| **C — Extremo a extremo** | el LLM lee el problema y responde |

20 problemas lógicos escritos en lenguaje natural. Clasifica **cada** fallo del enfoque B:
JSON mal formado · JSON válido pero modelo incorrecto · sobre-restringido · timeout.

Luego agrega el ciclo de auto-refinamiento y reporta la diferencia.

**El Duelo 1 se entrega hoy.**
