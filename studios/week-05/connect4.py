"""Taller de la semana 5 — Motor del juego (PROPORCIONADO; no modificar en el ejercicio).

Contiene el tablero de Conecta 4, ``minimax`` y ``alphabeta`` del notebook
de la sesión A, los órdenes estáticos de jugadas y la función de partidas
``play`` de las tres demostraciones. El taller trata de búsqueda adversarial
y orden de jugadas, no de volver a implementar el tablero. Escribe tu agente
del torneo, ``choose_move``, en ``starter.py``.

Decisiones de diseño del notebook:
    * ``push`` y ``pop`` MODIFICAN el tablero en el lugar. Copiar tableros
      a profundidad 7 generaría cientos de miles de objetos y dominaría el tiempo.
    * ``evaluate()`` puntúa desde la perspectiva de MAX: +10_000 si gana MAX,
      -10_000 si gana MIN; en otros casos usa grupos de fichas y control del centro.
    * ``alphabeta`` admite ``order``, una lista de prioridad de columnas:
      es el tema de la demostración 2.

Interfaz del notebook:
    board.legal_moves()            -> lista de columnas jugables
    board.push(col, player)        -> coloca una ficha de MAX o MIN
    board.pop(col)                 -> deshace la última ficha de esa columna
    board.winner()                 -> MAX / MIN / None
    board.full()                   -> bool
    board.evaluate()               -> entero desde la perspectiva de MAX
    minimax(board, depth, player, counter) -> (value, move)
    alphabeta(board, depth, player, alpha, beta, counter, order=None) -> (value, move)
"""
import time
from math import inf

ROWS, COLS, WIN = 6, 7, 4
# El tablero usa enteros: 0=vacío, MAX=1 y MIN=-1. Cambiar de turno equivale a negar el signo.
MAX, MIN = 1, -1        # MAX representa al jugador propio de la búsqueda


