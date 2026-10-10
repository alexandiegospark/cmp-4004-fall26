"""
Week 7 — Tarea 1: agente Wumpus lógicamente correcto (SOUND).

Completa las funciones de este archivo y luego ejecuta:

    python3 test_dpll.py

Todas las pruebas deben pasar, INCLUYENDO:

    test_reckless_agent_is_unsound

Esta prueba comprueba que un agente que NO utiliza la verificación por
entailment puede moverse hacia una casilla que no está demostrada como segura.

La idea importante es poder observar cómo falla una garantía:
el agente SOUND está construido de forma que solo puede moverse hacia
casillas cuya seguridad ha sido demostrada.

En cambio, el agente reckless (imprudente) no hace esa comprobación
y el test demuestra que puede cometer ese error.

El motor lógico ya está implementado en dpll.py. Allí se encuentran:

- DPLL
- entails()
- las reglas físicas del mundo de Wumpus

Aquí NO estamos implementando nuevamente el razonador lógico.

Estamos construyendo el AGENTE encima de ese motor, específicamente
el paso ASK del ciclo:

    percibir → TELL → ASK → actuar

Todo lo que necesitamos para esta tarea es:

- entails() -> para preguntar qué puede demostrar la KB
- Pv()      -> para representar la proposición "hay un pozo"
"""

from dpll import Pv, entails


# ---- Tarea 1: paso ASK -------------------------------------------------------
# Cada una de estas funciones hace UNA pregunta a la base de conocimiento (KB)
# utilizando entailment lógico.

def provably_safe(kb, x, y) -> bool:
    """
    ¿La KB DEMUESTRA que NO existe un pozo en (x, y)?

    En lógica:

        KB ⊨ ¬P(x,y)

    Utilizamos:

        entails(kb, [frozenset({-Pv(x, y)})])

    Importante:
    Pv(x,y) representa P(x,y): "hay un pozo".

    Por lo tanto:

        -Pv(x,y)

    representa:

        ¬P(x,y): "NO hay un pozo".

    Se coloca dentro de frozenset porque la conclusión
    debe expresarse como una cláusula CNF.
    """

    # Preguntamos si la KB implica lógicamente:
    # "no existe un pozo en (x,y)".
    return entails(
        kb,
        [frozenset({-Pv(x, y)})]
    )


def provably_pit(kb, x, y) -> bool:
    """
    ¿La KB DEMUESTRA que existe un pozo en (x, y)?

    En lógica:

        KB ⊨ P(x,y)
    """

    # Pv(x,y) es positivo porque ahora preguntamos:
    # "¿La KB puede demostrar que SÍ existe un pozo?"
    return entails(
        kb,
        [frozenset({Pv(x, y)})]
    )


# ---- Tarea 1: paso ACT, de dos maneras --------------------------------------

def sound_frontier(kb, squares) -> list:
    """
    Agente SOUND (lógicamente correcto).

    Devuelve únicamente las casillas que están
    DEMOSTRADAS como seguras.

    Este es el punto principal de la semana:

    el agente solo se mueve a una casilla si puede demostrar:

        KB ⊨ ¬P(x,y)

    Si ninguna casilla está demostrada como segura,
    devuelve una lista vacía [].

    Un agente correcto puede entonces detenerse
    o decidir asumir un riesgo de forma explícita.

    Lo importante es que NUNCA considera UNKNOWN como SAFE.
    """

    # Recorremos todas las casillas candidatas.
    #
    # Solo conservamos aquellas donde provably_safe()
    # devuelve True.
    return [
        sq
        for sq in squares
        if provably_safe(kb, *sq)
    ]


def reckless_frontier(kb, squares) -> list:
    """
    Agente UNSOUND (imprudente).

    Este agente representa el ERROR que queremos observar.

    En vez de preguntar:

        "¿Puedo DEMOSTRAR que la casilla es segura?"

    pregunta solamente:

        "¿Puedo demostrar que existe un pozo?"

    y si la respuesta es NO, entra.

    Por lo tanto trata UNKNOWN como SAFE.

    Pero:

        "No puedo demostrar que hay un pozo"

    NO significa:

        "Puedo demostrar que no hay un pozo".

    Este es también el tipo de error que puede cometer
    un LLM en la Tarea 2:

        "probablemente seguro"

    no significa:

        "demostrablemente seguro".

    Si UNKNOWN realmente contiene un pozo,
    este agente puede morir al entrar.
    """

    # Incluimos cualquier casilla que NO esté
    # demostrada explícitamente como pozo.
    #
    # El problema es que esto incluye también UNKNOWN.
    return [
        sq
        for sq in squares
        if not provably_pit(kb, *sq)
    ]


# ---- Tarea 2: esquema — el LLM como razonador -------------------------------
#
# En la Tarea 2 se le dan al LLM exactamente las MISMAS percepciones,
# pero expresadas en lenguaje natural.
#
# Luego se comparan las casillas que el LLM afirma que son
# "ciertamente seguras" contra:
#
#     sound_frontier(kb, frontier)
#
# Si el LLM declara segura una casilla que NO aparece
# en sound_frontier(), entonces realizó una afirmación UNSOUND.
#
# Es decir, afirmó más de lo que la evidencia lógica permite demostrar.
#
# Este es el error importante que debe registrarse
# en el Failure Atlas.


if __name__ == "__main__":

    # Importamos herramientas adicionales solo para la demostración.
    from dpll import (
        kb_from_percepts,
        classify,
        load_scenarios
    )

    # Cargamos el escenario del mundo de Wumpus.
    sc = load_scenarios()["wumpus"]

    # Percepciones conocidas por el agente.
    base = sc["base_percepts"]

    # Casillas de frontera que podrían explorarse.
    # Las convertimos a tuplas (x, y).
    frontier = [
        tuple(s)
        for s in sc["frontier"]
    ]

    # Construimos la base de conocimiento (KB)
    # a partir de las percepciones.
    kb = kb_from_percepts(base)

    print(
        "Percepciones: "
        "(1,1) sin brisa, "
        "(2,1) con brisa.\n"
    )

    # Clasificamos cada casilla de la frontera.
    #
    # Puede resultar:
    # SAFE    -> demostrablemente segura
    # PIT     -> demostrablemente contiene pozo
    # UNKNOWN -> la KB no puede demostrar ninguna de las dos
    for (x, y) in frontier:

        print(
            f"  ({x},{y}): "
            f"{classify(kb, x, y)}"
        )

    # El agente SOUND solo entra donde puede
    # demostrar que NO existe un pozo.
    print(
        "\nsound_frontier :",
        sound_frontier(kb, frontier)
    )

    # El agente reckless entra en cualquier casilla
    # donde no se haya demostrado explícitamente un pozo.
    #
    # Por eso también puede incluir UNKNOWN.
    print(
        "reckless_frontier:",
        reckless_frontier(kb, frontier)
    )