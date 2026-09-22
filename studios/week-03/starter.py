"""
Studio de la Semana 3 — archivo starter.

Aquí debes completar tres tareas principales:

Task 1:
    Formular el problema de Misioneros y Caníbales.

Task 2:
    Implementar BFS, DFS, UCS e IDS.

Task 3:
    Medir el comportamiento de los cuatro algoritmos
    utilizando varias instancias del 8-puzzle.

Mientras trabajas puedes ejecutar:

    python3 test_search.py

para comprobar si tus implementaciones pasan las pruebas.

IMPORTANTE:
Una de las pruebas demuestra intencionalmente que BFS puede devolver
una solución NO óptima cuando los costos de las acciones no son iguales.

Eso no significa que BFS esté mal implementado.
BFS solamente garantiza optimalidad cuando todos los pasos tienen
el mismo costo.
"""

# Importamos desde search.py:
#
# Problem:
#   clase base para representar problemas de búsqueda.
#
# Node:
#   representa un nodo dentro del árbol/grafo de búsqueda.
#
# search:
#   motor de búsqueda genérico que ya implementa BFS, DFS y UCS
#   dependiendo del tipo de frontera que le indiquemos.
from search import Problem, Node, search


# ============================================================
# TASK 1: MISIONEROS Y CANÍBALES
# ============================================================

# El problema tiene:
#
# - 3 misioneros
# - 3 caníbales
# - 1 bote
#
# El bote puede transportar 1 o 2 personas.
# Nunca puede cruzar vacío.
#
# Regla de seguridad:
#
# Si en cualquiera de las dos orillas hay al menos un misionero
# y los caníbales son más numerosos que los misioneros,
# ese estado es inválido.
#
# Ejemplo inválido:
#
# 1 misionero
# 2 caníbales
#
# porque:
#
# 2 > 1
#
# Estado sugerido:
#
# (m_left, c_left, boat_side)
#
# donde:
#
# m_left     = número de misioneros en la orilla izquierda.
# c_left     = número de caníbales en la orilla izquierda.
# boat_side  = posición del bote.
#
# boat_side = 0 → izquierda
# boat_side = 1 → derecha
#
# Estado inicial:
#
# (3, 3, 0)
#
# Estado objetivo:
#
# (0, 0, 1)


class MissionariesAndCannibals(Problem):
    """
    Clase que representará el problema de Misioneros y Caníbales.

    Esta clase HEREDA de Problem.

    En POO esto significa que MissionariesAndCannibals puede reutilizar
    atributos y comportamientos definidos en la clase Problem.

    Debemos definir los componentes específicos de este problema:
    - estado inicial
    - objetivo
    - acciones
    - transición
    - prueba de objetivo
    """

    def __init__(self):

        # Aquí debemos definir:
        #
        # self.initial
        # self.goal
        #
        # Lo recomendado es llamar al constructor de Problem usando:
        #
        # super().__init__(...)
        #
        # super() permite utilizar el constructor de la clase padre.
        #
        # TODO: establecer estado inicial y objetivo.
        raise NotImplementedError

    def actions(self, state):
        """
        Debe retornar todas las acciones LEGALES
        que pueden realizarse desde el estado actual.

        Por ejemplo, una acción podría representar:

            (1, 0)

        es decir:
        transportar 1 misionero y 0 caníbales.

        O:

            (1, 1)

        transportar 1 misionero y 1 caníbal.

        Debes decidir dónde comprobarás la regla:

            caníbales <= misioneros

        cuando haya misioneros presentes.

        Podrías hacerlo aquí en actions(),
        o después mediante result()/is_valid().

        Esa decisión forma parte de la FORMULACIÓN del problema.
        """

        # TODO: retornar las cargas legales del bote.
        raise NotImplementedError

    def result(self, state, action):
        """
        Aplica una acción a un estado.

        Debe calcular:
        - cuántos misioneros quedan a cada lado,
        - cuántos caníbales quedan,
        - y cambiar el lado del bote.

        Retorna:
            el nuevo estado producido por la acción.
        """

        # TODO: aplicar la acción y cambiar el lado del bote.
        raise NotImplementedError

    def is_goal(self, state):
        """
        Comprueba si hemos alcanzado el estado objetivo.

        Debe retornar:
            True  → si el problema está resuelto.
            False → si todavía no está resuelto.
        """

        # TODO
        raise NotImplementedError


