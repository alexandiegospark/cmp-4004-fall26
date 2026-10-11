---
marp: true
theme: default
paginate: true
header: 'CMP-4004 · Semana 2 · Agentes inteligentes'
---


# Agentes inteligentes

## La abstracción que resiste todos los cambios

**CMP-4004** · Semana 2

![bg right:35%](images/slide01-1.jpeg)

---

# ¿Qué es un agente?

![bg right:40%](images/slide02-1.png)

Cualquier entidad que **percibe** su entorno mediante sensores y **actúa** sobre él
mediante actuadores.

| | Sensores | → | Actuadores |
|---|---|---|---|
| **Ser humano** | ojos, oídos | cerebro | manos, boca |
| **Robot** | cámaras, sensores | procesador | motores |
| **Agente de software** | teclado, entrada de archivos | programa | pantalla, red |

Esa es toda la definición. Data de 1995 y sigue vigente, incluso para
cualquier producto comercializado como «agente de IA» en 2026.

<!--
NOTA SOBRE LA PRESENTACIÓN ORIGINAL: la diapositiva 2 de 03_Intelligent Agents.pptx contiene tres
viñetas sobre proposiciones y conectores lógicos, copiadas de la
presentación de lógica proposicional. No corresponden a una diapositiva titulada «¿Qué es un
agente?» y aquí se sustituyen. Si muestras el archivo original, omítelas.
-->

---

# *Función* del agente frente a *programa* del agente

![bg right:30%](images/slide03-1.svg)

| **Función del agente** | **Programa del agente** |
|---|---|
| Especificación abstracta del comportamiento | Implementación concreta |
| Define qué hacer en *cada* situación posible | Se ejecuta en una arquitectura física real |
| Asigna una acción al **historial** de percepciones: `f : P* → A` | Aproxima `f` de forma compacta y eficiente |
| En teoría, una tabla de consulta | |
| *Lo que queremos lograr* | *Cómo lo aproximamos de manera eficiente* |

---

# Por qué la tabla no es una opción

![bg right:35%](images/slide04-1.png)

**Mundo de la aspiradora.** Dos habitaciones, A y B; cada una puede estar sucia o limpia.
Sensores: posición actual + estado de la habitación. Actuadores: izquierda, derecha, aspirar.

Con *T* pasos de tiempo, la tabla de historiales de percepción tiene **4^T filas**.

| T | Filas |
|---|---|
| 5 | 1,024 |
| 10 | ~10⁶ |
| **20** | **~10¹²** |

> **Toda la IA consiste en buscar programas compactos que aproximen funciones
> intratables.**

<!--
5 min para esta diapositiva y la anterior juntas. Haz que calculen T=20:
no te limites a mostrar el número.
La oración final justifica las semanas 3-14. Dila exactamente una vez y despacio.
-->

---

# PEAS

![bg right:30%](images/slide06-1.png)

| | |
|---|---|
| **P** (rendimiento) | El criterio de éxito |
| **E**ntorno | El mundo en el que opera el agente |
| **A**ctuadores | Mecanismos para actuar sobre él |
| **S**ensores | Mecanismos para percibirlo |

### Taxi automatizado

- **P** — seguro, rápido, legal, cómodo, rentable *(estos criterios entran en conflicto)*
- **E** — carreteras, tráfico, peatones, clima
- **A** — dirección, acelerador, freno, señales, bocina, pantalla
- **S** — cámaras, lidar, GPS, velocímetro, acelerómetro

<!--
5 min. UN ejemplo bien desarrollado, no cuatro tratados superficialmente. La idea central es que
los componentes de P entran en conflicto: precisamente por eso existen los agentes basados en utilidad,
que veremos cuatro diapositivas más adelante.
-->

---

# Racionalidad

![bg right:32%](images/slide05-2.png)

Un **agente racional** selecciona, en cada momento, la acción que maximiza el
**valor esperado de una medida de rendimiento**, dados su historial de percepciones y
el conocimiento que incorpora.

Eso puede requerir que:

- **Explore** el entorno para recopilar información útil
- **Aprenda** de sus percepciones para mejorar su comportamiento futuro

Racional ≠ omnisciente. Racional ≠ acertado en retrospectiva.

---

# La medida de rendimiento es *tu* problema

La medida de rendimiento es un criterio **externo**. **La define quien diseña
el sistema, no el agente.**

> ## ⚠️ Obtienes lo que pides.
> ## Una medida deficiente produce comportamientos no deseados.

- ¿Qué ocurre si la especificamos incorrectamente?
- ¿Qué ocurre si no especificamos todo?

**Recompensar `dirt collected`** → una aspiradora perfectamente racional arroja suciedad al suelo
para poder recogerla de nuevo.

<!--
5 min; no lo apresures. Esta es la afirmación más importante de la presentación original.
Esto es manipulación de la recompensa o de la especificación y ahora es el problema central
de la seguridad de la IA. El hilo ético del curso empieza AQUÍ, en la semana 2, no en
la última clase. Conéctalo explícitamente con la semana 14.
-->

---

# Seis ejes del entorno como costos de ingeniería

![bg right:28%](images/slide08-1.jpeg)

| Eje | En el caso difícil, debes añadir… |
|---|---|
| Parcialmente observable | estado de creencias / estimación del estado **(sem. 12–13)** |
| Estocástico | razonamiento probabilístico, utilidad esperada **(sem. 12)** |
| Secuencial | búsqueda y planificación **(sem. 3–9)** |
| Dinámico | restricciones de tiempo real, deliberación limitada |
| Continuo | discretización u optimización continua **(sem. 10–11)** |
| Multiagente | razonamiento adversarial **(sem. 5)** |

