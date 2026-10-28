"""Ayudantes de la tarea 2 de la semana 4: duelo del LLM frente a A* con el mismo banco.

No necesitas modificar el código para el ejercicio. Implementa ``call_llm``
en tu script o usa ``aicourse.llm.LLM`` y entrega las salidas a
``score_llm_reply`` para cada instancia. Las categorías del plan son:

    illegal    — camino no contiguo o que sale de los límites
    suboptimal — camino legal cuyo costo supera el óptimo de A*
    wrong_cost — camino legal y óptimo, pero con costo declarado incorrecto
    correct    — camino legal, óptimo y con costo declarado correcto

La tercera categoría es especialmente interesante: un modelo puede producir
un camino correcto y declarar un costo incorrecto. Nunca confíes en el costo
que declara el modelo; vuelve a calcularlo siempre con el verificador.
"""
from dataclasses import dataclass
from typing import Optional

from gridworld import GridProblem, MOVES, TERRAIN, astar, load_instances, render


# El prompt y las etiquetas PATH:/COST: se conservan en inglés: forman el protocolo del experimento.
# render convierte la cuadrícula a texto sin alterar los datos originales.
def prompt_for(grid) -> str:
    """Devuelve el prompt exacto del plan de clase."""
    return (
        "Find the minimum-cost path from S to G.\n"
        "Terrain costs: '.' = 1, ',' = 3, '~' = 8.\n"
        "Move up/down/left/right only.\n"
        "Grid:\n" + render(grid) + "\n\n"
        "Reply with the path as a sequence of moves (U/D/L/R) and its total cost.\n"
        "Format your final answer as two lines:\n"
        "PATH: <letters, no separators>\n"
        "COST: <integer>\n"
    )


# POO: @dataclass transforma esta clase de datos y genera __init__, __repr__ y __eq__.
# Scored(...) crea una instancia; scored.category o scored.checker_cost acceden a sus atributos.
# No hereda de GridProblem ni ejecuta la evaluación por sí misma: solo reúne sus resultados.
# Las anotaciones describen tipos, pero no validan los valores automáticamente durante la ejecución.
@dataclass
class Scored:
    category: str          # 'illegal' | 'suboptimal' | 'wrong_cost' | 'correct'
    # Optional[str] admite texto o None; Optional[int] admite un entero o None.
    # No son valores por defecto: el inicializador generado recibe los cinco campos.
    llm_path: Optional[str]
    llm_reported_cost: Optional[int]
    checker_cost: Optional[int]
    optimal_cost: int


def _walk(grid, path: str):
    """Devuelve (end_state, total_cost), o (None, None) si el camino es ilegal."""
    # Instanciación: este objeto contiene la cuadrícula, sus dimensiones, el inicio y el objetivo.
    prob = GridProblem(grid)
    state = prob.initial
    total = 0
    # Simula cada letra del camino; MOVES define el desplazamiento de una celda contigua.
    for ch in path:
        if ch not in MOVES:
            return None, None
        dr, dc = MOVES[ch]
        r, c = state[0] + dr, state[1] + dc
        if not (0 <= r < prob.rows and 0 <= c < prob.cols):
            return None, None
        state = (r, c)
        # Cobra la celda de destino, igual que GridProblem.step_cost; no cobra el inicio de nuevo.
        total += TERRAIN[prob.grid[r][c]]
    return state, total


# Separa la respuesta declarada por el LLM de la comprobación independiente del camino y su costo.
# El tipo de retorno Scored indica que el resultado será una instancia de la clase de datos.
def score_llm_reply(grid, llm_path: str, llm_reported_cost: int) -> Scored:
    # Instanciación: este objeto contiene la cuadrícula, sus dimensiones, el inicio y el objetivo.
    prob = GridProblem(grid)
    node, _ = astar(prob, lambda p, st: 0)         # óptimo de referencia
    # h=0 convierte A* en búsqueda de costo uniforme: sirve de referencia con estos costos positivos.
    # .g accede al costo acumulado del nodo objetivo; no se toma del texto generado por el LLM.
    optimal = node.g
    # Normaliza la cadena con métodos str; una ruta None se trata como una cadena vacía.
    # El verificador recorre los movimientos y calcula por su cuenta el destino y el costo.
    end, checker_cost = _walk(grid, (llm_path or "").strip().upper())
    # El orden de estas ramas fija la categoría: primero legalidad y destino, luego optimalidad y costo declarado.
    if end is None or end != prob.goal:
        return Scored("illegal", llm_path, llm_reported_cost, checker_cost, optimal)
    if checker_cost > optimal:
        return Scored("suboptimal", llm_path, llm_reported_cost, checker_cost, optimal)
    if llm_reported_cost != checker_cost:
        return Scored("wrong_cost", llm_path, llm_reported_cost, checker_cost, optimal)
    # Construye un objeto resultado mediante el __init__ que generó @dataclass.
    return Scored("correct", llm_path, llm_reported_cost, checker_cost, optimal)


def parse_reply(text: str):
    """Extrae las líneas PATH: y COST:. Devuelve (path, cost); los campos ausentes o inválidos pueden ser None."""
    path, cost = None, None
    # splitlines, strip, upper, startswith y replace son métodos del objeto str.
    # Solo interpreta líneas con las etiquetas esperadas; otras explicaciones se ignoran.
    for line in text.splitlines():
        line = line.strip()
        # Si aparecen varias líneas de la misma etiqueta, la última sustituye el valor anterior.
        if line.upper().startswith("PATH:"):
            path = line.split(":", 1)[1].strip().upper().replace(" ", "")
        elif line.upper().startswith("COST:"):
            try:
                cost = int(line.split(":", 1)[1].strip())
            # int puede fallar con texto que no represente un entero; se conserva None para ese costo.
            except ValueError:
                cost = None
    return path, cost


# Ejecuta la demostración al lanzar el archivo, no al importarlo desde el notebook.
if __name__ == "__main__":
    # Demostración: evalúa una respuesta incorrecta preparada a mano para comprobar el proceso.
    grid = load_instances()[5][0]
    print("Sample 5x5 grid:")
    print(render(grid))
    print("\nGround-truth optimum via A*:",
          astar(GridProblem(grid), lambda p, st: 0)[0].g)
    # Respuesta deliberadamente ilegal
    scored = score_llm_reply(grid, "RRRRRR", 6)
    print("Scored illegal reply:", scored)