# ============================================================
# TASK 2: LOS CUATRO ALGORITMOS
# ============================================================

# search(problem, frontier_kind) YA EXISTE en search.py.
#
# Por eso BFS, DFS y UCS son muy sencillos.
#
# Los tres utilizan exactamente el mismo motor search().
#
# Lo único que cambia es la frontera:
#
# BFS → FIFO
# DFS → LIFO
# UCS → PRIORITY
#
# IDS es diferente porque utiliza varias búsquedas DFS
# con límites de profundidad crecientes.


def bfs(problem):
    """
    Breadth-First Search — búsqueda en anchura.

    Propiedades:

    - Es completa.
    - Encuentra la solución con menor número de pasos.
    - Solo es óptima en costo cuando todos los pasos
      tienen el mismo costo.

    Debe utilizar search() con una frontera FIFO.
    """

    # TODO:
    # retornar search(problem, ...)
    raise NotImplementedError


def dfs(problem):
    """
    Depth-First Search — búsqueda en profundidad.

    Explora primero una rama tan profundamente como sea posible.

    Utiliza una frontera LIFO.

    El conjunto explored de search.py evita que DFS quede atrapado
    indefinidamente en ciclos.

    DFS NO garantiza encontrar la solución óptima.
    """

    # TODO
    raise NotImplementedError


def ucs(problem):
    """
    Uniform-Cost Search — búsqueda de costo uniforme.

    UCS selecciona siempre el nodo cuyo costo acumulado g
    sea el menor.

    Utiliza una cola de prioridad.

    Propiedad importante:

    UCS es óptimo cuando los costos de los pasos son
    no negativos.
    """

    # TODO
    raise NotImplementedError


# ============================================================
# DEPTH-LIMITED SEARCH
# ============================================================

def depth_limited(problem, limit):
    """
    Realiza una búsqueda DFS con un límite máximo de profundidad.

    Este algoritmo será utilizado posteriormente por IDS.

    Parámetros:

    problem:
        problema que queremos resolver.

    limit:
        máxima profundidad que podemos explorar.

    Debe retornar:

        (node, expansions, hit_limit)

    donde:

    node:
        nodo objetivo si se encontró una solución.
        None si no se encontró.

    expansions:
        cantidad de nodos que fueron expandidos.

    hit_limit:
        True si la búsqueda tuvo que detenerse porque
        alcanzó el límite de profundidad.

        False si exploró todo lo posible sin necesidad
        de cortar por el límite.
    """

    # IDS utiliza TREE SEARCH en esta parte.
    #
    # No guarda todos los estados explorados globalmente,
    # porque eso aumentaría el uso de memoria.
    #
    # Sin embargo, conviene evitar ciclos triviales:
    #
    # A → B → A → B → A...
    #
    # Para ello se puede comprobar que el hijo no sea
    # inmediatamente igual al estado del padre.

    # TODO
    raise NotImplementedError


# ============================================================
# ITERATIVE DEEPENING SEARCH
# ============================================================

