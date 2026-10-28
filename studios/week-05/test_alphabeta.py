"""Pruebas proporcionadas para el taller de la semana 5.

Ejecuta ``python3 test_alphabeta.py``. Se imprime una línea por prueba.

Hay dos grupos:
  * Las pruebas de la PLANTILLA comprueban ``choose_move`` y ``order_moves``
    en ``starter.py``. Indican que no están implementadas hasta completar los TODO.
  * Las pruebas de GARANTÍAS usan el motor de ``connect4.py`` y siempre se ejecutan:
    - ``test_alphabeta_matches_minimax_value_with_fewer_nodes``: alfa-beta
      conserva el valor de minimax visitando estrictamente menos nodos.
      La poda es exacta: solo descarta ramas demostrablemente irrelevantes.
    - ``test_horizon_effect_shallow_agent_loses``: observa deliberadamente
      el fallo de una garantía. Un agente de profundidad limitada no ve más
      allá de su horizonte y pierde frente a otro más profundo, aunque sus
      jugadas sean óptimas CON RESPECTO A SU HORIZONTE.
"""
# Estas pruebas son funciones con assert, no clases de unittest.TestCase.
# Importan la clase Connect4 y funciones del motor; s es el alias del módulo starter del estudiante.
import sys
import time
from math import inf

from connect4 import (Connect4, minimax, alphabeta, play,
                      MAX, MIN, CENTER_FIRST)
import starter as s


# ---- Posiciones de prueba compartidas ---------------------------------------

def _fresh():
    """Posición de demostración del notebook: MAX y MIN han jugado en el centro."""
    # POO: crea una instancia nueva con sus propias casillas y alturas para aislar cada prueba.
    b = Connect4()
    b.push(3, MAX); b.push(3, MIN)
    return b


def _immediate_win_for_max():
    """MAX ocupa las columnas 0, 1 y 2 de la fila inferior y le toca jugar.
    La columna 3 completa cuatro en línea AHORA: un agente que busca debe elegirla."""
    # POO: crea una instancia nueva con sus propias casillas y alturas para aislar cada prueba.
    b = Connect4()
    for col, p in [(0, MAX), (4, MIN), (1, MAX), (5, MIN), (2, MAX), (6, MIN)]:
        # Método de instancia: b se recibe como self, col indica la columna y p el jugador de esta ficha.
        b.push(col, p)
    return b            # jugada ganadora: columna 3


def _immediate_threat_against_max():
    """MIN tiene tres fichas verticales en la columna 3 y le toca a MAX.
    Si MAX no juega en la 3, MIN gana en la siguiente media jugada.
    La única columna que bloquea esa amenaza es la 3."""
    # POO: crea una instancia nueva con sus propias casillas y alturas para aislar cada prueba.
    b = Connect4()
    for col, p in [(0, MAX), (3, MIN), (1, MAX), (3, MIN), (2, MAX), (3, MIN)]:
        # Método de instancia: b se recibe como self, col indica la columna y p el jugador de esta ficha.
        b.push(col, p)
    return b            # jugada de bloqueo: columna 3


# ---- Pruebas de la PLANTILLA: requieren completar starter.py -----------------

def test_order_moves_is_a_legal_permutation():
    b = _fresh()
    order = s.order_moves(b)
    legal = b.legal_moves()
    # Compara contenido sin importar el orden. Detecta columnas omitidas, extra o duplicadas.
    # No exige una prioridad concreta: el estudiante puede diseñar su propio orden.
    assert sorted(order) == sorted(legal), (
        f"order_moves must return exactly the legal columns; got {order} "
        f"for legal {legal}")
    print("  ok  order_moves returns the legal columns, reordered")


def test_choose_move_returns_legal_column():
    for b in (Connect4(), _fresh(), _immediate_threat_against_max()):
        move = s.choose_move(b, 300)
        # legal_moves() consulta el tablero; el valor devuelto debe ser un índice de columna disponible.
        assert move in b.legal_moves(), f"choose_move returned illegal col {move}"
    print("  ok  choose_move always returns a legal column")


def test_choose_move_takes_the_immediate_win():
    b = _immediate_win_for_max()
    # s.choose_move es una función del módulo, no un método del tablero; recibe b como argumento explícito.
    move = s.choose_move(b, 500)
    assert move == 3, (
        f"choose_move missed a one-move win: played {move}, should play 3. "
        "This is the exact failure the LLM challenger shows in class — do not "
        "reproduce it with a real search.")
    print("  ok  choose_move takes the immediate win (col 3)")


def test_choose_move_blocks_the_immediate_threat():
    b = _immediate_threat_against_max()
    # s.choose_move es una función del módulo, no un método del tablero; recibe b como argumento explícito.
    move = s.choose_move(b, 500)
    assert move == 3, (
        f"choose_move failed to block MIN's vertical threat: played {move}, "
        "must play 3.")
    print("  ok  choose_move blocks the immediate threat (col 3)")


