"""Generador de instancias del taller de la semana 4. Ejecútalo al preparar
el material y guarda ``instances.json`` junto al script en el repositorio.
Es determinista con SEED=20260807.

Las instancias tienen solución: existe un camino de costo finito. Son no
triviales, con inicio y objetivo distintos y no adyacentes. No se garantiza
una distribución específica de costos óptimos: el objetivo del taller es medir.
"""
import json
import random
from pathlib import Path

from gridworld import GridProblem, astar

SEED = 20260807
SIZES = [5, 8, 12, 16]
PER_SIZE = 10
# Distribución de terreno: principalmente camino, algo de hierba y poca agua.
WEIGHTS = {".": 0.60, ",": 0.28, "~": 0.12}


# rng es un objeto random.Random recibido como argumento; concentra el estado pseudoaleatorio.
# La función devuelve una lista de cadenas, una por cada fila de una cuadrícula n×n.
def random_grid(n, rng):
    while True:
        # Comprensiones anidadas crean filas y celdas; choices selecciona símbolos según WEIGHTS.
        # [0] extrae el elemento de la lista que devuelve choices para una selección.
        cells = [
            [rng.choices(list(WEIGHTS), weights=list(WEIGHTS.values()))[0]
             for _ in range(n)]
            for _ in range(n)
        ]
        # S en la región superior izquierda y G en la inferior derecha: separación no trivial.
        sr, sc = rng.randint(0, n // 2 - 1) if n > 2 else 0, rng.randint(0, n // 2 - 1) if n > 2 else 0
        gr, gc = rng.randint(n // 2, n - 1), rng.randint(n // 2, n - 1)
        # Si coincidieran las posiciones, descarta este intento y vuelve a generar una cuadrícula.
        if (sr, sc) == (gr, gc):
            continue
        cells[sr][sc] = "S"
        cells[gr][gc] = "G"
        grid = ["".join(row) for row in cells]
        # Comprobación de existencia de solución: los terrenos actuales son transitables; se conserva
        # la verificación porque cuesta poco y será útil si se añaden paredes.
        # POO: crea un problema para verificar la cuadrícula con la interfaz de A*.
        # lambda p, s: 0 es una función heurística sin información; produce búsqueda de costo uniforme.
        prob = GridProblem(grid)
        node, _ = astar(prob, lambda p, s: 0)
        if node is not None:
            return grid


def main():
    # Random es una clase: la instancia rng tiene su propia secuencia reproducible con esta semilla.
    rng = random.Random(SEED)
    out = {"seed": SEED, "sizes": SIZES, "per_size": PER_SIZE, "instances": {}}
    for n in SIZES:
        out["instances"][str(n)] = [random_grid(n, rng) for _ in range(PER_SIZE)]
    # Path es una clase que representa rutas; with_name devuelve una ruta en la carpeta del script.
    # write_text es un método de esa instancia y reemplaza el archivo de salida al ejecutar main().
    dest = Path(__file__).with_name("instances.json")
    # dumps serializa a JSON; indent=2 facilita leer el resultado sin cambiar sus datos.
    dest.write_text(json.dumps(out, indent=2))
    print(f"wrote {dest} — {sum(len(v) for v in out['instances'].values())} grids")


# Importar el módulo no genera archivos: main solo se llama al ejecutar este script directamente.
if __name__ == "__main__":
    main()
