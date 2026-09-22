"""
Studio de la Semana 3 — motor de búsqueda compartido.

Este archivo contiene la búsqueda genérica que se reutilizará después.
La idea principal es que BFS, DFS y UCS utilizan el mismo ciclo de búsqueda;
lo que cambia es únicamente la forma en que funciona la frontera.

NO se debe modificar este archivo.
Los algoritmos y problemas que debes desarrollar van en starter.py.
"""

from collections import deque
import heapq
import itertools
import json
from pathlib import Path


# ============================================================
# CLASE PROBLEM
# ============================================================

class Problem:
    """
    Clase base que representa un problema de búsqueda.

    Define los cinco componentes principales:
    1. Estado inicial.
    2. Acciones posibles.
    3. Función de transición.
    4. Prueba de objetivo.
    5. Costo de cada acción.

    Las clases concretas, como EightPuzzle o TinyGraph,
    HEREDAN de Problem y sobrescriben los métodos necesarios.
    """

    def __init__(self, initial, goal=None):
        # Guarda el estado inicial y el estado objetivo.
        self.initial, self.goal = initial, goal

    def actions(self, state):
        # Debe retornar las acciones legales desde un estado.
        # Las clases hijas deben implementar este método.
        raise NotImplementedError

    def result(self, state, action):
        # Debe retornar el nuevo estado después de aplicar una acción.
        # Las clases hijas deben implementar este método.
        raise NotImplementedError

    def is_goal(self, state):
        # Retorna True si el estado actual es igual al objetivo.
        return state == self.goal

    def step_cost(self, state, action):
        # Por defecto, cada acción cuesta 1.
        return 1


# ============================================================
# CLASE NODE
# ============================================================

class Node:
    """
    Representa un nodo dentro del árbol/grafo de búsqueda.

    Un nodo guarda:
    - state: estado actual.
    - parent: nodo desde el cual llegamos.
    - action: acción utilizada para llegar aquí.
    - g: costo acumulado desde el inicio.
    """

    # __slots__ limita los atributos que puede tener cada objeto Node.
    # También reduce el uso de memoria.
    __slots__ = ("state", "parent", "action", "g")

    def __init__(self, state, parent=None, action=None, g=0):
        # Guardamos toda la información del nodo.
        self.state, self.parent, self.action, self.g = state, parent, action, g

    def path(self):
        """
        Reconstruye el camino desde el nodo inicial hasta este nodo.

        Retorna:
            Una lista con las acciones realizadas.
        """

        # Empezamos desde el nodo actual.
        node, out = self, []

        # Retrocedemos siguiendo los nodos padre.
        while node.parent is not None:

            # Guardamos la acción que permitió llegar al nodo actual.
            out.append(node.action)

            # Retrocedemos al nodo padre.
            node = node.parent

        # Como recorrimos el camino desde el final hacia el inicio,
        # invertimos la lista antes de retornarla.
        return out[::-1]

    def __repr__(self):
        # Define cómo se muestra un objeto Node al imprimirlo.
        return f"Node({self.state}, g={self.g})"


# ============================================================
# CLASE FRONTIER
# ============================================================

class Frontier:
    """
    Representa la frontera de la búsqueda.

    La estructura utilizada determina el algoritmo:

    FIFO     -> BFS
    LIFO     -> DFS
    Priority -> UCS

    El ciclo principal de búsqueda es el mismo.
    Solo cambia la disciplina de la frontera.
    """

    def __init__(self, kind):

        # Guardamos qué tipo de frontera queremos.
        self.kind = kind

        # Este contador sirve para desempatar elementos
        # con el mismo costo dentro de la cola de prioridad.
        self.counter = itertools.count()

        # BFS y DFS utilizan deque.
        if kind in ("fifo", "lifo"):
            self.data = deque()

        # UCS utiliza una cola de prioridad implementada con heap.
        elif kind == "priority":
            self.data = []

        # Si se recibe un tipo inválido, generamos un error.
        else:
            raise ValueError(kind)

    def push(self, node):
        """
        Agrega un nodo a la frontera.
        """

        if self.kind == "priority":

            # UCS ordena los nodos usando node.g,
            # es decir, el costo acumulado del camino.
            heapq.heappush(
                self.data,
                (node.g, next(self.counter), node)
            )

        else:
            # BFS y DFS simplemente agregan al final.
            self.data.append(node)

    def pop(self):
        """
        Retorna y elimina el siguiente nodo que debe expandirse.
        """

        if self.kind == "priority":

            # UCS saca el nodo con menor costo g.
            return heapq.heappop(self.data)[2]

        if self.kind == "fifo":

            # BFS utiliza FIFO:
            # First In, First Out.
            # Sale el nodo que entró primero.
            return self.data.popleft()

        # DFS utiliza LIFO:
        # Last In, First Out.
        # Sale el nodo agregado más recientemente.
        return self.data.pop()

    def __len__(self):
        # Permite usar:
        # while frontier:
        #
        # Retorna cuántos nodos hay actualmente en la frontera.
        return len(self.data)


