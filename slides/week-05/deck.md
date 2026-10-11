---
marp: true
theme: default
paginate: true
header: 'CMP-4004 · Semana 5 · Búsqueda adversarial y juegos'
---

<!--
Semana 5, sesión A. Tiempo para la miniclase: 25 minutos.
Fuente: 02_Problem.pptx, diapositivas 17-22. Etapas según el plan de clase:
un agente→adversarial (3) → minimax (7) → alfa-beta (10) → evaluación/horizonte (5).
La sesión B es el TORNEO. Plan de clase: ../../weeks/week-05.md
-->

# Búsqueda adversarial y juegos

## Cuando alguien intenta hacerte perder

**CMP-4004** · Semana 5

![bg right:35%](images/slide17-1.jpeg)

---

# De un agente a dos

Hasta ahora: **un agente** que busca una solución en un entorno cooperativo o
neutral.

En los juegos: **dos o más agentes con objetivos opuestos.**

El problema ya no consiste en encontrar un camino hacia el objetivo. Consiste en encontrar la **estrategia
óptima**, suponiendo que el oponente también juega de manera óptima.

### Las suposiciones iniciales

- Dos jugadores: **MAX** y **MIN**
- **Suma cero**: la ganancia de un jugador es la pérdida del otro
- **Información perfecta**: completamente observable
- **Determinista**: sin aleatoriedad

<!--
3 min. Describe el cambio con precisión: cambia la FORMA DE LA SOLUCIÓN. En las semanas 3-4, una
solución era una secuencia. Aquí es una política, condicionada a lo que haga el oponente. Por eso
no puedes simplemente volver a ejecutar A*.
-->

---

# Minimax

![bg right:35%](images/slide18-1.png)

- **MAX** intenta maximizar el valor del estado final
- **MIN** intenta minimizar ese mismo valor
- Supone que **ambos jugadores juegan de manera óptima**

El valor minimax de un nodo se define recursivamente:

```
minimax(s) = Utility(s)                          if Terminal(s)
           = max over a of minimax(Result(s,a))  if Player(s) = MAX
           = min over a of minimax(Result(s,a))  if Player(s) = MIN
```

Explora el **árbol completo** hasta los nodos terminales.
Tiempo **O(bᵐ)** · Espacio **O(b·m)**

---

# Minimax supone un oponente perfecto

Esa suposición tiene un costo.

Contra un oponente **débil**, minimax puede ser **subóptimo**: no tenderá una
trampa porque supone que el oponente nunca caerá en ella.

Una jugada que gana el 90 % de las veces contra seres humanos reales y pierde contra un jugador
perfecto es invisible para minimax.

<!--
7 min para las dos diapositivas de minimax. RESUELVE A MANO UN ÁRBOL DE PROFUNDIDAD 3 en la pizarra con
la clase indicando los valores en voz alta. No lo omitas: quienes solo han visto la
fórmula no pueden seguir su ejecución, y el punto de control 1 les pide hacerlo.
La observación sobre el oponente débil toma un minuto y resulta sorprendente.
-->

---

# Poda α-β

![bg right:32%](images/slide20-1.jpeg)

Minimax explora todo el árbol, algo inviable en juegos reales.
**α-β elimina las ramas que no pueden influir en la decisión final.**

- **α** — mejor valor encontrado hasta ahora para MAX (una cota **inferior**)
- **β** — mejor valor encontrado hasta ahora para MIN (una cota **superior**)

### Regla de poda

- Si el valor de un nodo **MIN** cae por debajo de **α** → poda
  *(MAX nunca elegiría este camino)*
- Si el valor de un nodo **MAX** supera **β** → poda
  *(MIN nunca elegiría este camino)*

**Devuelve exactamente la misma respuesta que minimax**, explorando muchos menos nodos.
Mejor caso: **O(b^(m/2))**.

---

# La poda no es una aproximación

![bg right:35%](images/slide21-1.png)

Vale la pena decirlo con cuidado, porque los estudiantes suelen clasificar α-β como un
«atajo heurístico».

No lo es. α-β descarta **solo ramas demostrablemente irrelevantes**. El valor de la
raíz es **idéntico**.

| | Minimax | α-β |
|---|---|---|
| Valor de la raíz | V | **V** |
| Nodos visitados | ~50,000 | ~4,000 |
| Garantía | exacta | **exacta** |

Obtener la misma respuesta con menos trabajo, sin pérdida, es poco frecuente. Reconoce cuándo
ocurre.

---

# El mejor caso requiere un orden perfecto de las jugadas

**O(b^(m/2)) no es lo que obtienes por defecto.** Es lo que obtienes si siempre
examinas primero la mejor jugada.

| Orden | Ramificación efectiva | Profundidad alcanzable con el mismo presupuesto |
|---|---|---|
| Peor caso | bᵐ (sin ninguna poda) | d |
| **Aleatorio** | ~b^(3m/4) | ~1.33 d |
| **Perfecto** | b^(m/2) | **2 d** |

## Un orden perfecto duplica la profundidad de búsqueda.

