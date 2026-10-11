"""Taller de la semana 2 — Torneo y puntuación de utilidad neta (PROPORCIONADO; úsalo sin editar en el ejercicio).

La puntuación ``score`` del mundo cuenta habitaciones limpias por paso. La tarea 1
plantea otra pregunta: ¿cuál es la utilidad NETA con un modelo de costo energético?
Aquí se fijan los valores para que todos usen los mismos:

    desplazarse (Left/Right) .... cuesta # Constantes compartidas del modelo de energía; no son atributos de un agente ni del mundo.
MOVE_COST = 1
    Suck ....................... cuesta SUCK_COST = 2
    cada habitación limpia ..... aporta CLEAN_REWARD = 3 por paso
    NoOp ....................... cuesta 0

``net_utility`` calcula por su cuenta recompensas y costos; no confía en informes
del agente. Recibe una fábrica de cero argumentos que devuelve un agente nuevo
para que cada ejecución empiece con su memoria interna reiniciada.
"""
import json
from pathlib import Path

from vacuum import VacuumWorld

# Constantes compartidas del modelo de energía; no son atributos de un agente ni del mundo.
MOVE_COST = 1
SUCK_COST = 2
CLEAN_REWARD = 3


def load_configs(path=None):
    """Devuelve las 8 configuraciones iniciales como pares ``(dirt_tuple, loc)``."""
    # POO: Path es una clase; path es un objeto que representa una ruta de archivo.
    # __file__ señala este módulo; with_name() cambia el nombre manteniendo la carpeta.
    # Si no se proporciona una ruta, usa configs.json junto a tournament.py.
    path = Path(path or Path(__file__).with_name("configs.json"))
    # read_text() es un método del objeto Path que lee el archivo; json.loads convierte
    # el texto JSON en objetos Python, como diccionarios, listas y valores booleanos.
    data = json.loads(path.read_text())
    # Comprensión de lista: extrae suciedad y ubicación, convirtiendo la suciedad a tupla.
    # La tupla es inmutable; VacuumWorld hará una copia en una lista para simular cambios.
    return [(tuple(c["dirt"]), c["loc"]) for c in data["configs"]]


def net_utility(make_agent, dirt, loc, steps=20):
    """Ejecuta un agente nuevo durante `steps` pasos y devuelve la utilidad neta.

    `make_agent` es una función sin argumentos que devuelve una función
    ``agent(percept)``, como ``model_based`` o ``lambda: simple_reflex``.
    """
    # Llama a la fábrica para obtener una política; agent es una función que recibe una percepción.
    # Crear un agente por episodio evita reutilizar la memoria de configuraciones anteriores.
    agent = make_agent()
    # Instanciación: VacuumWorld.__init__ prepara un mundo con atributos propios.
    world = VacuumWorld(dirt, loc)
    net = 0
    # _ indica que no se necesita el número del paso, solo repetir la evaluación steps veces.
    for _ in range(steps):
        # world.percept() invoca un método de la instancia; agent(...) llama a la política.
        action = agent(world.percept())
        # Primero descuenta energía según la acción. NoOp no tiene costo de energía.
        if action == "Suck":
            net -= SUCK_COST
        elif action in ("Left", "Right"):
            net -= MOVE_COST
        # step() modifica el mundo; la recompensa se calcula sobre el estado después de actuar.
        world.step(action)
        # not d vale True para cada habitación limpia; sum las cuenta y multiplica por la recompensa.
        # Las habitaciones ya limpias siguen aportando en cada paso, incluso durante NoOp.
        # net es distinto de world.score: incluye energía y el factor CLEAN_REWARD.
        net += CLEAN_REWARD * sum(not d for d in world.dirt)
    return net


def tournament(factories, steps=20, configs=None):
    """Evalúa cada fábrica en cada configuración, imprime una tabla y devuelve los totales.

    `factories` es un diccionario ``{name: make_agent}``; el resultado es ``{name: total_net}``.
    """
    # Si configs no se proporciona o es una lista vacía, carga las configuraciones del archivo.
    configs = configs or load_configs()
    # Iterar un diccionario entrega sus claves; guarda los nombres para mantener el orden de columnas.
    names = list(factories)
    # Las f-strings dan formato: <22 alinea a la izquierda; >14 alinea a la derecha.
    header = f"{'start':<22}" + "".join(f"{n:>14}" for n in names)
    print(header)
    print("-" * len(header))
    # Comprensión de diccionario: cada nombre comienza con un total independiente de cero.
    totals = {n: 0 for n in names}
    for dirt, loc in configs:
        row = f"dirt={dirt} loc={loc}"
        line = f"{row:<22}"
        for n in names:
            # Recupera la fábrica por nombre y evalúa un agente nuevo en esta configuración.
            u = net_utility(factories[n], dirt, loc, steps)
            totals[n] += u
            line += f"{u:>14}"
        print(line)
    print("-" * len(header))
    print(f"{'TOTAL':<22}" + "".join(f"{totals[n]:>14}" for n in names))
    # Además de imprimir, devuelve los números para analizarlos o compararlos desde otro programa.
    return totals
