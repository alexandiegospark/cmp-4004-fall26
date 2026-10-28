"""Taller de la semana 4 — Plantilla de la tarea 1: heurísticas en una cuadrícula con costos.

Completa las cuatro heurísticas y ejecuta ``python3 test_heuristics.py``.
Todas las pruebas requeridas deben pasar, INCLUIDA la que exige que una
heurística no admisible rompa la optimalidad. Una garantía cuyo fallo no
puedes observar es una garantía que no has comprendido.
"""
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

    Aquí resulta admisible porque MIN_COST == 1. Pregúntate: si MIN_COST
    fuera 2, ¿seguiría siendo admisible? ¿La seguiría dominando
    ``h_manhattan_scaled``?
    """
    # Consulta problem.goal para obtener la tupla objetivo; state contiene la tupla actual.
    # TODO solo marca trabajo pendiente y no se ejecuta. La excepción siguiente sí detiene la llamada.
    # TODO: devuelve |dr| + |dc| entre state y problem.goal
    # Conserva el ejercicio pendiente: reemplaza esta instrucción al implementar la heurística.
    raise NotImplementedError


def h_manhattan_scaled(problem: GridProblem, state) -> int:
    """Distancia de Manhattan × MIN_COST: heurística admisible para una
    cuadrícula con costos por paso de al menos MIN_COST."""
    # TODO
    # Conserva el ejercicio pendiente: reemplaza esta instrucción al implementar la heurística.
    raise NotImplementedError


# -> float permite un resultado real: la distancia euclidiana no tiene por qué ser entera.
def h_euclidean_scaled(problem: GridProblem, state) -> float:
    """Distancia euclidiana × MIN_COST. En una cuadrícula de cuatro direcciones
    es admisible, pero menos informada que Manhattan escalada: euclidiana <= Manhattan."""
    # TODO
    # Conserva el ejercicio pendiente: reemplaza esta instrucción al implementar la heurística.
    raise NotImplementedError


def h_bad(problem: GridProblem, state) -> int:
    """NO ADMISIBLE: debe sobreestimar al menos en algún estado.

    Forma sugerida: MAX_COST * distancia de Manhattan. MAX_COST vale 8,
    pero el camino óptimo suele recorrer celdas baratas, de modo que sobreestima.
    """
    # TODO
    # Conserva el ejercicio pendiente: reemplaza esta instrucción al implementar la heurística.
    raise NotImplementedError


# ---- Esquema de la tarea 2: el duelo con el LLM ------------------------------
# Consulta README.md, sección «Tarea 2». Los prompts y la representación de instancias están en duel.py,
# que importa ``gridworld.render`` y obtiene las cuadrículas de ``instances.json``.
# NO necesitas escribir duel.py: ya se proporciona. Tú añades la llamada al modelo
# mediante aicourse.llm y registras los conteos de cada categoría de fallo.


# Esta demostración solo se ejecuta al lanzar el archivo, no al importarlo desde las pruebas.
if __name__ == "__main__":
    # Prueba básica: resuelve una instancia 5×5 con cada heurística que hayas completado.
    from gridworld import load_instances
    grid = load_instances()[5][0]
    print("\n".join(grid), "\n")
    # Instanciación: prob es un objeto con su propio inicio y objetivo; no es una clase nueva.
    prob = GridProblem(grid)
    for name, h in [("zero", h_zero), ("manhattan", h_manhattan),
                    ("manhattan_scaled", h_manhattan_scaled),
                    ("euclidean_scaled", h_euclidean_scaled),
                    ("bad", h_bad)]:
        try:
            node, exp = astar(prob, h)
        # Captura las heurísticas todavía pendientes para continuar con las demás.
        except NotImplementedError:
            print(f"  {name:<20} not implemented yet")
            continue
        # node es el objeto objetivo devuelto por A*; .g es su costo acumulado, no su longitud.
        cost = node.g if node else None
        print(f"  {name:<20} cost={cost}  expansions={exp}")