# ============================================================
# BÚSQUEDA GENÉRICA
# ============================================================

def search(problem, frontier_kind):
    """
    Búsqueda genérica sobre un grafo.

    frontier_kind determina qué algoritmo utilizamos:

    "fifo"     -> BFS
    "lifo"     -> DFS
    "priority" -> UCS

    Retorna:
        (goal_node, expansions)

    goal_node:
        Nodo objetivo encontrado.

    expansions:
        Número de nodos expandidos durante la búsqueda.
    """

    # Creamos el nodo inicial usando el estado inicial del problema.
    start = Node(problem.initial)

    # Si el estado inicial ya es el objetivo,
    # no necesitamos expandir ningún nodo.
    if problem.is_goal(start.state):
        return start, 0

    # Creamos la frontera correspondiente al algoritmo elegido.
    frontier = Frontier(frontier_kind)

    # Insertamos el nodo inicial.
    frontier.push(start)

    # explored contiene los estados que ya fueron expandidos.
    explored = set()

    # Contador de nodos expandidos.
    # Sirve para comparar la eficiencia de los algoritmos.
    expansions = 0

    # Mientras existan nodos pendientes en la frontera...
    while frontier:

        # Sacamos el siguiente nodo según la disciplina
        # FIFO, LIFO o prioridad.
        node = frontier.pop()

        # IMPORTANTE:
        # La prueba de objetivo se realiza cuando el nodo se EXPANDE,
        # no cuando se genera.
        #
        # Esto es especialmente importante para UCS,
        # porque probar el objetivo al generar puede devolver
        # una solución que no tenga el costo mínimo.
        if problem.is_goal(node.state):
            return node, expansions

        # Si este estado ya fue explorado,
        # no lo procesamos nuevamente.
        if node.state in explored:
            continue

        # Marcamos el estado como explorado.
        explored.add(node.state)

        # Contamos una nueva expansión.
        expansions += 1

        # Recorremos todas las acciones posibles
        # desde el estado actual.
        for action in problem.actions(node.state):

            # Calculamos el estado que resulta
            # de aplicar esa acción.
            child_state = problem.result(node.state, action)

            # Si todavía no hemos explorado ese estado...
            if child_state not in explored:

                # Calculamos el costo de realizar la acción.
                cost = problem.step_cost(node.state, action)

                # Creamos el nodo hijo.
                #
                # node.g + cost representa el costo acumulado
                # desde el estado inicial hasta el nuevo nodo.
                child = Node(
                    child_state,
                    node,
                    action,
                    node.g + cost
                )

                # Agregamos el nodo hijo a la frontera.
                frontier.push(child)

    # Si la frontera queda vacía y nunca encontramos
    # el objetivo, retornamos None.
    return None, expansions


# ============================================================
# TINYGRAPH
# ============================================================

class TinyGraph(Problem):
    """
    Grafo pequeño utilizado para demostrar por qué BFS y UCS
    pueden encontrar soluciones diferentes cuando los costos
    de las acciones no son iguales.

    Caminos posibles hacia A:

        start -> A
        costo = 10

        start -> B -> A
        costo = 1 + 1 = 2

    BFS busca el camino con menor cantidad de pasos.
    UCS busca el camino con menor costo.
    """

    # Diccionario que representa las conexiones del grafo.
    #
    # Cada elemento tiene:
    # destino, costo
    EDGES = {
        "start": [("A", 10), ("B", 1)],
        "B": [("A", 1)],
        "A": []
    }

    def actions(self, state):
        # Retorna los estados a los que podemos movernos
        # desde el estado actual.
        return [dst for dst, _ in self.EDGES[state]]

    def result(self, state, action):
        # En este problema, la acción ya representa
        # directamente el siguiente estado.
        return action

    def step_cost(self, state, action):
        # Retorna el costo de viajar desde state
        # hacia el destino indicado por action.
        return dict(self.EDGES[state])[action]


