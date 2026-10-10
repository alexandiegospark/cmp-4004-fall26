"""
Week 6 — Motor compartido para CSP.

Este archivo contiene:

- Clase CSP
- Backtracking
- Forward Checking
- MRV + Degree
- LCV
- AC-3
- Sudoku
- Coloreo del mapa de Australia

La idea principal es que en CSP muchas veces la inferencia y la propagación
reducen más el trabajo que simplemente hacer más búsqueda.
"""

from collections import deque
import time
import itertools
import json
from pathlib import Path


# =========================================================
# CLASE CSP
# =========================================================

class CSP:
    """
    Representa un problema de satisfacción de restricciones.

    En POO:
    - variables, dominios y vecinos son atributos.
    - consistent() y degree() son métodos del objeto.
    """

    def __init__(self, variables, domains, neighbors):

        # Lista de variables del problema.
        self.variables = list(variables)

        # Dominio de posibles valores para cada variable.
        self.domains = {
            v: set(domains[v])
            for v in variables
        }

        # Variables relacionadas mediante restricciones.
        self.neighbors = neighbors

        # Guarda valores eliminados temporalmente
        # para poder restaurarlos durante backtracking.
        self.pruned = []

    def consistent(self, var, value, assignment):
        """
        Comprueba si asignar 'value' a 'var'
        viola alguna restricción.

        Aquí usamos una restricción all-different:
        ningún vecino puede tener el mismo valor.
        """

        return all(
            assignment.get(n) != value
            for n in self.neighbors[var]
        )

    def degree(self, var):
        """
        Devuelve cuántos vecinos/restricciones
        tiene una variable.
        """

        return len(self.neighbors[var])


# =========================================================
# CREAR UN CSP DE SUDOKU
# =========================================================

