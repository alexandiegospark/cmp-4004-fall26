"""Pruebas proporcionadas para el taller de la semana 2.

Ejecuta ``python3 test_agents.py``. Se imprime una línea por prueba.

Dos pruebas comprueban deliberadamente una propiedad sorprendente:

  - ``test_reflex_fails_under_partial_observability``: el agente reactivo simple
    deja de manera DEMOSTRABLE una habitación sucia con el sensor de ubicación
    averiado, mientras el agente basado en modelos limpia ambas. Observa el
    fallo de una garantía. Solo usa los agentes proporcionados, así que pasa
    antes de completar ``starter.py``.

  - ``test_utility_leaves_a_room_dirty``: el agente racional de utilidad deja
    una habitación sucia en al menos una configuración. Es racionalidad bajo
    un modelo de costo, no un error.
"""
# Las pruebas son funciones con assert, no clases de unittest.TestCase.
# Usan los objetos del entorno y las fábricas de agentes; no cambian las políticas que evalúan.
import sys

from vacuum import (VacuumWorld, BrokenSensorWorld, run, run_in,
                    simple_reflex, model_based)
from tournament import load_configs, net_utility
import starter as s

# Lee las ocho configuraciones del JSON una vez al importar el módulo.
CONFIGS = load_configs()


def _final(agent_or_factory, dirt, loc, steps=20, broken=False):
    """Ejecuta un agente durante los pasos indicados y devuelve el mundo resultante.

    Acepta la función directa del agente reactivo o una fábrica para los agentes
    basados en modelos, objetivos o utilidad.
    """
    # POO: crea una instancia de la clase base o de su subclase según broken.
    # Ambas ofrecen percept() y step(); run_in puede usarlas por la misma interfaz.
    world = BrokenSensorWorld(dirt, loc) if broken else VacuumWorld(dirt, loc)
    # Si es una fábrica, la llama para obtener un agente con memoria nueva.
    # Si es simple_reflex, conserva la función directamente: esta necesita una percepción como argumento.
    agent = agent_or_factory() if callable_is_factory(agent_or_factory) else agent_or_factory
    # run_in modifica el mismo objeto world y lo devuelve para consultar su estado final.
    return run_in(world, agent, steps)


def callable_is_factory(fn):
    """model_based, goal_based y utility_based son fábricas de cero argumentos;
    simple_reflex ya es el agente. Probar una llamada sin argumentos para
    distinguirlos es inseguro: se identifica explícitamente al reactivo."""
    # is compara identidad de objetos función, no nombres ni resultados de llamadas.
    # Esta regla está diseñada para estos agentes: cualquier función distinta se trata como fábrica.
    return fn is not simple_reflex


# ---- Garantía de agentes proporcionados: pasa aunque starter esté pendiente --

def test_reflex_fails_under_partial_observability():
    """simple_reflex falla en al menos una configuración con el sensor de
    ubicación averiado; model_based sigue limpiando AMBAS habitaciones.

    Alcance: solo configuraciones que comienzan en la habitación 0, donde la
    creencia inicial fija de model_based (loc=0) es correcta. Su memoria solo
    es tan fiable como esa creencia inicial: merece comentarse en la puesta
    en común. Aquí se mantiene correcta para aislar memoria frente a ausencia
    de memoria.
    """
    # Filtra la lista para que la creencia inicial loc=0 coincida con la ubicación real.
    # Así la prueba compara presencia de memoria, sin introducir un error inicial distinto.
    loc0 = [(dirt, loc) for dirt, loc in CONFIGS if loc == 0]
    reflex_failures = 0
    for dirt, loc in loc0:
        # el agente basado en modelos debe limpiar ambas habitaciones incluso con el sensor averiado:
        wm = _final(model_based, dirt, loc, broken=True)
        # wm es una instancia: .dirt consulta su atributo público con el estado real de ambas habitaciones.
        # assert lanza AssertionError si el estado no coincide con el resultado requerido.
        assert wm.dirt == [False, False], (
            f"model_based left a room dirty on broken-sensor dirt={dirt} loc={loc}: {wm}"
        )
        # el reactivo puede fallar: cuenta esos casos:
        wr = _final(simple_reflex, dirt, loc, broken=True)
        if wr.dirt != [False, False]:
            reflex_failures += 1
    # Se espera que el reactivo falle al menos una vez: demostrar su limitación hace pasar esta prueba.
    assert reflex_failures > 0, (
        "simple_reflex cleaned every broken-sensor world — the partial-"
        "observability failure did not reproduce (check BrokenSensorWorld)."
    )
    print(f"  ok  reflex failed on {reflex_failures}/{len(loc0)} broken-sensor "
          f"configs; model_based cleaned all (and that is the lesson)")


# ---- Agente basado en objetivos: requiere completar starter -----------------

