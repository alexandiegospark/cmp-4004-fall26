"""Taller de la semana 3 — SOLUCIÓN DE REFERENCIA (solo para el docente).

Versión completada de ``starter.py``: conserva los nombres y firmas para que
``test_search.py`` pase al importar este módulo como ``starter``. El material
describe ``studios/_verify_solutions.py`` como verificador que registra esta
solución con el nombre ``starter`` y ejecuta las pruebas sin modificarlas.

NO distribuir a estudiantes: se excluye mediante ``studios/.gitignore``.
La explicación didáctica está en ``solution.ipynb``, que importa este archivo
en lugar de copiarlo, para mantener ambas versiones sincronizadas.
"""
from search import Problem, Node, search


# ---- Tarea 1: formula misioneros y caníbales --------------------------------
# Estado: (m_left, c_left, boat_side); boat_side es 0=izquierda o 1=derecha, y
# m_left/c_left cuentan personas en la orilla IZQUIERDA. Inicial: (3, 3, 0); objetivo:
# (0, 0, 1). Decisión de diseño que debes defender en la demostración: imponemos
# la restricción de seguridad en ambas orillas dentro de
# ``actions()``: solo son alcanzables los estados legales, y ``result()``
# conserva una transición pura; la búsqueda no alcanza estados con misioneros devorados.

# El bote lleva 1 o 2 personas; nunca cruza vacío.
_BOAT_LOADS = [(1, 0), (2, 0), (0, 1), (0, 2), (1, 1)]


# Herencia: esta subclase conserva step_cost de Problem y redefine la formulación concreta.
# Sus métodos reciben self, la instancia, y state, una tupla que describe un estado del problema.
class MissionariesAndCannibals(Problem):
    def __init__(self):
        # Inicializa initial y goal del padre en ESTE objeto; no crea otro objeto Problem.
        super().__init__((3, 3, 0), (0, 0, 1))

    # El prefijo _ señala un método auxiliar interno por convención, no una prohibición de acceso.
    def _legal(self, state):
        """Ninguna orilla puede tener más caníbales que misioneros si hay al menos
        un misionero presente. También exige poblaciones entre 0 y 3."""
        m_left, c_left, _ = state
        if not (0 <= m_left <= 3 and 0 <= c_left <= 3):
            return False
        # La población total es fija; basta guardar la orilla izquierda y deducir la derecha.
        m_right, c_right = 3 - m_left, 3 - c_left
        if m_left > 0 and c_left > m_left:
            return False
        if m_right > 0 and c_right > m_right:
            return False
        return True

    def actions(self, state):
        m_left, c_left, boat = state
        legal = []
        # Prueba las cinco cargas posibles; primero comprueba que las personas estén en la orilla del bote.
        for dm, dc in _BOAT_LOADS:
            if boat == 0:                      # bote a la izquierda: transporta personas a la derecha
                if dm <= m_left and dc <= c_left:
                    nxt = (m_left - dm, c_left - dc, 1)
                    # Invoca otro método de esta misma instancia para comprobar AMBAS orillas tras el cruce.
                    if self._legal(nxt):
                        legal.append((dm, dc))
            else:                              # bote a la derecha: transporta personas a la izquierda
                m_right, c_right = 3 - m_left, 3 - c_left
                if dm <= m_right and dc <= c_right:
                    nxt = (m_left + dm, c_left + dc, 0)
                    # Invoca otro método de esta misma instancia para comprobar AMBAS orillas tras el cruce.
                    if self._legal(nxt):
                        legal.append((dm, dc))
        return legal

    def result(self, state, action):
        m_left, c_left, boat = state
        # La acción es una tupla de cantidades. La transición cambia los conteos y alterna el bote.
        # La legalidad ya se filtró en actions; result no repite esa validación.
        dm, dc = action
        if boat == 0:
            return (m_left - dm, c_left - dc, 1)
        return (m_left + dm, c_left + dc, 0)

    def is_goal(self, state):
        return state == self.goal


# ---- Tarea 2: cuatro algoritmos; un motor y distintas fronteras --------------

def bfs(problem):
    """Búsqueda en anchura: completa; óptima solo cuando los costos por paso son uniformes."""
    # FIFO retira primero el nodo más antiguo: explora por niveles, no por costo acumulado.
    return search(problem, "fifo")


def dfs(problem):
    """Búsqueda en profundidad sobre un grafo. El conjunto de explorados de
    ``search()`` evita ciclos indefinidos. No garantiza optimalidad."""
    # LIFO retira el último nodo insertado y profundiza en esa rama.
    return search(problem, "lifo")


