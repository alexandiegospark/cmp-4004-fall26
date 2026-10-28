"""Taller de la semana 4 — SOLUCIÓN DE REFERENCIA (solo para el docente).

Versión completada de ``starter.py``: conserva nombres y firmas para que las
pruebas de ``test_heuristics.py`` pasen si se importa como ``starter``.
El material describe ``studios/_verify_solutions.py`` como verificador que
registra esta solución con ese nombre y ejecuta las pruebas sin cambios.

NO distribuir a estudiantes: se excluye mediante ``studios/.gitignore``.
La explicación didáctica está en ``solution.ipynb``, que importa este archivo
sin copiarlo para mantener ambas versiones sincronizadas.
"""
from math import hypot

# GridProblem es la clase del dominio y astar es una función del motor compartido.
# Las heurísticas son funciones independientes: reciben un objeto problema y un estado.
from gridworld import GridProblem, astar, MIN_COST, MAX_COST


# ---- Tarea 1: implementa cuatro heurísticas ---------------------------------

# Las anotaciones de tipo indican que problem debe ofrecer la interfaz de GridProblem.
# -> int describe el resultado esperado; Python no valida automáticamente esos tipos al llamar.
def h_zero(problem: GridProblem, state) -> int:
    """Admisible, pero no informa: A* se convierte en búsqueda de costo uniforme."""
    return 0


def h_manhattan(problem: GridProblem, state) -> int:
    """Distancia de Manhattan sin escalar hasta el objetivo.

    Aquí es admisible porque ``MIN_COST == 1``: cada paso cuesta al menos 1,
    así que |dr|+|dc| no supera el costo restante real. Si ``MIN_COST`` fuera 2,
    seguiría subestimando y sería admisible, pero la versión escalada de abajo
    la dominaría: proporcionaría una cota inferior más ajustada.
    """
    # Acceso a un atributo del objeto problema; desempaqueta la fila y columna del objetivo.
    gr, gc = problem.goal
    # state es una tupla de coordenadas del nodo evaluado, distinta de la instancia problem.
    r, c = state
    # abs es una función incorporada: suma distancias por fila y columna, sin diagonales.
    return abs(r - gr) + abs(c - gc)


def h_manhattan_scaled(problem: GridProblem, state) -> int:
    """Distancia de Manhattan × MIN_COST: heurística admisible para una
    cuadrícula con costos por paso de al menos MIN_COST."""
    # Acceso a un atributo del objeto problema; desempaqueta la fila y columna del objetivo.
    gr, gc = problem.goal
    # state es una tupla de coordenadas del nodo evaluado, distinta de la instancia problem.
    r, c = state
    # Multiplica el mínimo de pasos por el menor costo posible de cada paso.
    return (abs(r - gr) + abs(c - gc)) * MIN_COST


def h_euclidean_scaled(problem: GridProblem, state) -> float:
    """Distancia euclidiana × MIN_COST. En una cuadrícula de cuatro direcciones
    es admisible, pero menos informada que Manhattan escalada: euclidiana <= Manhattan."""
    # Acceso a un atributo del objeto problema; desempaqueta la fila y columna del objetivo.
    gr, gc = problem.goal
    # state es una tupla de coordenadas del nodo evaluado, distinta de la instancia problem.
    r, c = state
    # hypot calcula la distancia en línea recta: sqrt(dr**2 + dc**2).
    return hypot(r - gr, c - gc) * MIN_COST


def h_bad(problem: GridProblem, state) -> int:
    """NO ADMISIBLE: puede sobreestimar cuando el camino óptimo pasa por
    celdas baratas. Usa ``MAX_COST × Manhattan``: MAX_COST vale 8, pero
    un buen camino suele pasar por '.' de costo 1. Supone el terreno más caro
    en cada paso y puede superar el costo restante real. Con esta heurística,
    A* puede devolver, y aquí devuelve, un camino subóptimo."""
    # Acceso a un atributo del objeto problema; desempaqueta la fila y columna del objetivo.
    gr, gc = problem.goal
    # state es una tupla de coordenadas del nodo evaluado, distinta de la instancia problem.
    r, c = state
    # Es un fallo deliberado del ejercicio: mayor estimación puede reducir trabajo y perder optimalidad.
    return (abs(r - gr) + abs(c - gc)) * MAX_COST


# ---- Esquema de la tarea 2: el duelo con el LLM ------------------------------
# Consulta README.md, sección «Tarea 2». Los prompts y la representación de instancias están en duel.py,
# que importa ``gridworld.render`` y obtiene las cuadrículas de ``instances.json``.
# NO necesitas escribir duel.py: ya se proporciona. Tú añades la llamada al modelo
# mediante aicourse.llm y registras los conteos de cada categoría de fallo.


# Esta demostración solo se ejecuta al lanzar el archivo, no al importarlo desde las pruebas.
if __name__ == "__main__":
    from gridworld import load_instances
    grid = load_instances()[5][0]
    print("\n".join(grid), "\n")
    # Instanciación: prob es un objeto con su propio inicio y objetivo; no es una clase nueva.
    prob = GridProblem(grid)
    for name, h in [("zero", h_zero), ("manhattan", h_manhattan),
                    ("manhattan_scaled", h_manhattan_scaled),
                    ("euclidean_scaled", h_euclidean_scaled),
                    ("bad", h_bad)]:
        # h guarda un objeto función; A* lo invocará durante la búsqueda con (prob, estado).
        node, exp = astar(prob, h)
        # node es el objeto objetivo devuelto por A*; .g es su costo acumulado, no su longitud.
        cost = node.g if node else None
        print(f"  {name:<20} cost={cost}  expansions={exp}")
