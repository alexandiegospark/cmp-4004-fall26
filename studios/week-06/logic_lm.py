"""
Week 6 — Logic-LM, brazo B.

Este archivo YA ESTÁ DADO y no debes modificarlo.

Su trabajo es:

1. Crear el prompt que convierte lenguaje natural -> CSP en JSON.
2. Extraer JSON de la respuesta del LLM.
3. Convertir ese JSON en un CSP real.
4. Resolverlo con el MISMO backtracking de csp.py.
5. Clasificar si la respuesta del modelo fue correcta o falló.

La idea importante es:

Lenguaje natural
      ↓
     LLM
      ↓
  CSP en JSON
      ↓
backtrack_search()
      ↓
   solución
"""

import json
import re
from pathlib import Path

# Reutilizamos exactamente el mismo solver CSP de la semana.
from csp import backtrack_search


# Archivo que contiene los 20 puzzles verificados.
PUZZLE_BANK = Path(__file__).with_name("puzzles.json")


# =========================================================
# PROMPT PARA EL MODELO
# =========================================================

# Este es el prompt exacto que recibe el LLM.
# El modelo NO debe resolver el puzzle:
# debe traducirlo a una representación CSP.
MODEL_PROMPT = """Translate this logic puzzle into a CSP in the JSON format below.
Do not solve it. Output only JSON.

{{"variables": {{"name": ["domain", "values"]}},
  "constraints": [{{"type": "alldiff", "vars": [...]}},
                  {{"type": "neq", "a": "X", "b": "Y"}},
                  {{"type": "eq",  "a": "X", "b": "value"}}]}}

Puzzle:
{puzzle}"""


# =========================================================
# ERRORES PERSONALIZADOS
# =========================================================

class ParseError(Exception):
    """
    Se lanza cuando la respuesta del LLM
    no contiene un JSON recuperable.
    """
    pass


class ModelError(Exception):
    """
    Se lanza cuando sí existe JSON,
    pero no representa correctamente un CSP.
    """
    pass


# =========================================================
# EXTRAER JSON DE LA RESPUESTA DEL LLM
# =========================================================

def parse_json(text):
    """
    Busca el primer objeto JSON {...} dentro de la respuesta.

    El modelo podría responder:

        Aquí está el JSON:
        ```json
        {...}
        ```

    Esta función intenta ignorar ese texto adicional
    y recuperar solamente el JSON.
    """

    # Si el modelo no respondió nada.
    if text is None:
        raise ParseError("empty reply")

    # Primero intenta encontrar JSON dentro de:
    # ```json
    # {...}
    # ```
    fenced = re.search(
        r"```(?:json)?\s*(\{.*?\})\s*```",
        text,
        re.DOTALL
    )

    candidate = fenced.group(1) if fenced else None

    # Si no estaba dentro de un bloque ```json```,
    # buscamos manualmente las llaves.
    if candidate is None:

        # Primera llave de apertura.
        start = text.find("{")

        if start == -1:
            raise ParseError("no '{' in reply")

        depth = 0

        # Buscamos hasta que las llaves estén balanceadas.
        for i in range(start, len(text)):

            if text[i] == "{":
                depth += 1

            elif text[i] == "}":
                depth -= 1

                # depth == 0 significa que encontramos
                # el cierre del objeto JSON principal.
                if depth == 0:
                    candidate = text[start:i + 1]
                    break

        if candidate is None:
            raise ParseError("unbalanced braces")

    # Intentamos convertir el texto a un objeto Python.
    try:
        return json.loads(candidate)

    except json.JSONDecodeError as e:
        raise ParseError(
            f"invalid JSON: {e}"
        ) from e


# =========================================================
# CSP GENERADO A PARTIR DEL JSON DEL MODELO
# =========================================================