def test_choose_move_respects_the_time_budget():
    # Un agente con respuesta disponible debe devolverla pronto con poco tiempo, sin
    # perder por excederlo. Se permite margen generoso por recolección de basura o cachés frías.
    b = _fresh()
    budget_ms = 300
    t0 = time.perf_counter()
    move = s.choose_move(b, budget_ms)
    # Convierte la diferencia de segundos a milisegundos para compararla con budget_ms.
    elapsed_ms = (time.perf_counter() - t0) * 1000
    assert move in b.legal_moves()
    # La prueba admite 2000 ms adicionales: superarla no demuestra por sí sola un límite estricto de 300 ms.
    # La condición temporal original se conserva exactamente.
    assert elapsed_ms < budget_ms + 2000, (
        f"choose_move took {elapsed_ms:.0f} ms on a {budget_ms} ms budget — "
        "it is not stopping between depths. In the tournament this forfeits.")
    print(f"  ok  choose_move respected the budget ({elapsed_ms:.0f} ms / {budget_ms} ms)")


# ---- Pruebas de GARANTÍAS: usan el motor proporcionado y siempre se ejecutan --

def test_alphabeta_matches_minimax_value_with_fewer_nodes():
    """La garantía relevante: mismo valor con estrictamente menos nodos."""
    for depth in (2, 4, 5, 6):
        # Dos tableros equivalentes y dos listas contador distintas: evita mezclar los datos de las búsquedas.
        # counter[0] puede modificarse dentro de todas las llamadas recursivas que comparten esa lista.
        b1, c1 = _fresh(), [0]
        v_mini, _ = minimax(b1, depth, MAX, c1)
        b2, c2 = _fresh(), [0]
        v_ab, _ = alphabeta(b2, depth, MAX, -inf, inf, c2, CENTER_FIRST)
        # Se exige igualdad de VALOR. Dos columnas distintas podrían empatar y ser igualmente óptimas.
        assert v_mini == v_ab, (
            f"α-β changed the ANSWER at depth {depth}: {v_mini} vs {v_ab}. "
            "That is a bug — pruning must be exact.")
        # Estos contadores incluyen también hojas y estados terminales: miden llamadas visitadas.
        assert c2[0] < c1[0], (
            f"α-β did not expand fewer nodes at depth {depth}: "
            f"{c2[0]} !< {c1[0]}")
    print("  ok  α-β returns minimax's value while expanding fewer nodes")


def test_horizon_effect_shallow_agent_loses():
    """Fallo deliberado de una garantía: el jugador de menor profundidad pierde.
    play(2, 5) -> gana MIN, el más profundo; play(6, 4) -> gana MAX, el más profundo.

    En el notebook, play(5, 5) también da la victoria a MIN, pero es un efecto
    particular de ``evaluate()`` con igual profundidad, NO el efecto horizonte.
    Por eso esta prueba no exige ese resultado.
    """
    # play devuelve (ganador, tablero final); _ descarta el objeto tablero en esta comprobación.
    # Ambos usan alfa-beta y la misma evaluación; aquí cambia la profundidad de cada jugador.
    w_shallow_max, _ = play(2, 5)
    assert w_shallow_max == MIN, (
        f"expected the depth-5 side (MIN) to beat the depth-2 side; got {w_shallow_max}")
    w_deep_max, _ = play(6, 4)
    assert w_deep_max == MAX, (
        f"expected the depth-6 side (MAX) to beat the depth-4 side; got {w_deep_max}")
    print("  ok  horizon effect: the shallow agent loses to the deeper one")


# Las funciones son objetos: esta lista guarda sus referencias y main las llama después con t().
TESTS = [
    test_order_moves_is_a_legal_permutation,
    test_choose_move_returns_legal_column,
    test_choose_move_takes_the_immediate_win,
    test_choose_move_blocks_the_immediate_threat,
    test_choose_move_respects_the_time_budget,
    test_alphabeta_matches_minimax_value_with_fewer_nodes,
    test_horizon_effect_shallow_agent_loses,
]


def main():
    # Ejecuta todas las pruebas, contabilizando tanto ejercicios pendientes como aserciones fallidas.
    failed = 0
    for t in TESTS:
        try:
            t()
        # Aparece mientras starter conserve las instrucciones de tarea pendiente; no se completan aquí.
        except NotImplementedError:
            print(f"  --  {t.__name__}: starter not implemented yet")
            failed += 1
        # e es el objeto excepción que contiene el mensaje de la condición fallida.
        except AssertionError as e:
            print(f"  FAIL {t.__name__}: {e}")
            failed += 1
    if failed:
        print(f"\n{failed}/{len(TESTS)} failed")
        # Un código de salida 1 señala fallos al sistema; si todo pasa, main termina normalmente con 0.
        sys.exit(1)
    print(f"\nall {len(TESTS)} tests pass")


# Al importar el módulo solo define las pruebas; al lanzarlo directamente ejecuta main().
if __name__ == "__main__":
    main()
