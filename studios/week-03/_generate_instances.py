"""Generador de instancias para el estudio de la semana 3 (8-puzzle).

Ejecutar una sola vez durante la generación; guarda ``instances.json``
en el mismo directorio. Determinístico (SEED=20260807).

El método es exactamente el del apéndice del notebook: una búsqueda BFS exhaustiva
*hacia atrás desde el estado objetivo* etiqueta cada uno de los 181 440 estados
alcanzables con su verdadera profundidad óptima.

Luego muestreamos PER_DEPTH instancias para cada profundidad objetivo. Debido a que
las profundidades se obtienen directamente de la BFS exhaustiva, la longitud óptima
de la solución de cada instancia es exacta; nunca se debe confiar en una profundidad
de un puzzle etiquetada manualmente, incluyendo estas.

Las cuatro instancias canónicas del notebook (D8, D12, D16 -> sus respectivos grupos)
se fijan como la primera entrada de su profundidad correspondiente, de modo que los
datos del notebook aparezcan literalmente en el banco de instancias.
"""
import json
import random
from collections import deque
from pathlib import Path

# Importamos del archivo search.py:
# - EightPuzzle: la clase que representa el problema del 8-puzzle.
# - GOAL: el estado objetivo.
# - D8, D12, D16: estados conocidos con profundidad óptima 8, 12 y 16.
from search import EightPuzzle, GOAL, D8, D12, D16


# Semilla fija para que la selección aleatoria sea reproducible.
# Esto significa que, si ejecutamos el programa varias veces,
# se elegirán los mismos estados.
SEED = 20260807

# Profundidades óptimas que queremos incluir en nuestro conjunto de instancias.
DEPTHS = [4, 8, 12, 16]

# Número de instancias que queremos seleccionar por cada profundidad.
PER_DEPTH = 10

# Estados "fijados" que queremos conservar obligatoriamente
# porque ya aparecen en el notebook.
PINNED = {
    8: D8,
    12: D12,
    16: D16
}


# La BFS parte del objetivo porque cada movimiento del rompecabezas es reversible.
# Con costo 1 por movimiento, la primera visita da la distancia mínima también hacia GOAL.
def true_depths():
    """
    Realiza una BFS exhaustiva empezando desde GOAL y avanzando hacia atrás.

    Retorna:
        Un diccionario de la forma:
        {estado: profundidad_optima}

    La profundidad representa el número mínimo de movimientos
    necesarios para llegar desde ese estado hasta GOAL.
    """

    # El estado objetivo tiene distancia 0 respecto de sí mismo.
    dist = {GOAL: 0}

    # deque se usa como una cola FIFO para implementar BFS.
    # Empezamos colocando GOAL en la cola.
    q = deque([GOAL])

    # Creamos un objeto EightPuzzle para poder usar sus métodos
    # actions() y result().
    # POO: EightPuzzle hereda de Problem. pz es una instancia; sus métodos reciben self implícitamente.
    # actions(s) y result(s, a) trabajan con el estado pasado, sin cambiar pz.initial.
    pz = EightPuzzle(GOAL)

    # Mientras existan estados pendientes por explorar...
    while q:

        # Extraemos el primer estado de la cola.
        # Esto mantiene el comportamiento FIFO de BFS.
        s = q.popleft()

        # Obtenemos todas las acciones válidas desde el estado s.
        for a in pz.actions(s):

            # Aplicamos la acción a para obtener un nuevo estado t.
            t = pz.result(s, a)

            # Si todavía no hemos visitado ese estado...
            if t not in dist:

                # Su profundidad es una unidad mayor que la de su padre.
                dist[t] = dist[s] + 1

                # Lo agregamos a la cola para explorarlo después.
                q.append(t)

    # Retornamos el diccionario con todos los estados alcanzables
    # y su profundidad óptima.
    return dist