class _SpecCSP:
    """
    Representa el CSP generado a partir del JSON del LLM.

    Tiene la misma interfaz que espera backtrack_search:

        variables
        domains
        neighbors
        consistent()
        degree()

    Soporta:

        alldiff
        neq
        eq
    """

    def __init__(self, variables, domains, constraints):

        # Variables del problema.
        self.variables = list(variables)

        # Dominio posible de cada variable.
        self.domains = {
            v: set(domains[v])
            for v in variables
        }

        # Restricciones traducidas por el LLM.
        self.constraints = constraints

        # Vecinos de cada variable.
        self.neighbors = {
            v: set()
            for v in variables
        }

        # Restricciones binarias internas.
        # Ejemplo:
        # ("Ana", "Bob", "neq")
        self._binary = []

        varset = set(variables)

        # Procesamos cada restricción del JSON.
        for con in constraints:

            t = con.get("type")

            # ---------------------------------------------
            # ALLDIFF
            # ---------------------------------------------
            if t == "alldiff":

                vs = con["vars"]

                # alldiff(A,B,C) se transforma internamente
                # en restricciones de desigualdad por pares.
                for i, a in enumerate(vs):

                    for b in vs[i + 1:]:

                        self._link(a, b)

                        self._binary.append(
                            (a, b, "neq")
                        )

            # ---------------------------------------------
            # NEQ
            # ---------------------------------------------
            elif t == "neq":

                a, b = con["a"], con["b"]

                # Caso:
                # X != Y
                if a in varset and b in varset:

                    self._link(a, b)

                    self._binary.append(
                        (a, b, "neq")
                    )

                # Caso:
                # X != valor
                elif a in varset:

                    # Eliminamos directamente ese valor
                    # del dominio de X.
                    self.domains[a].discard(b)

                else:
                    raise ModelError(
                        f"neq references unknown variable: {a}"
                    )

            # ---------------------------------------------
            # EQ
            # ---------------------------------------------
            elif t == "eq":

                # Caso:
                # X == valor
                #
                # Reducimos el dominio de X
                # a un único valor.
                a, val = con["a"], con["b"]

                if a not in varset:
                    raise ModelError(
                        f"eq references unknown variable: {a}"
                    )

                self.domains[a] = (
                    {val}
                    if val in self.domains[a]
                    else set()
                )

            # Tipo de restricción desconocido.
            else:
                raise ModelError(
                    f"unknown constraint type {t!r}"
                )

    def _link(self, a, b):
        """
        Marca dos variables como vecinas,
        es decir, relacionadas por una restricción.
        """

        # Ambas deben existir.
        if (
            a not in self.neighbors
            or b not in self.neighbors
        ):
            raise ModelError(
                f"constraint references unknown variable: {a} / {b}"
            )

        # La relación es bidireccional.
        self.neighbors[a].add(b)
        self.neighbors[b].add(a)

    def consistent(self, var, value, assignment):
        """
        Comprueba si asignar value a var
        viola alguna restricción binaria.
        """

        for (a, b, kind) in self._binary:

            if kind != "neq":
                continue

            # var = a y b ya tiene el mismo valor.
            if (
                var == a
                and b in assignment
                and assignment[b] == value
            ):
                return False

            # var = b y a ya tiene el mismo valor.
            if (
                var == b
                and a in assignment
                and assignment[a] == value
            ):
                return False

        return True

    def degree(self, var):
        """
        Número de variables vecinas.

        Se utiliza, por ejemplo, como criterio
        de desempate junto con MRV.
        """
        return len(self.neighbors[var])


# =========================================================
# CONVERTIR JSON -> CSP
# =========================================================

