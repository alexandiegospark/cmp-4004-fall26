"""Taller de la semana 4 — Motor de búsqueda compartido (PROPORCIONADO; no modificar en el ejercicio).

Contiene A* del notebook de la sesión A y una cuadrícula con costos de terreno.
El taller trata de heurísticas, no de volver a implementar A*: la búsqueda
se proporciona y las heurísticas se escriben en ``starter.py``.

Costos de terreno: se cobran al ENTRAR en una celda.
    '.'  camino = 1
    ','  hierba = 3
    '~'  agua = 8
    'S'  inicio: costo 1 si se vuelve a entrar en él
    'G'  objetivo: costo 1 al entrar

Interfaz compatible con la semana 3 y el notebook:
    problem.actions(state)        -> tupla de movimientos legales ('U'/'D'/'L'/'R')
    problem.result(state, action) -> siguiente estado
    problem.is_goal(state)        -> bool
    problem.step_cost(s, action)  -> costo de entrar en la celda de destino
    astar(problem, h)             -> (goal_node, expansions) o (None, expansions)
    node.path()                   -> lista de movimientos; node.g -> costo del camino
"""
import heapq
import json
from pathlib import Path

# Diccionarios compartidos: TERRAIN traduce símbolos a costos y MOVES a cambios de coordenadas.
# Las letras de acción se conservan: U=arriba, D=abajo, L=izquierda, R=derecha.
TERRAIN = {".": 1, ",": 3, "~": 8, "S": 1, "G": 1}
MOVES = {"U": (-1, 0), "D": (1, 0), "L": (0, -1), "R": (0, 1)}
MIN_COST = min(TERRAIN.values())   # = 1
MAX_COST = max(TERRAIN.values())   # = 8


# POO: Node es una clase; cada instancia representa un camino hasta un estado de la cuadrícula.
# El estado indica dónde estamos; parent, action y g registran cómo llegamos y cuánto costó.
# Dos nodos pueden tener el mismo state y representar caminos de distinto costo.
class Node:
    # Limita los atributos de cada instancia a estos cuatro nombres y reduce memoria.
    # No hace al nodo inmutable: sus atributos declarados pueden cambiar.
    __slots__ = ("state", "parent", "action", "g")

    # __init__ inicializa la instancia. Python pasa automáticamente ese objeto como self.
    # Node(s, padre, accion, costo) guarda una referencia al nodo padre: composición de objetos.
    def __init__(self, state, parent=None, action=None, g=0):
        self.state, self.parent, self.action, self.g = state, parent, action, g

    # Método de instancia: node.path() usa node como self y devuelve las acciones del camino.
    # Recorre enlaces hacia atrás sin modificar los nodos; al final invierte la lista construida.
    def path(self):
        node, out = self, []
        while node.parent is not None:
            out.append(node.action)
            node = node.parent
        return out[::-1]