def test_goal_based_reaches_goal_on_every_config():
    for dirt, loc in CONFIGS:
        # s es el alias del módulo starter; s.goal_based es la fábrica que escribió el estudiante.
        w = _final(s.goal_based, dirt, loc)
        assert w.dirt == [False, False], (
            f"goal_based did not reach the goal on dirt={dirt} loc={loc}: {w}"
        )
    print("  ok  goal_based reaches (both rooms clean) on all 8 configs")


def test_goal_based_stops_when_done():
    # Una vez limpio el mundo, el agente basado en objetivos debe devolver NoOp, sin oscilar.
    # Crea una política con memoria nueva para este episodio.
    agent = s.goal_based()
    # Instancia con ambas habitaciones sucias y ubicación inicial 0.
    w = VacuumWorld((True, True), 0)
    run_in(w, agent, steps=20)                 # avanzar hasta el estado objetivo limpio
    assert w.dirt == [False, False]
    # Con el mundo limpio, las acciones siguientes deben ser NoOp: sin costo ni desplazamiento.
    # Guarda la posición antes de comprobar cinco acciones adicionales sobre el mismo objeto.
    loc_before = w.loc
    for _ in range(5):
        # Método de observación del mundo → función de decisión del agente.
        a = agent(w.percept())
        assert a == "NoOp", f"goal_based kept acting after the goal was reached: {a!r}"
        # step() aplica NoOp: no debe mover al agente; tiempo y puntuación sí continúan.
        w.step(a)
    assert w.loc == loc_before
    print("  ok  goal_based returns NoOp once the goal is reached (does not oscillate)")


# ---- Agente basado en utilidad: requiere completar starter ------------------

def test_utility_cleans_the_room_it_starts_in():
    # Una habitación inicial sucia recupera pronto el costo de aspirar, así que un agente racional
    # la limpia. En estas configuraciones, dirt[loc] es True.
    for dirt, loc in CONFIGS:
        # Omite configuraciones cuya habitación inicial ya estaba limpia: no prueban la limpieza.
        if not dirt[loc]:
            continue
        w = _final(s.utility_based, dirt, loc)
        # Comprueba la habitación de inicio, no exige que el agente de utilidad limpie ambas.
        assert w.dirt[loc] is False, (
            f"utility_based never cleaned its own starting room dirt={dirt} loc={loc}: {w}"
        )
    print("  ok  utility_based always cleans the (dirty) room it starts in")


def test_utility_leaves_a_room_dirty():
    """El descubrimiento: un agente voraz de utilidad deja al menos una habitación
    sucia en al menos una configuración porque viajar a una habitación que no
    ve no compensa de inmediato."""
    # Cuenta configuraciones con suciedad final: no cuenta el número total de habitaciones sucias.
    left_dirty = 0
    for dirt, loc in CONFIGS:
        w = _final(s.utility_based, dirt, loc)
        if w.dirt != [False, False]:
            left_dirty += 1
    # El resultado esperado es dejar suciedad en algún caso por el criterio voraz, no por azar.
    assert left_dirty > 0, (
        "utility_based cleaned every world — with this cost model a purely "
        "greedy agent should leave at least one room dirty. Make it weigh the "
        "IMMEDIATE net change of crossing, not the whole horizon."
    )
    print(f"  ok  utility_based rationally left a room dirty on {left_dirty}/{len(CONFIGS)} "
          f"configs (and that is the lesson)")


# Las funciones son objetos: esta lista guarda sus referencias, sin ejecutarlas todavía.
TESTS = [
    test_reflex_fails_under_partial_observability,
    test_goal_based_reaches_goal_on_every_config,
    test_goal_based_stops_when_done,
    test_utility_cleans_the_room_it_starts_in,
    test_utility_leaves_a_room_dirty,
]


def main():
    # El ejecutor llama a cada función, cuenta fallos y devuelve un código de salida al sistema.
    failed = 0
    for t in TESTS:
        try:
            # t contiene una función de TESTS; los paréntesis ejecutan esa prueba.
            t()
        # Esta excepción indica que falta implementar un agente en starter; no es un comentario TODO.
        except NotImplementedError:
            print(f"  --  {t.__name__}: agent not implemented yet")
            failed += 1
        # e es el objeto excepción de una aserción fallida; su mensaje describe la discrepancia.
        except AssertionError as e:
            print(f"  FAIL {t.__name__}: {e}")
            failed += 1
    if failed:
        print(f"\n{failed}/{len(TESTS)} failed")
        # Código 1: hubo pruebas fallidas. Si todo pasa, main termina normalmente con código 0.
        sys.exit(1)
    print(f"\nall {len(TESTS)} tests pass")


# Al lanzar el archivo ejecuta main(); al importarlo deja disponibles las funciones de prueba.
if __name__ == "__main__":
    main()
