---
marp: true
theme: default
paginate: true
header: 'CMP-4004 · Semana 1 · ¿Qué es la inteligencia?'
---

<!--
Semana 1, sesión A. Tiempo para la miniclase: 25 minutos.
Fuente: 01_Introduction to Artificial Intelligence.pptx (19 diapositivas), reorganizada
en una única línea temporal cronológica. Plan de clase: ../../weeks/week-01.md
-->

# Inteligencia artificial

## Fundamentos clásicos, comparaciones modernas

**CMP-4004** · Semana 1


![bg right:35%](images/slide01-1.jpeg)

---

# ¿Qué entendemos por *inteligencia*?

- La capacidad de entender o comprender
- La capacidad de resolver problemas
- Conocimiento, comprensión, el acto de entender
- El significado asignado a una proposición o expresión
- Capacidad, habilidad y experiencia

## ¿Y por inteligencia *artificial*?

<!--
2 min. NO resuelvas esta cuestión. Ya se realizó la encuesta inicial y los
resultados están en pantalla. Señala que las cinco definiciones son circulares o
discutibles: todas usan una palabra que necesita la misma explicación.
Este es exactamente el problema al que se enfrentó Turing y prepara la discusión del artículo.
-->

---

# Las ideas más antiguas son más antiguas de lo que crees

![bg right:40%](images/slide19-1.png)

**~800 a. C.** — la *Ilíada* describe a **Talos**: un autómata de bronce que protege Creta
de piratas e invasores.

La idea de un objeto fabricado que actúa por sí solo no pertenece a la informática. Es una
idea mitológica y aparece unos 2700 años antes del hardware.

---

# ~200 a. C. — El mecanismo de Anticitera

![bg right:45%](images/slide18-1.png)

La **computadora analógica** más antigua conocida. Predice posiciones astronómicas y
eclipses con hasta 19 años de anticipación; también calcula las fechas de seis competiciones
atléticas griegas.

> Este descubrimiento cuestiona de manera fundamental la creencia de que el desarrollo
> tecnológico humano siempre ha sido gradual.

<!--
1 min. Dedica 20 segundos al hallazgo: unos buzos lo encontraron en 1900;
en 1902 los arqueólogos descartaron un engranaje incrustado en roca porque el mecanismo
«parecía demasiado avanzado para la época». El estudio riguroso solo se retomó entre 1951 y 1971.
La lección trata de cómo los expertos manejan evidencia que contradice su modelo:
una lección que este curso utilizará repetidamente.
-->

---

# 1770 — El Turco mecánico

![bg right:40%](images/slide03-2.jpeg)

Construido por Wolfgang von Kempelen. Parecía jugar al ajedrez a un alto nivel contra
oponentes humanos.

**Había un ser humano escondido dentro.**

### Pregunta para la clase

¿Cuál es el equivalente moderno?

<!--
2 min; permite este desvío. Alguien mencionará etiquetadores de datos, anotadores de RLHF o
productos de «IA» con intervención humana. Esa es la respuesta correcta. Amazon dio a una
plataforma de trabajo colaborativo el nombre de esta máquina, aparentemente de forma intencional.
El Turco es el primer fraude de IA y establece la distinción central del curso:
la APARIENCIA de inteligencia frente al mecanismo.
También son de esta época los autómatas de Jaquet-Droz (1768-1774): la música,
el dibujante y el escritor. Mecanismos reales, sin seres humanos escondidos.
-->

---

# 1936–1945 — Computación de propósito general

![bg right:35%](images/slide04-1.png)

**Z1** (1936, Konrad Zuse) — calculadora binaria, leía operaciones de tarjetas
perforadas, aritmética de punto flotante, memoria de almacenamiento.

**ENIAC** (1945) — Integrador Numérico Electrónico y Computadora. Programable,
tubos de vacío, 170 m², 27 toneladas métricas.

Ahora existe el soporte físico. Todo lo que sigue trata de **qué calcular**.

---

# 1950 — La prueba de Turing

![bg right:38%](images/slide05-1.png)

Dos seres humanos y una computadora. El interrogador está aislado y hace preguntas
mediante una terminal de texto; después decide cuál de los participantes es la máquina.

Si el interrogador no puede distinguirlos, **se supone que la máquina es inteligente**.

> Un intento de proporcionar una definición *operativa* y satisfactoria de
> la inteligencia.

<!--
2 min. La palabra clave es «operativa». La propuesta de Turing: sustituir una
pregunta imposible de responder («¿pueden pensar las máquinas?») por una comprobable («¿pueden
superar esta prueba?»). Ese es el paso metodológico fundacional del campo y es el
mismo que está detrás de cada evaluación que los estudiantes realizarán este semestre.
Conexión: la discusión del artículo ya cubrió las nueve objeciones de §6.
Conexión con el curso: resultó posible manipular la evaluación. Conserva esa idea.
-->