Y puedes aproximarlo con poco costo:

- prueba primero las **capturas**
- prueba primero la **mejor jugada de la iteración anterior**
  → por eso **profundización iterativa + α-β** es la combinación habitual

> Una heurística sobre el **orden de búsqueda** puede importar tanto como la función
> de evaluación.

<!--
10 min para las tres diapositivas de alfa-beta. Recorre el MISMO árbol de profundidad 3 de la
diapositiva de minimax y tacha las ramas podadas. La mitad del árbol tachada y el mismo
valor en la raíz: esa imagen ES la lección.
Esta tabla de ordenamiento suele recibir poca atención y decide el torneo.
-->

---

# Funciones de evaluación y el horizonte

![bg right:32%](images/slide22-1.png)

En juegos reales no es posible llegar a los nodos terminales. Por tanto: **detén la búsqueda en la profundidad *d* y aplica
`Eval(s)`.**

`Eval` estima la utilidad de una posición no terminal: material, movilidad,
estructura. Shannon propuso exactamente esto en 1950.

## El efecto horizonte

El agente aplaza las malas noticias **justo más allá de su profundidad de búsqueda** y cree que escapó.

*Caso concreto:* un motor sacrifica material para retrasar un mate inevitable
más allá de su horizonte. «Ve» una puntuación mejor y está equivocado.

> **La racionalidad limitada produce errores *característicos*, no aleatorios.**

Esa oración se aplica a todos los sistemas de este curso, incluido el LLM.

<!--
5 min. Demuestra el efecto horizonte en vivo durante el bloque de programación: prepara una posición donde
una amenaza se resuelva en la profundidad 5 y ejecuta el agente con profundidad 4. Los estudiantes lo recordarán.
-->

---

# Los tipos A y B de Shannon

Shannon (1950) dividió los programas de juegos en dos tipos, y la distinción sigue vigente:

| | Estrategia |
|---|---|
| **Tipo A** | Buscar en **todo**, con poca profundidad. Fuerza bruta. |
| **Tipo B** | Buscar profundamente en **líneas prometedoras**, usando conocimiento. |

### ¿A cuál corresponde un LLM?

**A ninguno.** Es un *evaluador* de tipo B **sin ninguna búsqueda**, un caso
que Shannon no anticipó porque, en 1950, era inconcebible una función de evaluación lo bastante buena
como para jugar sin buscar.

Ruoss y colaboradores (2024): un transformer de 270 millones de parámetros, entrenado con 10 millones de
partidas anotadas por Stockfish, alcanza aproximadamente 2895 puntos Elo en ajedrez relámpago de Lichess: **nivel de
gran maestro, sin búsqueda durante la inferencia.**

**Entonces, ¿fue alguna vez esencial la búsqueda?** El propio artículo lo plantea como *planificación amortizada.*
El costo de búsqueda se pagó durante el **entrenamiento**. No desapareció: cambió de lugar.

<!--
Esta diapositiva incorpora la contraparte moderna a la clase para que la discusión del
artículo tenga un punto de conexión. Es la misma lección que Searchformer en la semana 4,
desde otra perspectiva: haz que la clase reconozca la convergencia.
-->

---

# A continuación: programación en vivo — Conecta 4

Construye el juego, después minimax y luego α-β. Registra cada nodo.

**Tres demostraciones, en orden:**

1. **La misma respuesta, menos nodos.** Comprueba con una aserción que ambos devuelven valores idénticos a profundidad 6;
   después muestra los conteos.
2. **Orden de las jugadas.** Ordena las jugadas empezando por el centro en lugar de ir de izquierda a derecha. Una línea;
   el conteo suele reducirse otra vez a la mitad.
3. **El efecto horizonte, en vivo.** Una amenaza que se resuelve en profundidad 5 y un agente
   que busca hasta profundidad 4.

---

# Sesión 5B — El torneo

## Entrega un agente

```python
def choose_move(board, time_budget_ms) -> int: ...
```

**Reglas estrictas:** 500 ms por jugada · sin procesos externos · sin llamadas de red ·
sin un libro de aperturas de más de 20 posiciones.

**Entrega 24 h antes de la sesión 5B** para poder realizar una prueba básica.

Todos contra todos: cada pareja juega contra las demás, con ambos colores. Después entra un **LLM
retador** en el cuadro del torneo.

<!--
Haz predicciones antes de cada partida. Cuando un agente pierda, pregunta a sus autores qué ocurrió.
Resultados recurrentes que vale la pena comentar: una evaluación sofisticada pierde contra un
agente más simple que busca dos medias jugadas más profundo (LA PROFUNDIDAD SUELE SUPERAR AL CONOCIMIENTO a
esta escala); alguien agota el tiempo y pierde por ello (lo que convierte a la profundización
iterativa en un algoritmo que puede interrumpirse en CUALQUIER MOMENTO, no solo en un truco de memoria).
Incluye en el cuadro un agente alfa-beta de referencia sin identificar, con profundidad 6, y
revélalo al final.
-->
