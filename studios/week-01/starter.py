"""Taller de la semana 1 — Plantilla de la tarea 1: amplía ELIZA y compara con el modelo local.

Completa los tres TODOs y ejecuta ``python3 test_eliza.py``. Todas las pruebas deben
pasar, INCLUIDA ``test_declared_failure_is_hollow``, que observa cómo falla una
garantía: ELIZA omite la segunda parte de una oración compuesta porque la primera
coincidencia gana y no tiene un modelo del resto de la entrada. Una prueba que
exige este fallo específico es deliberada: *predecir el fallo* es el objetivo de la semana 1.

Al final aparece el esquema de la tarea 2 (primer contacto). Ejecútalo en tu propio
script y escribe ``first_contact.md``. Los prompts están en ``prompts.json``.
"""
# Se organiza mediante funciones y datos compartidos; no hay clases propias.
# Importar RULES y reflect reutiliza otro módulo
import re

from eliza import RULES, FALLBACK, REFLECT, reflect, respond


# ---- Tarea 1a: añade TRES reglas nuevas -------------------------------------
def new_rules():
    """Devuelve una lista con al menos 3 reglas NUEVAS ``(pattern, [templates])``.

    Usa la estructura de ``eliza.RULES``: una cadena de expresión regular y una
    lista de plantillas cuyos campos ``{0}``, ``{1}``, etc. se completan con los
    grupos capturados después de sustituir los pronombres (véase ``eliza.respond``).

    Las reglas deben:
    - ser al menos 3;
    - no duplicar ningún patrón de ``eliza.RULES``;
    - activarse ante alguna entrada real y nunca ante la cadena vacía, porque
      eso impediría usar las respuestas por defecto.

    Ejemplo (elimínalo y escribe el tuyo):
        (r"\bI want (.*)", ["What would it mean to you to get {0}?"])
    """
    # list almacena varias reglas; cada tuple agrupa un patrón y sus plantillas.
    # TODO: devuelve una lista con al menos 3 tuplas (pattern, [templates]).
    raise NotImplementedError


# ---- Tarea 1b: función de respuesta ampliada --------------------------------
def extended_respond(text):
    """Responde con ``eliza.RULES`` PRIMERO, después ``new_rules()`` y luego FALLBACK.

    Las reglas base conservan la prioridad para que las nuevas no alteren la
    demostración. Reutiliza ``eliza.reflect`` para sustituir los pronombres.
    La implementación más breve es el bucle de ``eliza.respond`` aplicado a
    ``RULES + new_rules()``.
    """
    # El orden de la lista determina qué regla gana; return detiene el recorrido.
    # Un objeto Match ofrece groups(); las cadenas ofrecen format(*groups).
    # TODO: recorre RULES + new_rules(); en la primera coincidencia, sustituye
    #       los pronombres de los grupos y completa una plantilla aleatoria; si no, usa FALLBACK.
    raise NotImplementedError


# ---- Tarea 1c: declara tu fallo deliberado ----------------------------------
def failure_case():
    """Devuelve ``(input_text, why_it_fails)``.

    Elige una entrada para la que tu ELIZA ampliada responda con fluidez, pero
    sin comprensión: una respuesta pertinente y vacía, característica de ELIZA.
    La prueba exige una oración COMPUESTA ``"<cláusula A> and <cláusula B>"``:
    ELIZA reacciona a la cláusula A y omite por completo la B porque gana la primera
    coincidencia. El ejemplo del notebook es
    "My mother is a doctor and my father is a lawyer".

    El segundo elemento explica el fallo en una oración. Pégalo en la cadena de
    documentación de ``eliza.py`` para el commit solicitado por el plan:
    ``week01/eliza.py``, con el fallo documentado.
    """
    # Son dos valores en una tupla: dato de prueba y explicación legible del fallo.
    # TODO: devuelve (input_text, why_it_fails)
    raise NotImplementedError


# ---- Esquema de la tarea 2: primer contacto (véase README, «Tarea 2») ---------
# Envía los MISMOS prompts a ELIZA y al modelo local; registra AMBAS transcripciones
# en first_contact.md y responde las tres preguntas del README.
#
#     import json
#     from aicourse.llm import LLM
#     from starter import extended_respond
#
#     prompts = json.load(open("prompts.json"))["first_contact"]
#     # POO: LLM es una clase; llm es una instancia configurada con un backend.
#     # llm.complete(p) invoca su método; .text accede al atributo del resultado.
#     llm = LLM(backend="ollama")          # o ejecuta con --backend manual
#     for p in prompts:
#         print("you  >", p)
#         print("ELIZA>", extended_respond(p))
#         print("LLM  >", llm.complete(p).text, "\n")
#
# NO pidas al modelo que se evalúe a sí mismo («¿parece correcta esa respuesta?»). Tú eres
# quien verifica. Esa mala práctica corresponde al eje 3 de la ficha de evaluación.


# Al importar starter no se ejecuta esta demostración.
if __name__ == "__main__":
    # Prueba básica: ejecuta lo que hayas completado con una entrada.
    probe = "I am not feeling great about the exam"
    print("base   >", respond(probe))
    try:
        print("extended>", extended_respond(probe))
    except NotImplementedError:
        print("extended> not implemented yet")
    try:
        text, why = failure_case()
        print(f"failure > {text!r}\n          -> {extended_respond(text)}\n          ({why})")
    except NotImplementedError:
        print("failure > not declared yet")