# Esta clase no hereda de una clase Problem: ofrece la interfaz que astar necesita.
# Es tipado por comportamiento: basta con exponer initial y los métodos de transición y costo.
# El objeto problema describe el mundo; los objetos Node guardan los caminos que explora A*.
class GridProblem:
    """Cuadrícula con costos de terreno. El estado es una tupla (fila, columna)."""

    # GridProblem(grid) crea una instancia con atributos propios: grid, rows, cols, initial y goal.
    # self identifica esa instancia en cada método; no es el estado (fila, columna) que se explora.
    def __init__(self, grid):
        # grid: lista de cadenas con filas de igual longitud; contiene exactamente una S y una G.
        # Guarda la referencia recibida, sin copiar la lista. Este módulo solo la consulta.
        self.grid = grid
        self.rows, self.cols = len(grid), len(grid[0])
        self.initial = self._find("S")
        self.goal = self._find("G")

    # El prefijo _ marca un auxiliar interno por convención, no impide llamarlo desde fuera.
    # enumerate entrega el índice de fila y su cadena; str.find devuelve -1 si no halla el símbolo.
    def _find(self, ch):
        for r, row in enumerate(self.grid):
            c = row.find(ch)
            if c != -1:
                return (r, c)
        raise ValueError(f"grid has no {ch!r}")

    # Predicado: True solo si la fila y la columna están dentro de la cuadrícula.
    def _in_bounds(self, r, c):
        return 0 <= r < self.rows and 0 <= c < self.cols

    # Desempaqueta el estado y consulta el costo del símbolo de esa celda.
    def cost_of(self, state):
        r, c = state
        return TERRAIN[self.grid[r][c]]

    # Genera movimientos que no salen del tablero. No hay paredes en estos terrenos:
    # camino, hierba y agua son transitables, con distinto costo.
    def actions(self, state):
        r, c = state
        return tuple(m for m, (dr, dc) in MOVES.items()
                     if self._in_bounds(r + dr, c + dc))

    # Devuelve una tupla nueva; no modifica initial ni mueve un objeto dentro del problema.
    # Supone que action fue elegida entre las acciones legales del estado.
    def result(self, state, action):
        dr, dc = MOVES[action]
        return (state[0] + dr, state[1] + dc)

    def is_goal(self, state):
        return state == self.goal

    def step_cost(self, state, action):
        # Invoca dos métodos del mismo objeto: calcula el destino y cobra el costo de entrar en él.
        return self.cost_of(self.result(state, action))


def astar(problem, h):
    """A* del notebook. Devuelve (goal_node, expansions)."""
    # Crea el nodo raíz con costo g=0: estar inicialmente en S no cobra un paso de entrada.
    # h es un objeto función recibido como argumento y se invoca con (problem, state).
    start = Node(problem.initial)
    frontier = [(h(problem, start.state), 0, start)]   # (f, desempate, nodo)
    # Guarda el menor costo conocido por ESTADO, no por identidad de objeto Node.
    # Las tuplas de enteros son hashables y pueden usarse como claves del diccionario.
    best_g = {problem.initial: 0}
    expansions, tiebreak = 0, 0
    while frontier:
        # heapq extrae la tupla con menor f=g+h; el contador desempata antes de comparar nodos.
        _, _, node = heapq.heappop(frontier)
        # Comprueba el objetivo al retirar el nodo de la frontera, no cuando lo genera.
        # La garantía de costo óptimo depende de la heurística y de las condiciones de búsqueda.
        if problem.is_goal(node.state):
            return node, expansions
        # Puede quedar en el montículo un camino antiguo hacia un estado cuyo costo ya mejoró.
        # dict.get usa infinito como valor por defecto; las entradas peores se descartan.
        if node.g > best_g.get(node.state, float("inf")):
            continue                                    # entrada obsoleta
        expansions += 1
        for action in problem.actions(node.state):
            s2 = problem.result(node.state, action)
            g2 = node.g + problem.step_cost(node.state, action)
            # Solo inserta una mejora estricta. Puede volver a explorar un estado si llega más barato;
            # no hay un conjunto cerrado que prohíba todas las visitas posteriores.
            if g2 < best_g.get(s2, float("inf")):
                best_g[s2] = g2
                # Un contador único evita comparar directamente objetos Node, que no definen orden.
                tiebreak += 1
                heapq.heappush(frontier,
                               (g2 + h(problem, s2), tiebreak,
                                Node(s2, node, action, g2)))
    return None, expansions


# ---- Carga de instancias ----------------------------------------------------

def load_instances(path=None):
    """Carga el banco proporcionado como {size: [grid, ...]}; cada cuadrícula es
    una lista de cadenas. Véase instances.json, generado con semilla fija."""
    # POO: Path es una clase; with_name construye una ruta junto a este módulo.
    # read_text es un método de ese objeto y json.loads convierte el texto en datos Python.
    path = Path(path or Path(__file__).with_name("instances.json"))
    data = json.loads(path.read_text())
    return {int(k): v for k, v in data["instances"].items()}


# Los métodos str.join separan celdas por espacios y filas por saltos de línea, sin modificar grid.
def render(grid):
    return "\n".join(" ".join(row) for row in grid)
