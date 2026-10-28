"""Taller de la semana 5 — Tu agente para el torneo.

El motor, con tablero, ``minimax``, ``alphabeta``, órdenes estáticos y
``play``, se proporciona en ``connect4.py`` y no debe modificarse en el
ejercicio. Implementa un agente con límite temporal y una respuesta disponible:

    def choose_move(board, time_budget_ms) -> int

Reglas estrictas del plan: 500 ms por jugada, sin procesos externos, sin red y
sin libro de aperturas de más de 20 posiciones. El agente de referencia del
torneo usa alfa-beta a profundidad 6: compite mediante profundidad de búsqueda.

Completa ambas funciones y ejecuta ``python3 test_alphabeta.py``. Las pruebas
de tu agente deben pasar; las dos de garantías usan el motor proporcionado y
muestran qué aportan la poda y qué limita el efecto horizonte.

Una profundidad fija puede terminar demasiado pronto o superar los 500 ms y
perder la partida. La profundización iterativa busca a profundidades 1, 2, 3,
etc., conservando la mejor jugada de la última profundidad COMPLETADA mientras
intenta mejorarla. Esa respuesta disponible es esencial en el torneo.
"""
import time
from math import inf

# Connect4 es la clase del tablero; alphabeta es una función que recibe ese objeto y lo explora.
# order_moves y choose_move son funciones, no métodos de una clase de agente.
from connect4 import Connect4, alphabeta, MAX, CENTER_FIRST


# board es una instancia de Connect4; board.legal_moves() consulta su estado mediante un método.
# Ordenar las alternativas no coloca fichas ni modifica el tablero.
def order_moves(board):
    """Devuelve las columnas legales en el orden en que alfa-beta debe probarlas.

    El mejor caso O(b^(m/2)), que duplica la profundidad alcanzable, requiere
    examinar primero las jugadas fuertes. Un buen orden estático comienza por
    el centro: ``CENTER_FIRST`` de connect4.py. Como ampliación, prueba un
    orden dinámico que empiece por la mejor jugada de la iteración anterior.
    """
    # TODO marca trabajo pendiente y no se ejecuta: es un comentario.
    # raise NotImplementedError sí detiene la llamada hasta que implementes la función.
    # TODO: devuelve las jugadas legales de `board`, de mejor a peor.
    #   Mínimo: [c for c in CENTER_FIRST if c in board.legal_moves()]
    # Se conserva la tarea pendiente del ejercicio: reemplázala al escribir tu implementación.
    raise NotImplementedError


# El agente devuelve un índice de columna, no un tablero ni una evaluación.
# -> int es una anotación de tipo; Python no comprueba automáticamente ese contrato al ejecutar.
# Esta interfaz supone que quedan jugadas legales y evalúa siempre desde la perspectiva de MAX.
def choose_move(board, time_budget_ms) -> int:
    """Devuelve la columna que debe jugar MAX con profundización iterativa y alfa-beta.

    Contrato del torneo:
      1. Devolver SIEMPRE una columna legal incluso con poco tiempo: inicializa
         `best` con una jugada legal antes del bucle para no devolver None.
      2. No exceder mucho `time_budget_ms`: comprobar el reloj entre profundidades
         y detenerse cuando se agote el presupuesto.
      3. Conservar la mejor jugada de la última profundidad COMPLETADA, no una
         estimación parcial de una iteración sin terminar.

    Llama a ``alphabeta(board, depth, MAX, -inf, inf, counter, order)`` con
    profundidades crecientes. Usa ``order=order_moves(board)`` para favorecer
    la poda. Una profundidad sin terminar puede sugerir una jugada peor que
    la obtenida en la última iteración completa.
    """
    # El esquema siguiente es código comentado: Python no lo ejecuta.
    # Comprueba el reloj entre profundidades, pero alphabeta no tiene interrupción temporal interna;
    # no equivale a garantizar un límite estricto de 500 ms dentro de una iteración larga.
    # TODO: implementa la profundización iterativa.
    #   deadline = time.perf_counter() + time_budget_ms / 1000.0
    #   order = order_moves(board)
    #   best = order[0]                       # regla 1: disponer siempre de una jugada legal
    #   for depth in range(1, 43):
    #       if time.perf_counter() >= deadline:
    #           break
    #       value, move = alphabeta(board, depth, MAX, -inf, inf, [0], order)
    #       if move is not None:
    #           best = move                   # regla 3: conservar la última profundidad completada
    #   return best
    # Se conserva la tarea pendiente del ejercicio: reemplázala al escribir tu implementación.
    raise NotImplementedError


# Esta prueba básica se ejecuta al lanzar el archivo; importarlo no ejecuta este bloque.
if __name__ == "__main__":
    # Prueba básica: elige una jugada en una posición inicial con un presupuesto de 500 ms.
    # Instanciación: b contiene sus propias casillas, alturas y registro de última jugada.
    b = Connect4()
    b.push(3, MAX)          # coloca una ficha MAX en el centro antes de elegir la jugada
    try:
        t0 = time.perf_counter()
        move = choose_move(b, 500)
        dt = (time.perf_counter() - t0) * 1000
        print(f"choose_move -> col {move}  ({dt:.0f} ms, budget 500)")
        assert move in b.legal_moves(), "returned an illegal column!"
        print("legal:", b.legal_moves())
    # Captura el estado pendiente para mostrar el mensaje de la plantilla sin completar el ejercicio.
    except NotImplementedError:
        print("choose_move / order_moves not implemented yet — fill them in.")