def ids(problem, max_depth=40):
    """
    Iterative Deepening Search — profundización iterativa.

    IDS ejecuta repetidamente una búsqueda DFS limitada.

    Primero:

        límite = 0

    luego:

        límite = 1

    después:

        límite = 2

    etc.

    hasta encontrar el objetivo.

    De esta manera combina:

    - la baja memoria de DFS
    - la completitud de BFS

    Retorna:

        (node, total_expansions)

    donde total_expansions suma las expansiones realizadas
    en TODAS las iteraciones.
    """

    # Ejemplo conceptual:
    #
    # depth_limited(problem, 0)
    # depth_limited(problem, 1)
    # depth_limited(problem, 2)
    # depth_limited(problem, 3)
    # ...
    #
    # hasta encontrar la solución.

    # Si depth_limited indica:
    #
    # hit_limit = False
    #
    # y además no encontró solución,
    # significa que ya no existen niveles más profundos
    # que valga la pena explorar.

    # TODO
    raise NotImplementedError


# ============================================================
# TASK 3: MEDICIÓN DE LOS ALGORITMOS
# ============================================================

def measure(bank=None):
    """
    Ejecuta los cuatro algoritmos sobre un banco
    de instancias del 8-puzzle.

    Los algoritmos son:

    BFS
    DFS
    UCS
    IDS

    Retorna filas con:

        (
            profundidad,
            algoritmo,
            expansiones,
            longitud_solución
        )

    Estos datos permiten comparar el comportamiento
    de los algoritmos.
    """

    # Importamos las herramientas necesarias para el 8-puzzle.
    from search import load_instances, EightPuzzle

    # Si no se proporciona un banco manualmente,
    # cargamos instances.json.
    bank = bank or load_instances()

    # Aquí almacenaremos los resultados.
    rows = []

    # Recorremos las profundidades disponibles.
    #
    # Por ejemplo:
    #
    # 4, 8, 12, 16
    for depth in sorted(bank):

        # Para cada profundidad existen varias instancias
        # diferentes del 8-puzzle.
        for state in bank[depth]:

            # Creamos el problema del 8-puzzle
            # utilizando este estado como estado inicial.
            p = EightPuzzle(state)

            # Ejecutamos los cuatro algoritmos
            # sobre EXACTAMENTE el mismo problema.
            for name, algo in [
                ("BFS", bfs),
                ("DFS", dfs),
                ("UCS", ucs),
                ("IDS", ids)
            ]:

                # Ejecutamos el algoritmo.
                #
                # node = solución encontrada.
                # exp  = número de expansiones.
                node, exp = algo(p)

                # node.path() retorna la lista de acciones
                # utilizadas para llegar al objetivo.
                #
                # len(node.path()) nos dice cuántos movimientos
                # tiene la solución encontrada.
                rows.append(
                    (
                        depth,
                        name,
                        exp,
                        len(node.path())
                    )
                )

    # Retornamos todos los resultados.
    return rows


# ============================================================
# PRUEBA RÁPIDA
# ============================================================

if __name__ == "__main__":

    # Este bloque solamente se ejecuta cuando starter.py
    # se ejecuta directamente.
    #
    # No se ejecuta automáticamente si starter.py
    # es importado desde otro archivo.

    # Importamos:
    #
    # EightPuzzle → clase del problema.
    # D8          → instancia cuya profundidad óptima es 8.
    from search import EightPuzzle, D8

    # Creamos un problema utilizando D8
    # como estado inicial.
    p = EightPuzzle(D8)

    # Probamos los cuatro algoritmos.
    for name, algo in [
        ("bfs", bfs),
        ("dfs", dfs),
        ("ucs", ucs),
        ("ids", ids)
    ]:

        try:

            # Ejecutamos el algoritmo.
            node, exp = algo(p)

        except NotImplementedError:

            # Mientras un algoritmo todavía tenga TODO,
            # aparecerá este mensaje en lugar de detener
            # todo el programa.
            print(f"  {name:<5} not implemented yet")

            continue

        # Si el algoritmo está implementado,
        # mostramos:
        #
        # len        → longitud de la solución.
        # expansions → cantidad de nodos expandidos.
        print(
            f"  {name:<5} "
            f"len={len(node.path()):>4}  "
            f"expansions={exp:,}"
        )