def ucs(problem):
    """Búsqueda de costo uniforme: óptima con costos no negativos por paso."""
    # La cola de prioridad de Frontier usa node.g: retira primero el camino de menor costo.
    return search(problem, "priority")


def depth_limited(problem, limit):
    """Búsqueda recursiva en árbol hasta una profundidad fija.

    Devuelve ``(node, expansions, hit_limit)``: ``node`` es el Node objetivo
    o None; ``expansions`` cuenta nodos expandidos; ``hit_limit`` es True
    si se cortó por el límite de profundidad y no por agotar el subárbol.
    Esa bandera permite que ``ids`` sepa si aumentar el límite puede ayudar.

    Omite el estado del padre inmediato para evitar ciclos triviales de dos
    pasos sin guardar un conjunto de explorados. Es búsqueda en árbol:
    el límite de profundidad garantiza que cada búsqueda limitada termine.
    """
    expansions = 0

    # Clausura recursiva: conserva acceso a problem y al contador de la llamada depth_limited.
    # Cada llamada recursiva tiene sus propias variables node, limit y parent_state.
    def recur(node, limit, parent_state):
        # nonlocal permite modificar el contador de la función exterior, en lugar de crear uno local.
        nonlocal expansions
        # Comprueba el objetivo ANTES del límite: un objetivo situado exactamente en ese nivel es válido.
        if problem.is_goal(node.state):
            return node, False             # objetivo encontrado: esta rama no se cortó
        if limit == 0:
            return None, True              # corte por el límite de profundidad
        expansions += 1
        cutoff = False
        for action in problem.actions(node.state):
            child_state = problem.result(node.state, action)
            if child_state == parent_state:
                continue                   # evita regresar inmediatamente al padre
            # Composición de objetos: child guarda node como padre para reconstruir el plan con path().
            child = Node(child_state, node, action,
                         node.g + problem.step_cost(node.state, action))
            # Un paso consume una unidad del límite. Al retornar, continúa con otra rama si no encontró objetivo.
            found, was_cut = recur(child, limit - 1, node.state)
            if found is not None:
                return found, was_cut
            if was_cut:
                cutoff = True
        return None, cutoff

    # Instancia raíz sin padre, acción ni costo previo; la búsqueda empieza en el estado inicial.
    root = Node(problem.initial)
    node, hit_limit = recur(root, limit, None)
    return node, expansions, hit_limit


def ids(problem, max_depth=40):
    """Profundización iterativa: llama a ``depth_limited`` con límites 0, 1, 2, etc.
    hasta encontrar el objetivo. Devuelve ``(node, total_expansions)``. Si no
    encontró nada y NO cortó por el límite, se agotó el espacio explorado y
    devuelve ``(None, total)``.
    """
    total = 0
    for limit in range(max_depth + 1):
        node, expansions, hit_limit = depth_limited(problem, limit)
        # Acumula también el trabajo repetido de las búsquedas anteriores: no cuenta solo la última.
        total += expansions
        if node is not None:
            return node, total
        if not hit_limit:                  # sin ramas pendientes bajo el límite: agotado
            return None, total
    # También devuelve None si llegó a max_depth sin solución, aunque pueda existir una más profunda.
    return None, total


# ---- Tarea 3: medición, después de superar la tarea 2 ------------------------
def measure(bank=None):
    """Ejecuta los cuatro algoritmos sobre el banco de instancias y devuelve filas
    (depth, algorithm, expansions, solution_length). Después representa
    expansiones frente a profundidad con eje y LOGARÍTMICO: esa gráfica es el entregable."""
    from search import load_instances, EightPuzzle
    bank = bank or load_instances()
    rows = []
    for depth in sorted(bank):
        for state in bank[depth]:
            # Crea un objeto problema por instancia; los algoritmos reutilizan su interfaz polimórfica.
            p = EightPuzzle(state)
            for name, algo in [("BFS", bfs), ("DFS", dfs),
                               ("UCS", ucs), ("IDS", ids)]:
                node, exp = algo(p)
                # node es el objeto objetivo; path() reconstruye las acciones y len mide su longitud.
                rows.append((depth, name, exp, len(node.path())))
    return rows


# Esta demostración se ejecuta al lanzar el archivo; importarlo solo define clases y funciones.
if __name__ == "__main__":
    from search import EightPuzzle, D8
    p = EightPuzzle(D8)
    for name, algo in [("bfs", bfs), ("dfs", dfs), ("ucs", ucs), ("ids", ids)]:
        node, exp = algo(p)
        print(f"  {name:<5} len={len(node.path()):>4}  expansions={exp:,}")
