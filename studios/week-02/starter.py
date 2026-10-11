"""Taller de la semana 2 — Plantilla de la tarea 1: completa la clasificación de agentes.

Implementa los dos agentes y ejecuta ``python3 test_agents.py``. Todas las pruebas
requeridas deben pasar, INCLUIDAS las que comprueban una propiedad sorprendente:

  - el agente reactivo simple falla de manera DEMOSTRABLE en un mundo que maneja
    el basado en modelos, con observabilidad parcial: observa el fallo de una garantía;
  - el agente de utilidad deja RACIONALMENTE una habitación sucia en al menos
    una configuración: sigue la especificación bajo un modelo de costo.

El entorno y los agentes simple_reflex y model_based se proporcionan en
``vacuum.py``. Aquí escribes ``goal_based`` y ``utility_based``.
"""
# Los agentes se implementan con funciones. El entorno VacuumWorld sí usa una clase.
# Una fábrica devolverá una función interna con acceso a su memoria (clausura).
from vacuum import VacuumWorld, run, simple_reflex, model_based


# ---- Tarea 1: completa la clasificación de agentes --------------------------

def goal_based(goal=(False, False)):
    """Devuelve un agente que PLANIFICA hacia un objetivo explícito y después SE DETIENE.

    El objetivo es un estado de suciedad: ``(False, False)`` significa ambas
    habitaciones limpias. A diferencia del reactivo, que oscila sin fin, debe
    reconocer que alcanzó el objetivo y devolver ``"NoOp"`` desde entonces.

    Estado interno sugerido, como en model_based: recordar qué habitaciones
    limpió y dónde está, pues la percepción solo muestra la habitación actual.

    Devuelve una función ``agent(percept) -> action``.
    """
    # TODO significa tarea pendiente; el comentario no se ejecuta ni modifica el comportamiento.
    # Una lista o diccionario creado aquí puede guardar memoria para la función interna.
    # Cada llamada a la fábrica debe crear memoria nueva para evitar mezclar episodios.
    # TODO: construye un agente con estado interno que:
    #   - lea `loc` de la percepción: aquí el sensor FUNCIONA, a diferencia de
    #     model_based, que supone loc=0 y solo funciona con el sensor averiado
    #     cuando esa creencia resulta correcta;
    #   - devuelva Suck si la habitación está sucia y la registre como limpia;
    #   - se desplace hacia una habitación aún no limpiada en caso contrario;
    #   - devuelva "NoOp" cuando su registro cumpla `goal`: ambas habitaciones limpias.
    # Esta instrucción sí se ejecuta: marca el ejercicio pendiente. Sustitúyela al implementar el agente.
    raise NotImplementedError


def utility_based(move_cost=1, suck_cost=2, clean_reward=3):
    """Devuelve un agente que maximiza la utilidad NETA paso a paso.

    Modelo de costo, con los valores de ``tournament.py``: moverse cuesta
    ``move_cost``, cada Suck cuesta ``suck_cost`` y cada habitación limpia
    aporta ``clean_reward`` por paso. Solo ve ``percept``: no anticipa pasos
    futuros y debe razonar de forma voraz sobre el cambio neto inmediato.

    El descubrimiento esperado: A VECES DEJA UNA HABITACIÓN SUCIA porque pagar
    por viajar hacia un beneficio que no ve no compensa de inmediato. Repórtalo
    como resultado, no como error: es la primera vez que un agente toma una
    decisión que no deseabas, pero que sigue el criterio que le diste.

    Devuelve una función ``agent(percept) -> action``.
    """
    # TODO significa tarea pendiente; el comentario no se ejecuta ni modifica el comportamiento.
    # Una lista o diccionario creado aquí puede guardar memoria para la función interna.
    # Cada llamada a la fábrica debe crear memoria nueva para evitar mezclar episodios.
    # TODO: construye un agente con estado interno que:
    #   - lea `loc` de la percepción: aquí el sensor funciona;
    #   - limpie con Suck la habitación actual si está sucia: recupera pronto suck_cost;
    #   - en caso contrario, compare el costo inmediato de desplazarse con la recompensa
    #     inmediata, y devuelva "NoOp" cuando desplazarse no compense.
    # Esta instrucción sí se ejecuta: marca el ejercicio pendiente. Sustitúyela al implementar el agente.
    raise NotImplementedError


