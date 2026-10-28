"""Pruebas proporcionadas para la tarea 1 de la semana 4.

Ejecuta ``python3 test_heuristics.py``. Si pasan, tu tarea 1 es defendible
y puedes comenzar la tarea 2. Se imprime una línea por prueba.

La prueba de fallo ``test_inadmissible_heuristic_returns_suboptimal_path``
exige que ``h_bad`` rompa la optimalidad al menos una vez en el banco.
Ese es el objetivo: observar el fallo de una garantía.
"""
import sys

# Las pruebas son funciones con aserciones; no utilizan clases propias de pruebas.
# GridProblem es la clase del dominio, astar es la función evaluada y s es el alias del módulo starter.
from gridworld import GridProblem, astar, load_instances
import starter as s


def _optimal_cost(grid):
    """Óptimo de referencia: UCS, o A* con h=0, es óptima porque todos los costos por paso son > 0."""
    # Instancia un objeto problema; sus atributos initial y goal describen los extremos de esta cuadrícula.
    prob = GridProblem(grid)
    # La lambda recibe el problema y el estado, pero siempre devuelve cero.
    # Así se obtiene una referencia independiente de las heurísticas que implementa el estudiante.
    node, _ = astar(prob, lambda p, st: 0)
    assert node is not None
    return node.g


# Carga las 40 instancias del JSON al importar el módulo, sin modificar ese archivo.
BANK = load_instances()


def test_h_zero_admissible_and_optimal():
    # h_zero es admisible por definición y A* debe devolver el óptimo real.
    for size in BANK:
        for grid in BANK[size]:
            prob = GridProblem(grid)
            node, _ = astar(prob, s.h_zero)
            # node.g es el atributo de costo acumulado del Node; no es la longitud de node.path().
            assert node.g == _optimal_cost(grid), f"h_zero not optimal on {size}x{size}"
    print("  ok  h_zero admissible ⇒ optimal on all 40 grids")


def test_manhattan_scaled_is_admissible():
    # Para ser admisible, h(state) no debe superar el costo restante real de ningún estado alcanzable.
    for size in BANK:
        for grid in BANK[size]:
            prob = GridProblem(grid)
            # El costo restante de un estado se calcula ejecutando A* desde él con h=0.
            # Muestra: comprueba inicio, objetivo y un punto interior.
            for state in [prob.initial, prob.goal, (prob.rows // 2, prob.cols // 2)]:
                # costo restante real desde `state` hasta el objetivo:
                sub = GridProblem(grid)
                # Cambia un atributo de la instancia sub para buscar desde el estado de muestra.
                # prob es OTRO objeto: su initial no cambia y sigue sirviendo para evaluar la heurística.
                sub.initial = state
                node, _ = astar(sub, lambda p, st: 0)
                h = s.h_manhattan_scaled(prob, state)
                # assert lanza AssertionError al sobreestimar; la tolerancia evita diferencias numéricas mínimas.
                # Esta prueba muestrea tres estados por cuadrícula, no demuestra el caso general por sí sola.
                assert h <= node.g + 1e-9, (
                    f"h_manhattan_scaled overestimates at {state} on {size}x{size}: "
                    f"h={h} > remaining={node.g}"
                )
    print("  ok  h_manhattan_scaled admissible on sampled states across 40 grids")


def test_manhattan_scaled_dominates_zero():
    # Con una heurística que domina a h_zero, A* no debería expandir más nodos.
    for size in BANK:
        for grid in BANK[size]:
            prob = GridProblem(grid)
            # Mismo objeto problema, dos búsquedas nuevas: se comparan contadores, no segundos de ejecución.
            _, exp_zero = astar(prob, s.h_zero)
            _, exp_manh = astar(prob, s.h_manhattan_scaled)
            assert exp_manh <= exp_zero, (
                f"h_manhattan_scaled expanded MORE than h_zero on {size}x{size}: "
                f"{exp_manh} > {exp_zero}"
            )
    print("  ok  h_manhattan_scaled dominates h_zero (expansions never worse)")


def test_manhattan_scaled_returns_optimal_cost():
    for size in BANK:
        for grid in BANK[size]:
            prob = GridProblem(grid)
            node, _ = astar(prob, s.h_manhattan_scaled)
            # node.g es el atributo de costo acumulado del Node; no es la longitud de node.path().
            assert node.g == _optimal_cost(grid), (
                f"h_manhattan_scaled not optimal on {size}x{size}"
            )
    print("  ok  h_manhattan_scaled preserves optimality on all 40 grids")


def test_inadmissible_heuristic_returns_suboptimal_path():
    """Objetivo de la semana: h_bad debe romper la optimalidad al menos una vez."""
    broken = 0
    total = 0
    for size in BANK:
        for grid in BANK[size]:
            prob = GridProblem(grid)
            node, _ = astar(prob, s.h_bad)
            true_opt = _optimal_cost(grid)
            # Cuenta instancias con una solución estrictamente más cara, sin exigir que h_bad falle en todas.
            if node.g > true_opt:
                broken += 1
            total += 1
    # La prueba PASA cuando observa el fallo deliberado: confirma que no se puede confiar en h_bad.
    assert broken > 0, (
        f"h_bad returned optimal on ALL {total} instances — it is not actually "
        "inadmissible on this bank. Make it overestimate more aggressively."
    )
    print(f"  ok  h_bad broke optimality on {broken}/{total} instances "
          f"(and that is the lesson)")


# Las funciones son objetos: esta lista guarda referencias; main las ejecuta después con t().
TESTS = [
    test_h_zero_admissible_and_optimal,
    test_manhattan_scaled_is_admissible,
    test_manhattan_scaled_dominates_zero,
    test_manhattan_scaled_returns_optimal_cost,
    test_inadmissible_heuristic_returns_suboptimal_path,
]


def main():
    # Cuenta tareas pendientes y aserciones fallidas; mantiene el resto de pruebas en ejecución.
    failed = 0
    for t in TESTS:
        try:
            t()
        # Puede aparecer mientras las heurísticas de starter conserven sus TODO originales.
        except NotImplementedError:
            print(f"  --  {t.__name__}: heuristic not implemented yet")
            failed += 1
        # e es el objeto excepción; su mensaje explica la condición que no se cumplió.
        except AssertionError as e:
            print(f"  FAIL {t.__name__}: {e}")
            failed += 1
    if failed:
        print(f"\n{failed}/{len(TESTS)} failed")
        # Código de salida 1 si hubo fallos; sin fallos termina normalmente con código 0.
        sys.exit(1)
    print(f"\nall {len(TESTS)} tests pass")


# Lanza las pruebas al ejecutar este archivo, no al importarlo para usarlas desde otro módulo.
if __name__ == "__main__":
    main()
