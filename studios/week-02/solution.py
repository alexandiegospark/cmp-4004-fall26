"""Taller de la semana 2 — SOLUCIÓN DE REFERENCIA (solo para el docente).

Versión completada de ``starter.py``: conserva los nombres y firmas de las
funciones para que ``test_agents.py`` pase al importar este módulo como ``starter``.
El material describe ``studios/_verify_solutions.py`` como verificador: registra
este archivo con el nombre ``starter`` y ejecuta las pruebas sin modificarlas.

NO distribuir a estudiantes: se excluye mediante ``studios/.gitignore``.
La explicación didáctica está en ``solution.ipynb``, que importa este archivo
en lugar de copiarlo para mantener ambas versiones sincronizadas.
"""
# Las políticas son funciones, no clases. Cada fábrica devuelve una función con memoria propia.
# VacuumWorld sí es una clase; run y las demás políticas se importan para reutilizarlas.
from vacuum import VacuumWorld, run, simple_reflex, model_based


# ---- Tarea 1: completa la clasificación de agentes --------------------------

def goal_based(goal=(False, False)):
    """Devuelve un agente que PLANIFICA hacia un objetivo explícito y después SE DETIENE.

    El objetivo es un estado de suciedad: ``(False, False)`` significa ambas
    habitaciones limpias. A diferencia del agente reactivo, que oscila sin fin,
    este reconoce que alcanzó el objetivo y devuelve ``"NoOp"`` desde entonces.

    Mantiene un registro por habitación de lo que observó o dejó limpio.
    La percepción expone ``loc``, pues el sensor FUNCIONA en ``VacuumWorld``.
    A diferencia de ``model_based``, que ignora ``loc`` y solo funciona con el
    sensor averiado cuando su creencia inicial fija resulta correcta, este
    agente lee la ubicación real y no necesita adivinar dónde está.
    """
    # tuple convierte el objetivo en una secuencia inmutable: la política no lo modifica.
    goal = tuple(goal)
    # Memoria privada por clausura: cada llamada a la fábrica crea una lista nueva.
    # En cleaned, True significa «sabemos que está limpia», no «está sucia».
    cleaned = [False, False]          # habitaciones observadas o dejadas limpias

    # La función interna conserva acceso a las variables de su fábrica entre llamadas.
    # No es un método: no recibe self ni pertenece a una clase de agente.
    def agent(percept):
        # La percepción es una tupla; loc es el índice real y dirty describe esa habitación.
        loc, dirty = percept
        if dirty:
            cleaned[loc] = True        # quedará limpia al ejecutar este Suck
            return "Suck"
        cleaned[loc] = True            # ahora sabemos que la habitación actual está limpia
        # Una habitación cumple el objetivo si goal[i] es False (debe estar limpia) y
        # la hemos limpiado. Estas habitaciones aún necesitan trabajo:
        # Comprensión de lista: selecciona índices que deben estar limpios y aún no están registrados.
        # False en goal exige limpieza; un valor True no obliga a ensuciar una habitación.
        need = [i for i in range(2) if not goal[i] and not cleaned[i]]
        if not need:
            return "NoOp"              # objetivo alcanzado: detenerse; el reactivo no lo hace
        # Elige la primera habitación pendiente y devuelve una acción hacia ella.
        target = need[0]
        return "Right" if target == 1 else "Left"   # desplazarse hacia una habitación aún no limpiada

    # Devuelve la función, sin ejecutarla. El simulador la llamará con cada percepción.
    return agent


def utility_based(move_cost=1, suck_cost=2, clean_reward=3):
    """Devuelve un agente que maximiza la utilidad NETA paso a paso.

    Modelo de costo, con los valores de ``tournament.py``: cada desplazamiento
    cuesta ``move_cost``, cada Suck cuesta ``suck_cost`` y cada habitación
    limpia aporta ``clean_reward`` por paso. La función solo ve ``percept``:
    no anticipa pasos futuros y considera de forma voraz el cambio neto inmediato.

    El descubrimiento esperado: A VECES DEJA UNA HABITACIÓN SUCIA. Cuando la
    habitación actual está limpia, solo puede desplazarse a otra que no ve.
    Left/Right no limpia nada en el paso del desplazamiento; la cantidad de
    habitaciones limpias no cambia. El cambio neto inmediato de desplazarse es
    ``-move_cost``, una pérdida estricta con los costos dados, frente a ``0``
    para ``NoOp``. Sin horizonte futuro, no paga por viajar hacia un beneficio
    que aún no puede ver: se detiene. Repórtalo como resultado, no como error.
    """
    # Memoria privada por clausura: cada llamada a la fábrica crea una lista nueva.
    # En cleaned, True significa «sabemos que está limpia», no «está sucia».
    cleaned = [False, False]

    # La función interna conserva acceso a las variables de su fábrica entre llamadas.
    # No es un método: no recibe self ni pertenece a una clase de agente.
    def agent(percept):
        # La percepción es una tupla; loc es el índice real y dirty describe esa habitación.
        loc, dirty = percept
        if dirty:
            # Una habitación sucia recupera pronto suck_cost: clean_reward se acumula en cada
            # paso restante; con los valores del ejercicio, limpiar la habitación actual es
            # la acción inmediata racional.
            cleaned[loc] = True
            return "Suck"
        cleaned[loc] = True
        # Evalúa el cambio neto INMEDIATO de pasar a la otra habitación, que no observa.
        # Moverse cuesta move_cost ahora y no limpia nada durante este paso; la recompensa
        # por habitaciones limpias no cambia: net(cruzar) = -move_cost; net(NoOp) = 0.
        # La decisión de desplazarse solo usa move_cost. suck_cost y clean_reward
        # describen el modelo, pero esta implementación no los usa en una comparación explícita.
        # Si hay suciedad, siempre devuelve Suck; conserva esa conducta del código de referencia.
        net_of_crossing = -move_cost
        if net_of_crossing > 0:                     # nunca, con este modelo de costo
            other = 1 - loc
            return "Right" if other == 1 else "Left"
        return "NoOp"                                # desplazarse no compensa

    # Devuelve la función, sin ejecutarla. El simulador la llamará con cada percepción.
    return agent


# Ejecuta el torneo al lanzar este archivo; importar solution no ejecuta este bloque.
if __name__ == "__main__":
    from tournament import tournament, net_utility

    # El diccionario guarda fábricas, no agentes ya creados: cada episodio tendrá memoria nueva.
    # simple_reflex ya es una función de agente; lambda la devuelve con una interfaz de cero argumentos.
    factories = {
        "reflex": lambda: simple_reflex,
        "model": model_based,
        "goal": goal_based,
        "utility": utility_based,
    }
    tournament(factories)