# ============================================================
# ESTADO OBJETIVO DEL 8-PUZZLE
# ============================================================

# 0 representa el espacio vacío.
GOAL = (
    1, 2, 3,
    4, 5, 6,
    7, 8, 0
)


# ============================================================
# CLASE EIGHTPUZZLE
# ============================================================

class EightPuzzle(Problem):
    """
    Representa el problema del 8-puzzle.

    El estado utiliza una tupla de 9 posiciones.

    Ejemplo:

        1 2 3
        4 5 6
        7 8 _

    internamente se representa como:

        (1, 2, 3, 4, 5, 6, 7, 8, 0)

    Se utiliza una tupla porque puede ser usada dentro de sets
    y compararse fácilmente.
    """

    # MOVES indica con qué posiciones puede intercambiarse
    # el espacio vacío dependiendo de dónde se encuentre.
    #
    # Ejemplo:
    #
    # posición 0 puede intercambiarse con:
    # posición 1 o posición 3.
    MOVES = {
        0: (1, 3),
        1: (0, 2, 4),
        2: (1, 5),
        3: (0, 4, 6),
        4: (1, 3, 5, 7),
        5: (2, 4, 8),
        6: (3, 7),
        7: (4, 6, 8),
        8: (5, 7)
    }

    def __init__(self, initial, goal=GOAL):

        # Llamamos al constructor de la clase padre Problem.
        #
        # Esto es HERENCIA en POO.
        super().__init__(initial, goal)

    def actions(self, state):

        # Buscamos la posición donde se encuentra el 0.
        blank_position = state.index(0)

        # Retornamos las posiciones con las que
        # puede intercambiarse el espacio vacío.
        return self.MOVES[blank_position]

    def result(self, state, action):

        # Convertimos temporalmente la tupla en lista,
        # porque las tuplas no pueden modificarse.
        s = list(state)

        # Encontramos la posición del espacio vacío.
        b = state.index(0)

        # Intercambiamos el espacio vacío
        # con la posición indicada por action.
        s[b], s[action] = s[action], s[b]

        # Convertimos nuevamente el resultado a tupla.
        return tuple(s)


# ============================================================
# FUNCIÓN PARA MOSTRAR EL TABLERO
# ============================================================

def show(state):
    """
    Imprime un estado del 8-puzzle como una matriz 3x3.
    """

    # Recorremos las posiciones:
    # 0, 3 y 6.
    for r in range(0, 9, 3):

        # Imprimimos tres elementos por fila.
        #
        # El 0 se muestra como "_".
        print(
            " ".join(
                "_" if v == 0 else str(v)
                for v in state[r:r + 3]
            )
        )


# ============================================================
# INSTANCIAS CON PROFUNDIDAD CONOCIDA
# ============================================================

# Estas profundidades fueron verificadas mediante
# una BFS exhaustiva desde GOAL.
#
# La profundidad indica el número mínimo de movimientos
# necesarios para alcanzar GOAL.

D2 = (
    1, 2, 3,
    4, 5, 6,
    0, 7, 8
)  # profundidad óptima = 2

D8 = (
    0, 4, 2,
    5, 1, 3,
    7, 8, 6
)  # profundidad óptima = 8

D12 = (
    5, 4, 2,
    7, 0, 3,
    8, 1, 6
)  # profundidad óptima = 12

D16 = (
    7, 5, 2,
    4, 0, 3,
    8, 1, 6
)  # profundidad óptima = 16


# ============================================================
# CARGAR INSTANCIAS
# ============================================================

def load_instances(path=None):
    """
    Carga las instancias del 8-puzzle desde instances.json.

    Retorna un diccionario de la forma:

        {
            4:  [estado1, estado2, ...],
            8:  [estado1, estado2, ...],
            12: [...],
            16: [...]
        }

    Cada estado se convierte nuevamente en una tupla.
    """

    # Si no proporcionamos una ruta,
    # busca instances.json en la misma carpeta que este archivo.
    path = Path(
        path or Path(__file__).with_name("instances.json")
    )

    # Lee el archivo JSON y lo transforma
    # en estructuras de Python.
    data = json.loads(path.read_text())

    # Las listas provenientes del JSON se convierten en tuplas.
    #
    # También convertimos las claves de profundidad
    # de string a int.
    return {
        int(k): [tuple(s) for s in v]
        for k, v in data["instances"].items()
    }