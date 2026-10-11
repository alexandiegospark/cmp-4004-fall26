"""Taller de la semana 1 — SOLUCIÓN DE REFERENCIA (solo para el docente).

Versión completada de ``starter.py``: conserva los nombres y las firmas de las
funciones para que ``test_eliza.py`` pase al importar este módulo como ``starter``.
La verificación descrita por el material usa ``studios/_verify_solutions.py``:
registra este archivo con el nombre ``starter`` y ejecuta las pruebas sin cambios.

NO distribuir a estudiantes: se excluye mediante ``studios/.gitignore``.
La explicación didáctica está en ``solution.ipynb``, que importa este archivo
en lugar de copiarlo, para mantener ambas versiones sincronizadas.
"""
# Este módulo usa programación por funciones
import re

from eliza import RULES, FALLBACK, REFLECT, reflect, respond
import eliza
import random


# ---- Tarea 1a: añade TRES reglas nuevas -------------------------------------
def new_rules():
    """Tres reglas nuevas con un disparador real: ninguna coincide con una
    cadena vacía ni duplica un patrón base de ``eliza.RULES``."""
    # Cada regla es una tupla: patrón de búsqueda y lista de respuestas posibles.
    # (.*) captura texto; {0} recibe ese texto después de sustituir sus pronombres.
    return [
        (r"\bI want (.*)", ["What would it mean to you to get {0}?",
                            "Why do you want {0}?"]),
        (r"\bI can't (.*)", ["What makes you feel you can't {0}?",
                             "Have you ever been able to {0}?"]),
        (r"\bI think (.*)", ["Do you really think {0}?",
                             "What led you to think {0}?"]),
    ]


# ---- Tarea 1b: función de respuesta ampliada --------------------------------
def extended_respond(text):
    """Aplica PRIMERO las reglas base, luego ``new_rules()`` y finalmente
    una respuesta por defecto. Reutiliza el bucle de ``eliza.respond`` con la tabla combinada."""
    # + crea una lista combinada sin modificar RULES; el orden fija la prioridad.
    for pattern, templates in RULES + new_rules():
        # re.search devuelve un objeto Match o None; IGNORECASE ignora mayúsculas.
        m = re.search(pattern, text, re.IGNORECASE)
        if m:
            # En POO, m.groups() es un método del objeto Match: obtiene sus grupos.
            # La comprensión de lista transforma cada grupo mediante reflect.
            groups = [reflect(g) for g in m.groups()]
            # choice elige una plantilla; str.format es un método del objeto cadena.
            # *groups desempaqueta la lista como argumentos; return termina la búsqueda.
            return random.choice(templates).format(*groups)
    # Solo llegamos aquí si ninguna regla coincidió: usamos una respuesta por defecto.
    return random.choice(FALLBACK)


# ---- Tarea 1c: declara tu fallo deliberado ----------------------------------
def failure_case():
    """Oración compuesta cuya SEGUNDA cláusula ELIZA omite por completo:
    detecta ``my mother`` en la cláusula A y no examina ``my father is a lawyer``."""
    # Devuelve una tupla con la entrada experimental y la explicación del fallo.
    # La entrada y la explicación se conservan literalmente para mantener el experimento.
    return (
        "My mother is a doctor and my father is a lawyer",
        "First-match-wins: the 'my (mother|father|family)' rule fires on clause "
        "A, so clause B ('my father is a lawyer') is never inspected — fluent, "
        "on-topic, and half-blind.",
    )


# Este bloque se ejecuta al lanzar el archivo, pero no al importarlo desde el notebook.
if __name__ == "__main__":
    probe = "I am not feeling great about the exam"
    print("base    >", respond(probe))
    print("extended>", extended_respond(probe))
    text, why = failure_case()
    print(f"failure > {text!r}\n          -> {extended_respond(text)}\n          ({why})")
