"""Pruebas proporcionadas para el taller de la semana 3.

Ejecuta ``python3 test_search.py``. Se muestra una línea por prueba. Superarlas
significa que los cuatro algoritmos se comportan según la teoría, INCLUIDO
el caso que debe comportarse mal:

``test_bfs_suboptimal_nonuniform_cost`` exige que BFS devuelva un camino NO
óptimo. No es un error: BFS solo es óptima con costos uniformes por paso.
``TinyGraph`` incumple esa condición deliberadamente. Observar el fallo de
una garantía permite comprender cuándo se aplica.
"""
import sys

from search import EightPuzzle, TinyGraph, Problem, D8
import starter as s


# Instancia de profundidad 8: la longitud óptima es 8, verificada mediante BFS exhaustiva
# desde el objetivo (véase _generate_instances.py). BFS, UCS e IDS deben devolver 8.
D8_OPTIMAL_LEN = 8


# POO: subclase de Problem que redefine acciones y transición; hereda __init__, is_goal y costo 1.
# EDGES es un atributo de clase compartido. Cada instancia conserva su propio initial y goal.
class CyclicGraph(Problem):
    """Grafo con un ciclo A->B->C->A y una salida C->G. El conjunto de
    explorados del motor evita recorrer indefinidamente estados repetidos;
    DFS debe terminar y alcanzar G."""
    EDGES = {"A": ["B"], "B": ["C"], "C": ["A", "G"], "G": []}

    def actions(self, state):
        # Busca la lista de vecinos en la tabla de clase mediante esta instancia.
        return self.EDGES[state]

    def result(self, state, action):
        # En este dominio, la acción es el nombre del destino y también el nuevo estado.
        return action


def test_bfs_optimal_uniform_cost():
    # Rompecabezas de 8 fichas: cada movimiento cuesta 1, así que BFS SÍ es óptima aquí.
    # EightPuzzle(D8) crea un objeto problema; s es el alias del módulo starter.
    # bfs devuelve un Node objetivo y un contador; _ descarta el contador en esta prueba.
    node, _ = s.bfs(EightPuzzle(D8))
    assert node is not None, "bfs found no solution"
    # path() es un método de Node: reconstruye la lista de acciones mediante sus padres.
    # assert lanza AssertionError si la longitud no coincide con el óptimo conocido.
    assert len(node.path()) == D8_OPTIMAL_LEN, (
        f"bfs length {len(node.path())} != optimal {D8_OPTIMAL_LEN}"
    )
    print(f"  ok  bfs optimal on uniform costs (len={D8_OPTIMAL_LEN})")


def test_bfs_suboptimal_nonuniform_cost():
    """Idea central del ejercicio: BFS cuenta aristas, no costo. En TinyGraph,
    el camino al objetivo con menos aristas cuesta 10; el óptimo cuesta 2.
    BFS debe devolver la respuesta INCORRECTA de costo 10: su garantía de
    optimalidad no se aplica cuando los costos por paso son diferentes."""
    # TinyGraph hereda el inicializador: start es el inicio y A el objetivo.
    # FIFO encuentra la arista directa antes que el camino de dos pasos, aunque sea más cara.
    node, _ = s.bfs(TinyGraph("start", "A"))
    assert node is not None
    # g es el costo acumulado del objeto Node, no la cantidad de movimientos de su path().
    # Esta prueba PASA cuando se observa la limitación esperada de BFS.
    assert node.g == 10, (
        f"expected BFS to return the suboptimal cost-10 path, got g={node.g}. "
        "If you got 2, check that bfs really uses a FIFO frontier (not priority)."
    )
    print("  ok  bfs suboptimal on non-uniform costs (g=10 > optimum 2 -- the lesson)")


def test_dfs_terminates_on_cyclic_graph():
    node, _ = s.dfs(CyclicGraph("A", "G"))   # si no termina, revisa el conjunto de explorados de DFS
    assert node is not None and node.state == "G", "dfs did not reach the goal"
    print("  ok  dfs terminates on a cyclic graph (explored set does its job)")


def test_ucs_optimal_nonuniform_cost():
    # La misma interfaz polimórfica del problema, pero prioridad por costo en lugar de orden de llegada.
    node, _ = s.ucs(TinyGraph("start", "A"))
    assert node is not None
    assert node.g == 2, f"ucs not optimal on non-uniform costs: g={node.g} != 2"
    print("  ok  ucs optimal on non-uniform costs (g=2)")


def test_ids_matches_bfs_solution_length():
    # Crea problemas equivalentes para comparar longitud óptima, no el número de expansiones.
    ids_node, _ = s.ids(EightPuzzle(D8))
    bfs_node, _ = s.bfs(EightPuzzle(D8))
    assert ids_node is not None, "ids found no solution"
    assert len(ids_node.path()) == len(bfs_node.path()) == D8_OPTIMAL_LEN, (
        f"ids len {len(ids_node.path())} != bfs len {len(bfs_node.path())} "
        f"(both should be {D8_OPTIMAL_LEN})"
    )
    print(f"  ok  ids matches bfs solution length ({D8_OPTIMAL_LEN}) at O(bd) memory")


# Las funciones son objetos: la lista guarda referencias que main llamará después.
TESTS = [
    test_bfs_optimal_uniform_cost,
    test_bfs_suboptimal_nonuniform_cost,
    test_dfs_terminates_on_cyclic_graph,
    test_ucs_optimal_nonuniform_cost,
    test_ids_matches_bfs_solution_length,
]


def main():
    # Ejecuta las cinco funciones de prueba y cuenta tareas pendientes o aserciones fallidas.
    failed = 0
    for t in TESTS:
        try:
            t()
        # Se espera mientras los TODO de starter sigan sin implementarse; no modifica esos TODO.
        except NotImplementedError:
            print(f"  --  {t.__name__}: algorithm not implemented yet")
            failed += 1
        # e es el objeto excepción y contiene el mensaje de la comprobación fallida.
        except AssertionError as e:
            print(f"  FAIL {t.__name__}: {e}")
            failed += 1
    if failed:
        print(f"\n{failed}/{len(TESTS)} failed")
        # Código de salida 1 para fallos; si todo pasa, main termina normalmente con código 0.
        sys.exit(1)
    print(f"\nall {len(TESTS)} tests pass")


# Ejecuta las pruebas solo al lanzar el archivo directamente, no al importarlo.
if __name__ == "__main__":
    main()