def main():
    # Calculamos la profundidad óptima de todos los estados alcanzables.
    dist = true_depths()

    # Mostramos cuántos estados fueron encontrados
    # y cuál es la profundidad máxima del 8-puzzle.
    print(
        f"reachable states: {len(dist):,}   "
        f"hardest: {max(dist.values())} moves"
    )

    # Creamos un diccionario para agrupar estados según su profundidad.
    #
    # Ejemplo:
    # {
    #   4:  [estados con profundidad 4],
    #   8:  [estados con profundidad 8],
    #   12: [estados con profundidad 12],
    #   16: [estados con profundidad 16]
    # }
    by_depth = {d: [] for d in DEPTHS}

    # Recorremos todos los estados encontrados por BFS.
    for state, d in dist.items():

        # Solo guardamos estados cuya profundidad
        # está dentro de DEPTHS.
        if d in by_depth:
            by_depth[d].append(state)

    # Creamos un generador pseudoaleatorio usando una semilla fija.
    # Gracias a SEED, el resultado será siempre reproducible.
    # Random es una clase; rng es una instancia con estado pseudoaleatorio propio.
    # shuffle es su método: modifica pool en el lugar sin usar el generador global del módulo random.
    rng = random.Random(SEED)

    # Diccionario que finalmente será guardado como JSON.
    out = {
        "seed": SEED,
        "depths": DEPTHS,
        "per_depth": PER_DEPTH,
        "instances": {}
    }

    # Procesamos cada profundidad deseada.
    for d in DEPTHS:

        # Ordenamos los estados primero para garantizar un orden inicial
        # determinista antes de mezclarlos.
        pool = sorted(by_depth[d])

        # Mezclamos los estados de manera pseudoaleatoria.
        rng.shuffle(pool)

        # Elegimos las primeras PER_DEPTH instancias.
        chosen = pool[:PER_DEPTH]

        # Si existe una instancia PINNED para esta profundidad
        # y no fue seleccionada aleatoriamente...
        if d in PINNED and PINNED[d] not in chosen:

            # La ponemos obligatoriamente al inicio
            # y completamos el resto con otras instancias.
            chosen = [PINNED[d]] + chosen[:PER_DEPTH - 1]

        # Si la instancia PINNED ya estaba dentro de chosen...
        elif d in PINNED:

            # La quitamos de su posición actual.
            chosen.remove(PINNED[d])

            # Y la movemos al primer lugar.
            chosen = [PINNED[d]] + chosen

        # Verificación de seguridad:
        # comprobamos que cada estado seleccionado
        # realmente tenga la profundidad óptima esperada.
        for st in chosen:
            assert dist[st] == d, (st, dist[st], d)

        # Convertimos cada tupla de estado en lista
        # porque JSON trabaja naturalmente con listas.
        out["instances"][str(d)] = [list(st) for st in chosen]

    # Construimos la ruta del archivo instances.json
    # en la misma carpeta donde está este script.
    # Path representa una ruta como objeto. with_name devuelve otra ruta en la misma carpeta;
    # write_text escribe y reemplaza el archivo de destino cuando se ejecuta main().
    dest = Path(__file__).with_name("instances.json")

    # Convertimos el diccionario out a formato JSON
    # y lo escribimos en el archivo.
    #
    # indent=2 sirve para que el JSON quede ordenado y legible.
    dest.write_text(json.dumps(out, indent=2))

    # Contamos cuántas instancias fueron guardadas en total.
    n = sum(len(v) for v in out["instances"].values())

    # Mostramos un mensaje indicando dónde se guardó el archivo
    # y cuántas instancias contiene.
    print(
        f"wrote {dest} -- {n} instances across depths {DEPTHS}"
    )


# Esta condición verifica si el archivo está siendo ejecutado directamente.
#
# Si lo ejecutamos como script, se llama a main().
# Si se importa desde otro archivo, main() no se ejecuta automáticamente.
if __name__ == "__main__":
    main()