def build_csp(spec):
    """
    Valida el JSON generado por el modelo
    y construye un CSP que el solver pueda resolver.

    Si la estructura está mal,
    lanza ModelError.
    """

    # Debe ser un diccionario y contener "variables".
    if (
        not isinstance(spec, dict)
        or "variables" not in spec
    ):
        raise ModelError(
            "spec missing 'variables'"
        )

    variables = spec["variables"]

    # "variables" debe ser un objeto no vacío.
    if (
        not isinstance(variables, dict)
        or not variables
    ):
        raise ModelError(
            "'variables' must be a non-empty object"
        )

    domains = {}

    # Validamos el dominio de cada variable.
    for name, dom in variables.items():

        if (
            not isinstance(dom, list)
            or not dom
        ):
            raise ModelError(
                f"variable {name!r} has an empty/invalid domain"
            )

        domains[name] = list(dom)

    # Si no existen restricciones,
    # usamos una lista vacía.
    constraints = spec.get(
        "constraints",
        []
    )

    if not isinstance(constraints, list):
        raise ModelError(
            "'constraints' must be a list"
        )

    # Creamos el objeto CSP.
    return _SpecCSP(
        list(variables),
        domains,
        constraints
    )


# =========================================================
# CATEGORÍAS DE RESULTADO DEL BRAZO B
# =========================================================

# El modelo respondió algo que no se pudo interpretar como JSON.
MALFORMED = "malformed_json"

# El JSON era utilizable, pero modeló mal el puzzle
# y produjo una respuesta diferente al gold.
WRONG_MODEL = "valid_json_wrong_model"

# El modelo creó un CSP demasiado restrictivo
# y el solver demuestra que no tiene solución.
NO_SOLUTION = "valid_no_solution"

# El solver excedió el límite de llamadas.
TIMEOUT = "timeout"

# La solución coincide con la respuesta correcta.
OK = "correct"


# =========================================================
# PIPELINE COMPLETO DEL BRAZO B
# =========================================================

def classify_arm_b(
    reply,
    gold=None,
    limit=200_000
):
    """
    Ejecuta todo el pipeline sobre una respuesta del LLM.

    Flujo:

        respuesta del LLM
              ↓
          parse_json
              ↓
           build_csp
              ↓
       backtrack_search
              ↓
      comparar con gold
              ↓
        categoría final

    Devuelve:

        (categoria, solucion)
    """

    # ---------------------------------------------
    # 1. PARSEAR JSON
    # ---------------------------------------------

    try:
        spec = parse_json(reply)

    except ParseError:

        # Ni siquiera pudimos recuperar JSON.
        return MALFORMED, None

    # ---------------------------------------------
    # 2. CONSTRUIR CSP
    # ---------------------------------------------

    try:
        csp = build_csp(spec)

    except ModelError:

        # El JSON existe, pero su estructura
        # no permite construir un CSP.
        return MALFORMED, None

    # ---------------------------------------------
    # 3. RESOLVER CSP
    # ---------------------------------------------

    # Usamos el MISMO solver de csp.py,
    # activando Forward Checking y MRV.
    sol, counter = backtrack_search(
        csp,
        use_fc=True,
        use_mrv=True,
        limit=limit
    )

    # El solver agotó el límite de búsqueda.
    if sol == "TIMEOUT":
        return TIMEOUT, None

    # El CSP no tiene ninguna solución.
    #
    # Normalmente indica que el LLM tradujo
    # mal el puzzle y lo sobre-restringió.
    if sol is None:
        return NO_SOLUTION, None

    # ---------------------------------------------
    # 4. COMPARAR CONTRA LA RESPUESTA CORRECTA
    # ---------------------------------------------

    if gold is not None:

        # Si alguna variable no coincide con gold,
        # el modelo CSP estaba equivocado.
        if any(
            sol.get(k) != v
            for k, v in gold.items()
        ):
            return WRONG_MODEL, sol

    # Todo funcionó correctamente.
    return OK, sol


# =========================================================
# EJEMPLOS FEW-SHOT
# =========================================================

# Estos ejemplos muestran al modelo cómo transformar:
#
# lenguaje natural -> variables + dominios + restricciones.
#
# Cada ejemplo tiene:
#
# puzzle -> texto original
# spec   -> CSP correcto
# gold   -> solución correcta

