"""Taller de la semana 5 — SOLUCIÓN DE REFERENCIA (solo para el docente).

Versión completada de ``starter.py``: conserva nombres y firmas para que
``test_alphabeta.py`` pase si se importa como ``starter``. El material
describe ``studios/_verify_solutions.py`` como verificador que registra este
archivo con ese nombre y ejecuta las pruebas sin modificarlas.

NO distribuir a estudiantes: se excluye mediante ``studios/.gitignore``.
La explicación está en ``solution.ipynb``, que importa este archivo sin copiarlo.

La idea central es la profundización iterativa: buscar a profundidad 1, 2, 3,
etc., conservar la mejor jugada de la última profundidad COMPLETADA y detenerse
al agotar el tiempo. Esto permite mantener una respuesta disponible mientras
se intenta mejorarla, una característica decisiva en el torneo.
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

    El orden estático ``CENTER_FIRST`` es fuerte en Conecta 4: las columnas
    centrales participan en más líneas ganadoras. Filtra esa lista para
    conservar las columnas jugables. Es una permutación de ``board.legal_moves()``.
    """
    # Comprensión de lista: recorre la prioridad estática y elimina las columnas llenas.
    # Devuelve una lista nueva; CENTER_FIRST y las casillas del tablero no cambian.
    return [c for c in CENTER_FIRST if c in board.legal_moves()]


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

    Tras cada profundidad completada, pone su mejor columna al inicio del
    orden para que la siguiente iteración la examine primero y pode más.
    """
    # perf_counter mide segundos; divide los milisegundos entre 1000 para calcular el instante límite.
    deadline = time.perf_counter() + time_budget_ms / 1000.0
    order = order_moves(board)
    # Guarda una respuesta disponible antes de buscar. Supone que order no está vacía.
    best = order[0]                       # regla 1: disponer siempre de una jugada legal
    # Prueba límites 1 a 42, máximo de fichas del tablero completo. Cada iteración vuelve a buscar desde la raíz.
    for depth in range(1, 43):
        # El reloj se comprueba SOLO entre profundidades. La llamada siguiente a alphabeta no recibe
        # deadline ni puede interrumpirse por tiempo aquí, así que una iteración larga puede sobrepasarlo.
        # Este comentario explica la implementación existente; no añade un control temporal nuevo.
        if time.perf_counter() >= deadline:
            break
        # -inf e inf dejan inicialmente abierta la ventana de poda; [0] es un contador mutable nuevo.
        # La búsqueda coloca y deshace fichas sobre el objeto board sin copiarlo por cada rama.
        value, move = alphabeta(board, depth, MAX, -inf, inf, [0], order)
        # Solo actualiza best después de que alphabeta regrese con la profundidad completa.
        if move is not None:
            best = move                   # regla 3: conservar la última profundidad completada
            # orden dinámico: en la siguiente iteración, prueba primero la mejor jugada anterior
            # Construye una lista nueva con best al frente y las demás columnas sin duplicarla.
            order = [best] + [c for c in order if c != best]
    # Entrega la última jugada disponible incluso si no hubo tiempo para la primera búsqueda.
    return best


# Esta prueba básica se ejecuta al lanzar el archivo; importarlo no ejecuta este bloque.
if __name__ == "__main__":
    # Prueba básica: elige una jugada en una posición inicial con un presupuesto de 500 ms.
    # Instanciación: b contiene sus propias casillas, alturas y registro de última jugada.
    b = Connect4()
    b.push(3, MAX)          # coloca una ficha MAX en el centro antes de elegir la jugada
    t0 = time.perf_counter()
    move = choose_move(b, 500)
    dt = (time.perf_counter() - t0) * 1000
    print(f"choose_move -> col {move}  ({dt:.0f} ms, budget 500)")
    assert move in b.legal_moves(), "returned an illegal column!"
    print("legal:", b.legal_moves())
