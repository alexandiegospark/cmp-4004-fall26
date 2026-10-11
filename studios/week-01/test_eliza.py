"""Pruebas proporcionadas para la tarea 1 de la semana 1.

Ejecuta ``python3 test_eliza.py``. Se muestra una línea por prueba.

La mayoría comprueba TUS ampliaciones de ``starter.py`` y anunciará que aún no
están implementadas hasta que completes los TODO. La prueba
``test_base_eliza_ignores_second_clause`` comprueba el fallo de una garantía del
motor proporcionado y siempre se ejecuta. ``test_declared_failure_is_hollow``
exige reproducirlo con tu caso declarado. Observar un fallo deliberado permite
aprender a predecirlo, una habilidad central de este curso.
"""
# Estas pruebas son funciones con assert
# Los módulos eliza y starter agrupan funciones
import re
import sys
import random

import eliza
import starter as s

# Patrones del motor base: la tarea 1a no debe duplicarlos.
# Un set reúne patrones únicos y permite comprobar pertenencia con in.
# _ recibe las plantillas, que no se necesitan en esta comprensión.
BASE_PATTERNS = {p for p, _ in eliza.RULES}


def test_base_eliza_ignores_second_clause():
    """FALLO DE GARANTÍA del motor proporcionado: en la oración compuesta del
    notebook, ELIZA reacciona a 'my mother' e ignora por completo la segunda cláusula."""
    # Fija la semilla para repetir las mismas elecciones aleatorias en la prueba.
    random.seed(1)
    probe = "My mother is a doctor and my father is a lawyer"
    reply = eliza.respond(probe).lower()
    # assert lanza AssertionError si no se cumple la condición esperada.
    # Aquí se espera detectar la madre y omitir el contenido restante, un fallo conocido.
    assert "mother" in reply, f"expected ELIZA to react to clause A, got: {reply!r}"
    for dropped in ("father", "lawyer", "doctor"):
        assert dropped not in reply, (
            f"ELIZA somehow surfaced {dropped!r} — the second clause was NOT "
            f"dropped, so this is not the first-match-wins failure: {reply!r}")
    print("  ok  base ELIZA drops the second clause of a compound sentence")


def test_new_rules_count_and_shape():
    # Se llama a la función del módulo starter; el TODO puede lanzar NotImplementedError.
    rules = s.new_rules()
    # isinstance comprueba el tipo del objeto; len verifica el mínimo de reglas.
    assert isinstance(rules, list) and len(rules) >= 3, (
        f"Task 1a asks for >= 3 new rules; got {len(rules) if hasattr(rules,'__len__') else rules!r}")
    for pattern, templates in rules:
        assert isinstance(pattern, str) and pattern, "each pattern must be a non-empty regex string"
        # Construye un objeto Pattern para detectar errores de sintaxis del patrón.
        re.compile(pattern)  # debe ser una expresión regular válida
        assert isinstance(templates, list) and templates, "each rule needs >= 1 template string"
        assert all(isinstance(t, str) and t for t in templates), "templates must be non-empty strings"
        # Un patrón que acepta la cadena vacía podría eclipsar las respuestas por defecto.
        assert re.search(pattern, "") is None, (
            f"pattern {pattern!r} matches the empty string — it would fire on "
            "everything and shadow the fallback. Make it a real trigger.")
    print(f"  ok  new_rules(): {len(rules)} well-formed, non-empty-matching rules")


def test_new_rules_are_novel():
    # Compara cada patrón con el conjunto base; no modifica ninguna regla.
    for pattern, _ in s.new_rules():
        assert pattern not in BASE_PATTERNS, (
            f"pattern {pattern!r} duplicates a base rule — add something new")
    print("  ok  new_rules() does not duplicate the base engine's patterns")


def test_extended_respond_preserves_base_behavior():
    """Las reglas base conservan la prioridad: 'I feel ...' debe activar la
    regla original y sustituir los pronombres, no usar una regla nueva ni FALLBACK."""
    # Fija la semilla para repetir las mismas elecciones aleatorias en la prueba.
    random.seed(1)
    # lower() es un método del objeto str; devuelve otra cadena en minúsculas.
    reply = s.extended_respond("I feel anxious most of the time").lower()
    assert reply.startswith("do you often feel"), (
        f"extended_respond must consult the base rules first; got: {reply!r}")
    assert "anxious" in reply, f"reflection dropped the content: {reply!r}"
    print("  ok  extended_respond preserves base behavior (base rules win)")


def test_declared_failure_is_hollow():
    """FALLO DE GARANTÍA de tu código: failure_case() debe declarar una
    oración compuesta cuya segunda cláusula ELIZA omita completamente."""
    # El desempaquetado asigna los dos elementos devueltos a text y why.
    text, why = s.failure_case()
    assert isinstance(text, str) and text, "failure_case must return an input string"
    assert isinstance(why, str) and why.strip(), "failure_case must explain the failure"
    assert " and " in text.lower(), (
        "the provided test pins the compound-sentence failure: use "
        "'<clause A> and <clause B>'")
    # Fija la semilla para repetir las mismas elecciones aleatorias en la prueba.
    random.seed(1)
    reply = s.extended_respond(text).lower()
    # split es un método de str; con 1 divide solo en el primer « and ».
    _, second = text.lower().split(" and ", 1)
    # Heurística de la prueba: considera contenido las palabras de al menos 4 letras.
    # Esto verifica omisión de palabras; no demuestra comprensión del lenguaje.
    content = [w for w in re.findall(r"[a-z]+", second) if len(w) >= 4]
    assert content, "clause B has no content words to drop — pick a richer sentence"
    # Comprueba si reaparece cada palabra, también después de sustituir su pronombre.
    surfaced = [w for w in content if w in reply or REFLECT_get(w) in reply]
    assert not surfaced, (
        f"clause B words {surfaced} surfaced in the reply {reply!r} — ELIZA "
        "actually used the second clause, so this is not an ELIZA-class drop. "
        "Pick an input where the second clause is genuinely ignored.")
    print(f"  ok  declared failure drops clause B entirely ({text!r})")


def REFLECT_get(word):
    # dict.get es un método del diccionario: busca la palabra o devuelve la original.
    return eliza.REFLECT.get(word, word)


# Las funciones también son objetos: esta lista guarda referencias, sin ejecutarlas.
TESTS = [
    test_base_eliza_ignores_second_clause,
    test_new_rules_count_and_shape,
    test_new_rules_are_novel,
    test_extended_respond_preserves_base_behavior,
    test_declared_failure_is_hollow,
]


def main():
    # Recorre objetos función y los llama con t(); cuenta tareas pendientes y fallos.
    failed = 0
    for t in TESTS:
        try:
            t()
        # Excepción esperada mientras falten TODO en starter.py.
        except NotImplementedError:
            print(f"  --  {t.__name__}: starter TODO not implemented yet")
            failed += 1
        # e es el objeto excepción; su mensaje explica qué comprobación falló.
        except AssertionError as e:
            print(f"  FAIL {t.__name__}: {e}")
            failed += 1
    if failed:
        print(f"\n{failed}/{len(TESTS)} failed")
        # El código de salida 1 indica al sistema que hubo pruebas fallidas.
        sys.exit(1)
    print(f"\nall {len(TESTS)} tests pass")


if __name__ == "__main__":
    main()