**Esta tabla es el programa del curso disfrazado.** Dilo en voz alta.

---

# Los ejes formulados como preguntas

| Eje | La pregunta |
|---|---|
| **Observable** | ¿Puede el agente acceder al estado completo en todo momento? ¿Pueden sus sensores detectar lo relevante para elegir una acción? ¿Necesita memoria? |
| **Determinista** | ¿El siguiente estado está completamente determinado por el estado actual y la acción? *Estocástico:* misma entrada, distintas salidas. |
| **Episódico** | ¿Es independiente cada episodio de percepción y acción? ¿Pueden las decisiones actuales afectar las futuras? |
| **Estático** | ¿Cambia el entorno mientras el agente delibera? *Semidinámico:* el mundo no cambia, pero tu puntuación sí; por ejemplo, el ajedrez con reloj. |
| **Discreto** | ¿Hay un número finito de estados, percepciones y acciones bien definidos? |
| **Un solo agente** | ¿Hay otros agentes, competitivos o cooperativos? |

![](images/slide09-1.jpeg) ![](images/slide10-1.jpeg) ![](images/slide11-1.jpeg) ![](images/slide12-1.png)

---

# Clasifica estas tareas

| Tarea | Obs. | Det. | Epis. | Estático | Disc. | Agentes |
|---|---|---|---|---|---|---|
| Ajedrez con reloj | total | det. | sec. | **semi** | disc. | varios |
| Póquer | **parcial** | **estoc.** | sec. | estático | disc. | varios |
| Conducir un taxi | **parcial** | **estoc.** | sec. | **dinámico** | **cont.** | varios |
| Diagnóstico médico | **parcial** | **estoc.** | sec. | dinámico | cont. | uno |
| Crucigrama | total | det. | sec. | estático | disc. | uno |

Lee las entradas en negrita como una lista de recursos necesarios. Conducir un taxi tiene negrita en cinco
columnas: por eso sigue sin estar resuelto.

<!--
10 min en total para las tres diapositivas sobre ejes. Haz la clasificación mediante una encuesta en vivo o
en el chat; funciona mucho mejor como actividad que como respuesta revelada.
-->

---

# Cuatro arquitecturas, cada una corrige el defecto de la anterior

![bg right:30%](images/slide14-1.png)

## 1 · Agente reactivo simple

- Considera solo la **percepción actual**. Sin memoria.
- Opera mediante **reglas de condición y acción**
- ✅ Implementación simple y eficiente
- ❌ **Falla en entornos parcialmente observables**: si no puede ver el
  estado completo, no puede actuar correctamente

Solo funciona cuando la percepción actual contiene toda la información relevante.

---

# 2 · Agente reactivo basado en modelos

![bg right:30%](images/slide15-1.png)

Mantiene un **estado interno** mediante dos modelos:

- **Modelo del mundo** — cómo evoluciona el entorno independientemente del agente
- **Modelo de transición** — cómo afectan al entorno las acciones del propio agente

Actualiza el estado interno en cada paso y luego aplica reglas de condición y acción **a ese
estado**.

Ahora puede actuar de forma coherente **sin observar el entorno completo**.

---

# 3 · Agente basado en objetivos

![bg right:30%](images/slide16-1.png)

Saber dónde *estás* no es suficiente: también necesitas saber adónde **quieres
ir**.

- Los **objetivos** describen estados deseados del mundo
- El agente elige acciones que lo acercan al objetivo; esto requiere
  **planificación y búsqueda**
- ✅ Se adapta cuando cambia el objetivo
- ❌ Los objetivos son **binarios**: no distinguen un camino mejor de uno peor

---

# 4 · Agente basado en utilidad

![bg right:30%](images/slide17-1.png)

Distingue entre soluciones de **diferente calidad**. Elige la acción que
maximiza la **utilidad esperada**, ponderando los resultados por su probabilidad.

Maneja:

- **Objetivos en conflicto** — rapidez frente a seguridad en un taxi
- **Incertidumbre** — actuar cuando el resultado no está garantizado

Solo la utilidad permite equilibrar criterios. Los objetivos no.

<!--
5 min para las cuatro arquitecturas. Enfatiza especialmente el último paso: la tarea del taller depende de
él. Su agente basado en utilidad dejará una habitación sucia porque limpiarla cuesta más que
la recompensa restante, y lo reportarán como un error.
-->

---

# ¿Cuánta estructura tiene un estado?

![bg right:32%](images/slide18-1.png)

| Representación | Un estado es… |
|---|---|
| **Atómica** | una caja negra indivisible, sin estructura interna |
| **Factorizada** | un conjunto de variables o atributos con valores |
| **Estructurada** | objetos y las relaciones entre ellos |

**¿Por qué importa el nivel?**

Una mayor expresividad permite más razonamiento y aumenta la complejidad
computacional.

*Atómica → semanas 3–5. Factorizada → semana 6. Estructurada → semanas 8–9.*

---

# A continuación: programación en vivo

## Mundo de la aspiradora, tres agentes, una interfaz

Después **hacemos fallar el sensor de ubicación** en cuatro líneas y observamos cómo el agente reactivo
se vuelve incapaz de actuar.

**Taller:** conectarás un LLM a la misma interfaz `percept → action` y
contarás cuántas líneas de código defensivo necesita que los agentes clásicos no necesitaban.

<!--
El código está en ../../weeks/week-02.md. El fallo del sensor es lo que justifica
el agente basado en modelos; no pases directamente a la solución.
-->