---

# 1956 — Dartmouth: el campo recibe un nombre

![bg right:33%](images/slide07-1.png)

> «El estudio se realizará sobre la base de la conjetura de que **cada aspecto del
> aprendizaje o cualquier otra característica de la inteligencia puede, en principio, describirse
> con tanta precisión que sea posible construir una máquina que lo simule.**»

McCarthy · Minsky · Rochester · Shannon

**La agenda de 1956:** computadoras automáticas · programar una computadora para usar lenguaje ·
redes neuronales · teoría del tamaño de un cálculo · mejora autónoma ·
abstracciones · aleatoriedad y creatividad

<!--
2 min. Lee en voz alta la última oración de la propuesta: «Creemos que se
puede lograr un avance significativo... si un grupo de científicos cuidadosamente seleccionado
trabaja en ello conjuntamente durante un verano».
Después pregunta qué tan acertada fue esa estimación. Los siete puntos de la agenda siguen siendo
áreas de investigación abiertas 70 años después. Este es el documento fundacional del campo y su
primer retraso respecto al calendario; el optimismo sobre los plazos es una característica permanente de la IA.
-->

---

# 1957–1958 — Dos lenguajes, dos filosofías

![bg right:30%](images/slide06-1.svg)

| **FORTRAN** (1957, IBM) | **LISP** (1958, McCarthy) |
|---|---|
| Computación numérica | Computación simbólica |
| **Imperativo** | Basado en el **cálculo λ** y la recursión |
| Gestiona el estado (variables) | Tipos dinámicos y funciones |
| Condicionales, bucles | Estructura principal: la **lista** |
| | Llamadas en notación prefija: `(f a1 a2 a3)` |

La IA simbólica se escribió en LISP durante treinta años porque el lenguaje y la
teoría compartían una misma estructura.

---

# 1958 — El perceptrón

![bg right:38%](images/slide08-1.png)

Un modelo computacional inspirado en las neuronas biológicas, propuesto por
**Frank Rosenblatt**.

- Una red de unidades de procesamiento simples que almacena conocimiento a partir de la experiencia
- El conocimiento se adquiere del entorno mediante un **proceso de aprendizaje**
- Las conexiones entre unidades —los **pesos sinápticos**— son donde reside el conocimiento

**La idea:** aprender de los datos en lugar de ser programado.

<!--
1 min aquí; el tratamiento completo corresponde a la semana 14.
CORRECCIÓN QUE DEBES DECIR EN VOZ ALTA: la presentación 07 del material original lo llama «Mark»
Rosenblatt. Es FRANK Rosenblatt. «Mark I Perceptron» era el nombre de la máquina:
casi con certeza ese es el origen del error. Corrígelo abiertamente; mostrar
cómo manejar un error en una fuente es parte de lo que enseña esta diapositiva.
-->

---

# 1972 — Prolog

![bg right:30%](images/slide09-1.png)

**Algoritmo = Lógica + Control**

- Un lenguaje de programación lógica **declarativo**
- Los programas son conjuntos de cláusulas con una notación cercana a la lógica de primer orden
- El programador expresa lo que es *verdadero*; el lenguaje realiza la búsqueda
- Muchos sistemas expertos —jurídicos, médicos y financieros— se escribieron en él

<!--
1 min. Tratamiento completo en la semana 8.
DOS CORRECCIONES a la presentación original; hazlas de forma visible:
  1. Dice «Creado por Dennis Ritchie en Bell Labs». Es falso. Prolog fue
     creado por ALAIN COLMERAUER y PHILIPPE ROUSSEL en Marsella en 1972.
     Ritchie creó C: una confusión comprensible solo si no se
     revisa con atención.
  2. Describe Prolog como «un lenguaje imperativo y compilado» dos líneas después de
     describir correctamente la programación lógica. Prolog es declarativo.
Di claramente: estoy corrigiendo mi propio material del curso delante de ustedes. Hagan lo mismo con
mis diapositivas cuando encuentren algo incorrecto. Esa instrucción es fundamental
en un curso cuyo método consiste en comprobar afirmaciones frente a la evidencia.
-->

---

# ¿Qué *es* un modelo?

- Una descripción de un sistema o fenómeno en lenguaje matemático
- Una **hipótesis** para explicar un fenómeno
- Algo que construimos o suponemos a partir de reglas definidas *a priori* o de
  observaciones

## Dos formas de construir uno

| **Métodos formales** | **Métodos estadísticos** |
|---|---|
| Lógica de primer orden | Regresión |
| Cálculo λ | Clasificación |
| Lógica temporal | Redes bayesianas |
| Sistemas de reescritura | Redes de Markov |
| Cálculo causal | |