EXAMPLE_PUZZLES = [

    # -----------------------------------------------------
    # EJEMPLO 1: COLORES
    # -----------------------------------------------------

    {
        "puzzle": (
            "Three friends -- Ana, Bob, Cara -- each pick a different colour "
            "from red, green, blue. Ana is not red. Bob is blue."
        ),

        "spec": {

            # Cada persona es una variable.
            "variables": {
                "Ana": ["red", "green", "blue"],
                "Bob": ["red", "green", "blue"],
                "Cara": ["red", "green", "blue"]
            },

            "constraints": [

                # Todos eligen un color diferente.
                {
                    "type": "alldiff",
                    "vars": ["Ana", "Bob", "Cara"]
                },

                # Bob = blue.
                {
                    "type": "eq",
                    "a": "Bob",
                    "b": "blue"
                },

                # Ana != red.
                {
                    "type": "neq",
                    "a": "Ana",
                    "b": "red"
                },
            ],
        },

        # Solución correcta.
        "gold": {
            "Ana": "green",
            "Bob": "blue",
            "Cara": "red"
        },
    },


    # -----------------------------------------------------
    # EJEMPLO 2: CASAS
    # -----------------------------------------------------

    {
        "puzzle": (
            "Two houses, numbered 1 and 2, one owned by Xu and one by Yara. "
            "Xu does not live in house 1."
        ),

        "spec": {

            "variables": {
                "Xu": [1, 2],
                "Yara": [1, 2]
            },

            "constraints": [

                # No pueden vivir en la misma casa.
                {
                    "type": "alldiff",
                    "vars": ["Xu", "Yara"]
                },

                # Xu != casa 1.
                {
                    "type": "neq",
                    "a": "Xu",
                    "b": 1
                },
            ],
        },

        "gold": {
            "Xu": 2,
            "Yara": 1
        },
    },


    # -----------------------------------------------------
    # EJEMPLO 3: HORARIOS
    # -----------------------------------------------------

    {
        "puzzle": (
            "Three tasks A, B, C run in slots 1, 2, 3 (all different). "
            "A runs in slot 1. C does not run in slot 2."
        ),

        "spec": {

            # Cada tarea puede ocupar los slots 1, 2 o 3.
            "variables": {
                "A": [1, 2, 3],
                "B": [1, 2, 3],
                "C": [1, 2, 3]
            },

            "constraints": [

                # Las tareas deben usar slots diferentes.
                {
                    "type": "alldiff",
                    "vars": ["A", "B", "C"]
                },

                # A = slot 1.
                {
                    "type": "eq",
                    "a": "A",
                    "b": 1
                },

                # C != slot 2.
                {
                    "type": "neq",
                    "a": "C",
                    "b": 2
                },
            ],
        },

        "gold": {
            "A": 1,
            "B": 2,
            "C": 3
        },
    },
]


# =========================================================
# BANCO COMPLETO DE 20 PUZZLES
# =========================================================

def load_puzzles(path=None):
    """
    Carga los 20 puzzles verificados
    desde puzzles.json.

    Cada puzzle contiene:

        id
        worked_example
        puzzle
        spec
        gold
    """

    # Si no se especifica ruta,
    # usamos puzzles.json junto a este archivo.
    p = (
        Path(path)
        if path
        else PUZZLE_BANK
    )

    # Abrimos el archivo JSON.
    with open(
        p,
        encoding="utf-8"
    ) as fh:

        return json.load(fh)["puzzles"]


# =========================================================
# EJEMPLOS COMPLETAMENTE RESUELTOS
# =========================================================

def worked_examples(path=None):
    """
    Devuelve únicamente los puzzles marcados:

        worked_example = true

    Son 5 ejemplos que pueden utilizarse
    como few-shot examples para el LLM.
    """

    return [
        p
        for p in load_puzzles(path)
        if p.get("worked_example")
    ]