def sudoku_csp(grid):
    """
    Convierte un Sudoku en un CSP.

    grid:
        string de 81 caracteres.

    '.' o '0' significa celda vacía.
    """

    # Cada variable es una posición (fila, columna).
    cells = [
        (r, c)
        for r in range(9)
        for c in range(9)
    ]

    neighbors = {}

    # Construimos los vecinos de cada celda.
    for (r, c) in cells:

        peers = set()

        # Vecinos de la misma fila y columna.
        for k in range(9):
            peers.add((r, k))
            peers.add((k, c))

        # Calculamos el bloque 3x3 al que pertenece.
        br = 3 * (r // 3)
        bc = 3 * (c // 3)

        # Agregamos las celdas del mismo bloque.
        for dr in range(3):
            for dc in range(3):
                peers.add((br + dr, bc + dc))

        # Una celda no es vecina de sí misma.
        peers.discard((r, c))

        neighbors[(r, c)] = peers

    # Creamos los dominios.
    domains = {}

    for i, (r, c) in enumerate(cells):

        ch = grid[i]

        # Si ya existe un número, su dominio tiene un solo valor.
        if ch not in ".0":
            domains[(r, c)] = {int(ch)}

        # Si está vacía, puede ser cualquier número del 1 al 9.
        else:
            domains[(r, c)] = set(range(1, 10))

    # Retornamos un objeto CSP.
    return CSP(
        cells,
        domains,
        neighbors
    )


# =========================================================
# MOSTRAR SUDOKU
# =========================================================

def show_sudoku(assignment):
    """Muestra una asignación en formato Sudoku."""

    for r in range(9):

        row = " ".join(
            str(assignment.get((r, c), "."))
            for c in range(9)
        )

        print(
            row[:5] + "|" +
            row[6:11] + "|" +
            row[12:]
        )

        # Separación visual de los bloques 3x3.
        if r in (2, 5):
            print(
                "-" * 5 +
                "+" +
                "-" * 5 +
                "+" +
                "-" * 5
            )


# =========================================================
# INSTANCIAS DE SUDOKU
# =========================================================

# Sudoku difícil.
HARD = (
    "..............3.85..1.2.......5.7.....4...1...9.......5"
    "......73..2.1........4...9"
)

# Sudoku fácil.
EASY = (
    "53..7....6..195....98....6.8...6...34..8.3..17...2...6"
    ".6....28....419..5....8..79"
)

# Sudoku de dificultad media.
MED = (
    "4.....8.5.3..........7......2.....6.....8.4......1...."
    "...6.3.7.5..2.....1.4......"
)


# =========================================================
# BACKTRACKING
# =========================================================

def backtrack_search(
    csp,
    use_fc=False,
    use_mrv=False,
    use_lcv=False,
    use_ac3=False,
    limit=2_000_000
):
    """
    Resuelve un CSP mediante backtracking.

    Los parámetros permiten activar o desactivar:

    use_fc  -> Forward Checking
    use_mrv -> MRV + Degree
    use_lcv -> Least Constraining Value
    use_ac3 -> AC-3 antes de iniciar la búsqueda
    """

    # Contador de llamadas recursivas.
    counter = {"calls": 0}

    # Copiamos los dominios para no modificar el CSP original.
    domains = {
        v: set(csp.domains[v])
        for v in csp.variables
    }

    # -----------------------------------------------------
    # AC-3 opcional
    # -----------------------------------------------------

    if use_ac3:

        # AC-3 intenta reducir los dominios
        # antes de comenzar la búsqueda.
        if not ac3(csp, domains):
            return None, counter

    # Variables cuyo dominio ya tiene un solo valor
    # pueden asignarse directamente.
    assignment = {
        v: next(iter(domains[v]))
        for v in csp.variables
        if len(domains[v]) == 1
    }

    # -----------------------------------------------------
    # PROPAGAR LOS VALORES INICIALES
    # -----------------------------------------------------

    if use_fc:

        # Eliminamos de los vecinos los valores
        # que ya están asignados.
        for v, val in assignment.items():

            for n in csp.neighbors[v]:

                if n not in assignment:
                    domains[n].discard(val)

    # =====================================================
    # SELECCIÓN DE VARIABLE
    # =====================================================

    def select_unassigned():
        """Selecciona la siguiente variable a asignar."""

        unassigned = [
            v
            for v in csp.variables
            if v not in assignment
        ]

        # Sin MRV: tomamos simplemente la primera.
        if not use_mrv:
            return unassigned[0]

        # MRV:
        # elegimos la variable con menos valores posibles.
        #
        # En empate usamos Degree:
        # elegimos la que tiene más vecinos.
        return min(
            unassigned,
            key=lambda v: (
                len(domains[v]),
                -csp.degree(v)
            )
        )

    # =====================================================
    # ORDENAR VALORES
    # =====================================================

    def order_values(var):
        """Decide en qué orden probar los valores."""

        vals = list(domains[var])

        # Sin LCV usamos el orden normal.
        if not use_lcv:
            return vals

        # LCV:
        # preferimos el valor que elimina menos
        # opciones de los vecinos.
        def conflicts(val):

            return sum(
                1
                for n in csp.neighbors[var]
                if (
                    n not in assignment
                    and val in domains[n]
                )
            )

        return sorted(
            vals,
            key=conflicts
        )

    # =====================================================
    # FORWARD CHECKING
    # =====================================================

    def forward_check(var, value):
        """
        Elimina 'value' de los dominios de los vecinos.

        Si algún dominio queda vacío,
        sabemos inmediatamente que esa decisión falla.
        """

        removed = []

        for n in csp.neighbors[var]:

            if (
                n not in assignment
                and value in domains[n]
            ):

                # Eliminamos el valor.
                domains[n].discard(value)

                # Guardamos qué eliminamos
                # para poder restaurarlo después.
                removed.append((n, value))

                # Si un dominio queda vacío,
                # esta rama no puede producir solución.
                if not domains[n]:
                    return removed, True

        return removed, False

    # =====================================================
    # DESHACER FORWARD CHECKING
    # =====================================================

    def undo(removed):
        """Restaura valores eliminados durante backtracking."""

        for n, value in removed:
            domains[n].add(value)

    # =====================================================
    # BACKTRACKING RECURSIVO
    # =====================================================

    def recurse():

        # Contamos cada llamada recursiva.
        counter["calls"] += 1

        # Evitamos búsquedas demasiado grandes.
        if counter["calls"] > limit:
            raise TimeoutError(
                "call limit exceeded"
            )

        # Si todas las variables están asignadas,
        # encontramos una solución.
        if len(assignment) == len(csp.variables):
            return dict(assignment)

        # Elegimos la siguiente variable.
        var = select_unassigned()

        # Probamos sus posibles valores.
        for value in order_values(var):

            # Solo continuamos si no viola restricciones.
            if csp.consistent(
                var,
                value,
                assignment
            ):

                # Asignamos temporalmente.
                assignment[var] = value

                removed = []
                wiped = False

                # Forward checking opcional.
                if use_fc:
                    removed, wiped = forward_check(
                        var,
                        value
                    )

                # Si ningún dominio quedó vacío,
                # continuamos recursivamente.
                if not wiped:

                    result = recurse()

                    if result is not None:
                        return result

                # Si falló, restauramos los dominios.
                if use_fc:
                    undo(removed)

                # BACKTRACK:
                # eliminamos la asignación y probamos otra.
                del assignment[var]

        # Ningún valor funcionó.
        return None

    # Ejecutamos la búsqueda.
    try:
        return recurse(), counter

    # Si superamos el límite de llamadas.
    except TimeoutError:
        return "TIMEOUT", counter


# =========================================================
# AC-3
# =========================================================

def ac3(csp, domains):
    """
    Algoritmo AC-3.

    Intenta eliminar valores imposibles de los dominios
    antes o durante la resolución del CSP.

    Devuelve False si detecta una inconsistencia.
    """

    # Creamos una cola con todos los arcos (X, Y).
    queue = deque(
        (x, y)
        for x in csp.variables
        for y in csp.neighbors[x]
    )

    def revise(x, y):
        """
        Revisa si algún valor del dominio de X
        no tiene soporte en Y.
        """

        removed = False

        # Usamos copia porque podemos modificar domains[x].
        for vx in set(domains[x]):

            # Como la restricción es all-different,
            # vx es válido si existe algún valor en Y
            # diferente de vx.
            if not any(
                vy != vx
                for vy in domains[y]
            ):

                domains[x].discard(vx)
                removed = True

        return removed

    # Continuamos hasta alcanzar un punto fijo:
    # es decir, hasta que ya no haya más cambios.
    while queue:

        x, y = queue.popleft()

        # Si el dominio de X cambió...
        if revise(x, y):

            # Si quedó vacío, el problema es inconsistente.
            if not domains[x]:
                return False

            # Como X cambió, debemos revisar
            # nuevamente sus otros vecinos.
            for z in csp.neighbors[x]:

                if z != y:
                    queue.append((z, x))

    return True


# =========================================================
# COLOREO DEL MAPA DE AUSTRALIA
# =========================================================

# Regiones vecinas.
AUS_NEIGHBORS = {
    "WA": {"NT", "SA"},
    "NT": {"WA", "SA", "Q"},
    "SA": {"WA", "NT", "Q", "NSW", "V"},
    "Q": {"NT", "SA", "NSW"},
    "NSW": {"Q", "SA", "V"},
    "V": {"SA", "NSW", "T"},
    "T": {"V"},
}


# Dominio de colores posibles.
COLORS = {
    "red",
    "green",
    "blue"
}


def australia_csp(colors=None):
    """
    Crea el problema de colorear Australia.

    Restricción:
    regiones vecinas no pueden tener el mismo color.
    """

    colors = colors or COLORS

    return CSP(
        list(AUS_NEIGHBORS),

        # Cada región puede inicialmente usar cualquier color.
        {
            v: set(colors)
            for v in AUS_NEIGHBORS
        },

        AUS_NEIGHBORS
    )


# =========================================================
# VERIFICAR SOLUCIÓN DE SUDOKU
# =========================================================

def valid_sudoku(sol, csp):
    """
    Comprueba independientemente que una solución
    de Sudoku sea válida.
    """

    for var, val in sol.items():

        for n in csp.neighbors[var]:

            # Dos vecinos no pueden tener el mismo valor.
            if sol[n] == val:
                return False

    # Debe haber 81 valores y todos entre 1 y 9.
    return (
        len(sol) == 81
        and all(
            1 <= v <= 9
            for v in sol.values()
        )
    )


# =========================================================
# VERIFICADOR GENÉRICO DE CSP
# =========================================================

def solution_consistent(sol, csp):
    """
    Comprueba que una solución:

    - exista
    - sea completa
    - no viole restricciones
    """

    # No aceptamos fallo ni timeout.
    if sol in (None, "TIMEOUT"):
        return False

    # Deben estar asignadas todas las variables.
    if len(sol) != len(csp.variables):
        return False

    for var in csp.variables:

        # Cada variable debe aparecer.
        if var not in sol:
            return False

        # Ningún vecino puede tener el mismo valor.
        for n in csp.neighbors[var]:

            if sol.get(n) == sol[var]:
                return False

    return True