<!--
3 min. Esta es la diapositiva más importante de la presentación. Dilo explícitamente:
  la columna IZQUIERDA corresponde a las semanas 3-11. La DERECHA, a las semanas 12-14.
  La tensión entre ambas ES el curso.
No dejes que se interprete como una simple taxonomía. Es el programa del curso.
-->

---

# 1975 / 1986 — Retropropagación

![bg right:35%](images/slide11-1.png)

Calcula el gradiente de la pérdida con respecto a cada peso de la red.

Permitió entrenar **unidades conectadas en serie**, añadiendo la no linealidad
que permite a una red resolver **XOR**.

<!--
1 min; se deriva rigurosamente en la semana 14.
CORRECCIÓN: la presentación lo fecha en 1975, correspondiente a la tesis de Werbos. El resultado que
realmente impulsó el campo es el de Rumelhart, Hinton y Williams (1986). Vale la pena
mencionar ambas fechas; la diferencia de 11 años entre «publicado» y «reconocido» es, por sí misma,
una lección sobre cómo se reciben las ideas en un campo.
-->

---

# 1995 — Máquinas de vectores de soporte

![bg right:35%](images/slide12-1.png)

Vapnik y sus colegas de AT&T Bell Labs: un clasificador lineal que **maximiza el
margen** entre dos subespacios.

Llega la teoría del aprendizaje estadístico: la generalización se convierte en algo sobre lo que puedes
razonar, en lugar de algo que solo esperas obtener.

<!--
30 segundos. Solo como hito. No enseñamos el truco del kernel en este curso;
dilo y explica por qué: requiere una sesión que no tenemos; consulta el mapa de cobertura.
-->

---

# Años 2000 — Aprendizaje profundo

![bg right:35%](images/slide13-1.png)

Las herramientas teóricas existían desde los años sesenta; el término aparece en 1986. Bengio,
Hinton y LeCun establecen las bases para entrenar redes cuya **profundidad**
puede aumentar.

Lo que cambió no fue la idea. Fueron **los datos y la capacidad de cómputo**.

---

# Los límites de los modelos estadísticos

![bg right:45%](images/slide15-1.png)

La correlación no es intervención.

**El cálculo causal de Judea Pearl (1987)** representa relaciones de causa y efecto en un
**grafo dirigido acíclico**, lo que permite preguntar:

- ¿Es A la causa y B el efecto?
- ¿Es B la causa y A el efecto?
- *(Pero no ambas cosas a la vez.)*

Un modelo que predice no necesariamente puede decirte **qué ocurre si actúas**.

<!--
2 min. Esta es la mejor idea de la presentación original y es fácil omitirla.
Consérvala: es la formulación más clara disponible de lo que no proporciona un sistema puramente
predictivo; y cada LLM que la clase evalúe este semestre es un
sistema puramente predictivo. Anticipa la semana 12.
-->

---

# La línea temporal en una tabla

| Época | Hito | Lo que hizo *posible* |
|---|---|---|
| ~800 a. C. | Talos (mito) | La idea de un objeto fabricado autónomo |
| ~200 a. C. | Anticitera | La computación como artefacto físico |
| 1770 | Turco mecánico | La *apariencia* de inteligencia y el primer fraude de IA |
| 1936–45 | Z1, ENIAC | Computación programable de propósito general |
| 1950 | Prueba de Turing | La inteligencia como algo que puedes *comprobar* |
| 1956 | Dartmouth | La IA como disciplina con nombre y agenda |
| 1957–58 | FORTRAN, LISP | Computación imperativa frente a simbólica |
| 1958 | Perceptrón | Aprender de los datos en lugar de ser programado |
| 1972 | Prolog | La computación como deducción lógica |
| 1986 | Retropropagación (pub. 1975) | Profundidad → no linealidad → XOR |
| 1987→ | Cálculo causal | Razonar sobre intervenciones |
| 1995 | SVM | Maximización del margen; teoría del aprendizaje |
| Años 2000 | Aprendizaje profundo | Aprendizaje de representaciones a gran escala |

<!--
No leas esto en voz alta. Es la diapositiva de referencia que los estudiantes capturan.
Vale la pena mencionar los hitos por lo que HICIERON POSIBLE, no por sus fechas.
-->

---

# A continuación: programación en vivo

## Construimos ELIZA (1966) en 40 líneas

Después la hacemos fallar deliberadamente.

**La pregunta con la que terminaremos:**

> Un LLM tampoco tiene un modelo explícito del mundo: predice tokens.
> ¿Es ELIZA con más parámetros o es algo de una categoría diferente?
>
> *Escribe tu respuesta. Volveremos a abrirla en la semana 14.*

<!--
El código para programar en vivo está en ../../weeks/week-01.md. Recoge las predicciones selladas:
son el mejor entregable disponible para cerrar la semana 14; los estudiantes las pierden
si no las conservas tú.
-->