# ---- Esquema de la tarea 2: el LLM como función del agente -------------------
# Consulta README.md, sección «Tarea 2». Conecta el modelo a la MISMA interfaz percept->action.
# Tú proporcionas la llamada; debes manejar las salidas mal formadas y REGISTRAR
# cada fallo de análisis: corresponde al eje 8 de la ficha de evaluación.
#
from aicourse.llm import LLM
# POO: LLM es una clase; model es una instancia creada mediante su inicializador.
# Este objeto reúne la configuración y los métodos de acceso al modelo de lenguaje.
# La creación está a nivel de módulo: también ocurre al importar starter, no solo al ejecutarlo.
model = LLM()  # el backend local que hayas configurado
#
# El prompt se conserva en inglés: las palabras de acción y sus campos forman la interfaz experimental.
# {history}, {loc} y {status} son campos que se completan con str.format, sin cambiar sus nombres.
PROMPT = """You control a vacuum robot in a 2-room world.
Rooms 0 and 1. Each is Clean or Dirty.
Actions: Left, Right, Suck, NoOp.
History of (percept, action) so far:
{history}
Current percept: location={loc}, status={status}
Reply with exactly one action word and nothing else."""

# Convierte la respuesta libre del modelo en una de las cuatro cadenas válidas para el entorno.
# No es un método de clase: es una función auxiliar que devuelve una acción o None.
def parse_action(raw):
    actions = ["Left", "Right", "Suck", "NoOp"]

    # strip() es un método de str: devuelve otra cadena sin espacios exteriores.
    text = raw.strip()

    # El orden importa: devuelve la primera acción cuya palabra aparezca como subcadena.
    # lower() compara sin distinguir mayúsculas. También acepta «Suck.» o «I would suck».
    # Si la respuesta menciona varias acciones o una negación, este analizador no interpreta su sentido.
    for action in actions:
        if action.lower() in text.lower():
            return action

    # Conserva la respuesta original en la salida para poder documentar el fallo de análisis.
    print("PARSE FAILURE:", raw)
    return None


# history es una lista de pares (percepción, acción); convierte cada par en una línea de texto.
def fmt(history):
    # join() es un método de str; une las líneas generadas con saltos de línea.
    return "\n".join(
        f"{percept} -> {action}"
        for percept, action in history
    )


# Fábrica de una política con clausura: la función interna recuerda la lista history recibida.
# La lista no se copia: el llamador y este agente comparten el mismo objeto mutable.
# Usa una lista distinta para cada episodio si quieres separar sus historiales.
def llm_agent(history):
    # Cada llamada decide una acción a partir de la percepción actual y del historial acumulado.
    def agent(percept):
        # Desempaqueta la tupla; dirty=True se comunica al modelo como Dirty.
        loc, dirty = percept

        # Invoca complete(), método de la instancia model, con el prompt ya rellenado.
        # PROMPT.format() es otro método, esta vez del objeto cadena que contiene la plantilla.
        resp = model.complete(
            PROMPT.format(
                history=fmt(history),
                loc=loc,
                status="Dirty" if dirty else "Clean"
            )
        )

        # resp es el objeto resultado; .text accede al atributo que guarda su respuesta textual.
        action = parse_action(resp.text)

        # Si no se pudo analizar, adopta NoOp como acción por defecto. Aquí no hay reintento.
        if action is None:
            action = "NoOp"

        # append() es un método de list: modifica el historial compartido añadiendo este paso.
        history.append((percept, action))

        return action

    # Devuelve el objeto función; no hace una llamada al LLM hasta recibir una percepción.
    return agent



# Ejecuta las mismas 8 configuraciones; repite UNA 5 veces y cuenta las secuencias distintas.
# Es una comprobación directa de reproducibilidad, eje 5. Compara con los cuatro agentes clásicos.


# Este bloque de demostración se ejecuta al lanzar el archivo, no al importarlo.
if __name__ == "__main__":
    # Prueba básica: ejecuta cada agente que hayas completado sobre una configuración.
    from tournament import tournament, net_utility

    # Guarda fábricas de cero argumentos. lambda devuelve el reactivo, que no necesita memoria nueva.
    factories = {
        "reflex": lambda: simple_reflex,
        "model": model_based,
    }
    for name, make in [("goal", goal_based), ("utility", utility_based)]:
        try:
            make()  # lanza NotImplementedError hasta que lo completes
            factories[name] = make
        # Captura el ejercicio aún pendiente y continúa la demostración con lo disponible.
        except NotImplementedError:
            print(f"  {name:<10} not implemented yet")

    if len(factories) > 2:
        print()
        tournament(factories)