# POO: Connect4 es una clase que reúne el estado del tablero y los métodos para usarlo.
# b = Connect4() crea una instancia independiente; b.push(...) llama un método de esa instancia.
# No hay subclases propias en este módulo: la búsqueda se organiza con funciones que reciben el objeto.
class Connect4:
    # __init__ inicializa el objeto recién creado. Python pasa ese objeto como self automáticamente.
    # self.grid, self.heights y self.last son atributos de INSTANCIA, no variables compartidas entre tableros.
    def __init__(self):
        # La comprensión crea una lista distinta para cada fila, evitando que las filas compartan memoria.
        # La fila 0 es la inferior: las fichas se apilan hacia índices de fila mayores.
        self.grid = [[0] * COLS for _ in range(ROWS)]
        self.heights = [0] * COLS      # cantidad de fichas en cada columna
        self.last = None

    # ---- Mecánica del tablero ----------------------------------------
    # Método de consulta: devuelve una lista nueva con las columnas no llenas, sin modificar el tablero.
    def legal_moves(self):
        return [c for c in range(COLS) if self.heights[c] < ROWS]

    # Método que modifica el MISMO objeto: usa heights para localizar el primer espacio libre de la columna.
    # Supone que la columna es legal y player es MAX o MIN; no valida esos argumentos por su cuenta.
    def push(self, col, player):
        r = self.heights[col]
        self.grid[r][col] = player
        self.heights[col] += 1
        self.last = (r, col, player)

    # Deshace la ficha superior de una columna no vacía; la búsqueda lo llama tras explorar una jugada.
    # Restaura grid y heights, pero no restaura last. Las búsquedas de este módulo no consultan last.
    def pop(self, col):
        self.heights[col] -= 1
        r = self.heights[col]
        self.grid[r][col] = 0

    # all devuelve True solo si todas las columnas alcanzaron la altura ROWS.
    def full(self):
        return all(h == ROWS for h in self.heights)

    # ---- Comprobación de estados terminales --------------------------
    # El prefijo _ indica un auxiliar interno por convención; no impone privacidad automática.
    # Revisa cuatro casillas desde (r,c) en dirección (dr,dc), con límites y fichas iguales.
    def _line(self, r, c, dr, dc):
        p = self.grid[r][c]
        if p == 0:
            return None
        for k in range(1, WIN):
            rr, cc = r + dr * k, c + dc * k
            if not (0 <= rr < ROWS and 0 <= cc < COLS) or self.grid[rr][cc] != p:
                return None
        return p

    # Recorre cada casilla ocupada y prueba líneas horizontales, verticales y las dos diagonales.
    # Devuelve el entero del ganador; None significa que no encontró una línea ganadora.
    def winner(self):
        for r in range(ROWS):
            for c in range(COLS):
                if self.grid[r][c] == 0:
                    continue
                for dr, dc in ((0, 1), (1, 0), (1, 1), (1, -1)):
                    w = self._line(r, c, dr, dc)
                    if w:
                        return w
        return None

    # ---- Evaluación --------------------------------------------------
    # yield convierte este método en un generador: entrega un grupo de cuatro casillas cada vez.
    # No crea primero una lista con todos los grupos; la evaluación los consume durante el recorrido.
    def _windows(self):
        for r in range(ROWS):
            for c in range(COLS):
                for dr, dc in ((0, 1), (1, 0), (1, 1), (1, -1)):
                    rr, cc = r + dr * (WIN - 1), c + dc * (WIN - 1)
                    if 0 <= rr < ROWS and 0 <= cc < COLS:
                        yield [self.grid[r + dr * k][c + dc * k] for k in range(WIN)]

    def evaluate(self):
        """Valor heurístico desde la perspectiva de MAX."""
        w = self.winner()
        if w == MAX:
            return 10_000
        if w == MIN:
            return -10_000
        score = 0
        # Aquí win es una lista de cuatro casillas. Sus métodos count cuentan las fichas de cada jugador.
        # Un grupo con fichas de ambos jugadores no puede completarse para ninguno y se descarta.
        for win in self._windows():
            mx, mn = win.count(MAX), win.count(MIN)
            if mx and mn:
                continue                       # grupo bloqueado: no aporta a ninguno de los jugadores
            # El diccionario da más peso a dos y tres fichas alineadas que a una sola.
            # Los grupos de cuatro iguales ya quedaron resueltos por winner() al inicio de evaluate().
            if mx:
                score += {1: 1, 2: 10, 3: 50}[mx]
            elif mn:
                score -= {1: 1, 2: 10, 3: 50}[mn]
        # El centro vale más: conocimiento clásico del dominio de Conecta 4.
        for r in range(ROWS):
            if self.grid[r][COLS // 2] == MAX:
                score += 3
            elif self.grid[r][COLS // 2] == MIN:
                score -= 3
        return score

    # Método especial: print(board) o str(board) lo llaman para mostrar texto legible.
    # Invierte el orden de filas al imprimir: arriba aparece la fila superior y abajo la inferior.
    def __str__(self):
        sym = {0: ".", MAX: "X", MIN: "O"}
        rows = ["|" + " ".join(sym[self.grid[r][c]] for c in range(COLS)) + "|"
                for r in reversed(range(ROWS))]
        return "\n".join(rows) + "\n " + " ".join(str(c) for c in range(COLS))


# ---- minimax ----------------------------------------------------------------

# Función recursiva, no método: recibe una instancia Connect4 y alterna MAX/MIN en cada nivel.
# depth cuenta medias jugadas pendientes; counter es una lista mutable compartida por las llamadas.
# El resultado es (valor desde MAX, columna elegida); en un estado terminal la columna es None.
def minimax(board, depth, player, counter):
    # Cuenta cada llamada, incluidas las hojas y los estados terminales; no solo nodos con hijos generados.
    counter[0] += 1
    winner = board.winner()
    # Caso base: victoria, límite de profundidad o tablero lleno. La recursión vuelve con evaluate().
    if winner is not None or depth == 0 or board.full():
        return board.evaluate(), None

    best_move = None
    if player == MAX:
        # MAX busca el valor mayor; empieza con -infinito para aceptar la primera alternativa.
        best = -inf
        for move in board.legal_moves():
            # Explora sobre el tablero compartido; pop deberá deshacer esta ficha antes de probar otra columna.
            board.push(move, MAX)
            value, _ = minimax(board, depth - 1, MIN, counter)
            # Retroceso: restaura las casillas y alturas del tablero al estado previo a este intento.
            board.pop(move)
            if value > best:
                best, best_move = value, move
        return best, best_move
    else:
        # MIN busca el valor menor desde la misma perspectiva de MAX; empieza con +infinito.
        best = inf
        for move in board.legal_moves():
            board.push(move, MIN)
            value, _ = minimax(board, depth - 1, MAX, counter)
            # Retroceso: restaura las casillas y alturas del tablero al estado previo a este intento.
            board.pop(move)
            if value < best:
                best, best_move = value, move
        return best, best_move


# ---- Poda alfa-beta ---------------------------------------------------------

# Alfa-beta conserva el valor minimax para el mismo horizonte y una lista completa de jugadas.
# alpha es la cota inferior de MAX; beta, la superior de MIN. Si se cruzan, no hace falta seguir la rama.
# La poda puede cambiar qué jugada se elige entre empates, aunque conserve el mismo valor.
def alphabeta(board, depth, player, alpha, beta, counter, order=None):
    # Cuenta cada llamada, incluidas las hojas y los estados terminales; no solo nodos con hijos generados.
    counter[0] += 1
    winner = board.winner()
    # Caso base: victoria, límite de profundidad o tablero lleno. La recursión vuelve con evaluate().
    if winner is not None or depth == 0 or board.full():
        return board.evaluate(), None

    moves = board.legal_moves()
    # Filtra el orden recibido por legalidad. Para mantener todas las alternativas, order debe incluir
    # todas las columnas legales: las que falten en esa lista no se explorarán.
    if order is not None:
        moves = [c for c in order if c in moves]

    best_move = None
    if player == MAX:
        # MAX busca el valor mayor; empieza con -infinito para aceptar la primera alternativa.
        best = -inf
        for move in moves:
            # Explora sobre el tablero compartido; pop deberá deshacer esta ficha antes de probar otra columna.
            board.push(move, MAX)
            value, _ = alphabeta(board, depth - 1, MIN, alpha, beta, counter, order)
            # Retroceso: restaura las casillas y alturas del tablero al estado previo a este intento.
            board.pop(move)
            if value > best:
                best, best_move = value, move
            # Actualiza lo mejor que MAX puede asegurar entre las opciones examinadas.
            alpha = max(alpha, best)
            # Ya existe una alternativa suficiente en un ancestro: continuar esta rama no mejora su decisión.
            if alpha >= beta:
                break                      # aquí se aplica la poda
        return best, best_move
    else:
        # MIN busca el valor menor desde la misma perspectiva de MAX; empieza con +infinito.
        best = inf
        for move in moves:
            board.push(move, MIN)
            value, _ = alphabeta(board, depth - 1, MAX, alpha, beta, counter, order)
            # Retroceso: restaura las casillas y alturas del tablero al estado previo a este intento.
            board.pop(move)
            if value < best:
                best, best_move = value, move
            # Actualiza lo mejor que MIN puede asegurar para reducir el valor de MAX.
            beta = min(beta, best)
            # Ya existe una alternativa suficiente en un ancestro: continuar esta rama no mejora su decisión.
            if alpha >= beta:
                break
        return best, best_move


# ---- Órdenes estáticos de jugadas: demostración 2 ----------------------------
# Las columnas centrales son fuertes en Conecta 4: empezar por el centro es un buen orden
# estático. Estos son los mismos órdenes del notebook.
CENTER_FIRST = [3, 2, 4, 1, 5, 0, 6]
LEFT_TO_RIGHT = [0, 1, 2, 3, 4, 5, 6]
WORST = [0, 6, 1, 5, 2, 4, 3]


# ---- Enfrentamiento entre agentes: demostración 3 ----------------------------

def play(depth_max, depth_min, order=CENTER_FIRST, max_plies=42, verbose=False):
    """Enfrenta MAX y MIN con alfa-beta a distintas profundidades. Devuelve (winner, board)."""
    # Instancia un tablero nuevo para esta partida; cada llamada a play empieza desde cero.
    board = Connect4()
    player = MAX
    for ply in range(max_plies):
        if board.winner() is not None or board.full():
            break
        # Cada jugador puede mirar a distinta profundidad, pero usa la misma función de evaluación.
        d = depth_max if player == MAX else depth_min
        _, move = alphabeta(board, d, player, -inf, inf, [0], order)
        if move is None:
            break
        board.push(move, player)
        if verbose:
            print(f"ply {ply}: {'MAX' if player == MAX else 'MIN'} -> col {move}")
        # Con MAX=1 y MIN=-1, el cambio de signo alterna el turno.
        player = -player
    return board.winner(), board


# Al importar connect4 se definen clases y funciones; esta demostración solo corre al lanzar el archivo.
if __name__ == "__main__":
    # Demostración 1: misma respuesta con muchos menos nodos.
    def fresh():
        b = Connect4()
        b.push(3, MAX); b.push(3, MIN)
        return b

    print(f"  {'depth':>6}{'minimax':>12}{'alpha-beta':>13}{'speedup':>10}")
    print("  " + "-" * 45)
    for depth in (2, 4, 5, 6):
        # Cada algoritmo recibe su propio tablero y su propio contador para comparar resultados y trabajo.
        b1, c1 = fresh(), [0]
        v1, _ = minimax(b1, depth, MAX, c1)
        b2, c2 = fresh(), [0]
        v2, _ = alphabeta(b2, depth, MAX, -inf, inf, c2)
        assert v1 == v2, f"VALUES DIFFER at depth {depth}: {v1} vs {v2}"
        print(f"  {depth:>6}{c1[0]:>12,}{c2[0]:>13,}{c1[0] / c2[0]:>9.1f}x")
    print("\nAll values identical. Pruning changed the COST, not the ANSWER.")
