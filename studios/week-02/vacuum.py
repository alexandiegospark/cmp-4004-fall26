"""Taller de la semana 2 — Mundo compartido de la aspiradora (PROPORCIONADO; no modificar en el ejercicio).

Contiene el entorno y los tres agentes del notebook de la sesión A. La semana 2
trata de arquitecturas de agentes, no de volver a implementar el mundo:
se proporcionan el entorno y los agentes que ya viste construir en vivo.
Los agentes que faltan, basados en objetivos y utilidad, se escriben en ``starter.py``.

El mundo tiene dos habitaciones. Una percepción es ``(location, is_dirty_here)``.
El agente no ve si la OTRA habitación está sucia.

Interfaz compartida por las políticas:
    world.percept()      -> (location, is_dirty_here)
    world.step(action)   -> aplica 'Suck' | 'Left' | 'Right' | 'NoOp'
    agent(percept)        -> una palabra de acción
    run(agent, steps, dirt, loc) -> el mundo después de `steps` acciones
"""


# POO: una clase define los datos y las operaciones de sus objetos.
# VacuumWorld es el modelo del entorno; cada instancia representa una simulación independiente.
class VacuumWorld:
    """Dos habitaciones. Percepción = (ubicación, estado de suciedad local)."""

    # __init__ inicializa una instancia al escribir VacuumWorld(dirt, loc).
    # self es esa instancia y Python lo pasa automáticamente a sus métodos.
    # True significa habitación sucia; loc es el índice de la habitación actual (0 o 1).
    def __init__(self, dirt=(True, True), loc=0):
        # Los atributos guardan estado propio del objeto: suciedad, posición, puntuación y tiempo.
        # list(dirt) crea una copia mutable; limpiar este mundo no modifica la secuencia de entrada.
        # Estos atributos son públicos: el código evaluador puede consultarlos mediante world.dirt, etc.
        self.dirt, self.loc, self.score, self.t = list(dirt), loc, 0, 0

    # Método de observación: devuelve una tupla sin modificar el mundo.
    # world.percept() llama este método con world como self; solo revela la habitación actual.
    def percept(self):
        return (self.loc, self.dirt[self.loc])

    # Método que modifica el estado: ejecuta una acción y avanza un paso de la simulación.
    # Las palabras Suck, Left, Right y NoOp forman la interfaz y se conservan en inglés.
    def step(self, action):
        if action == "Suck":
            self.dirt[self.loc] = False
        elif action == "Left":
            self.loc = 0
        elif action == "Right":
            self.loc = 1
        # NoOp no entra en ninguna rama: no limpia ni mueve, pero el tiempo y la puntuación avanzan.
        # No hay una validación explícita: otras cadenas tampoco entrarían en esas ramas.
        # medida de rendimiento: habitaciones limpias, sumadas a lo largo del tiempo
        # not d es True para una habitación limpia; sum cuenta esos valores como 1.
        # Esta puntuación cuenta habitaciones limpias por paso, sin restar energía.
        self.score += sum(not d for d in self.dirt)
        self.t += 1

    # Método especial: Python lo usa para representar el objeto, por ejemplo al imprimirlo.
    # Produce texto descriptivo; no modifica la simulación. D indica suciedad y . indica limpieza.
    def __repr__(self):
        rooms = "".join("D" if d else "." for d in self.dirt)
        return f"[{rooms}] agent@{self.loc} t={self.t} score={self.score}"


# Herencia: BrokenSensorWorld es una subclase de VacuumWorld y reutiliza su implementación.
# Hereda __init__, step y __repr__; solo redefine (sobrescribe) percept.
# Por eso conserva el estado real, pero entrega al agente una observación incompleta.
class BrokenSensorWorld(VacuumWorld):
    """El sensor de ubicación está averiado y devuelve None. Todo lo demás
    es idéntico: observabilidad parcial mediante cuatro líneas de cambio."""

    # Método de observación: devuelve una tupla sin modificar el mundo.
    # world.percept() llama este método con world como self; solo revela la habitación actual.
    def percept(self):
        # self.loc sigue siendo la ubicación real; únicamente se oculta en el resultado del sensor.
        return (None, self.dirt[self.loc])   # ubicación desconocida


# ---- Agentes proporcionados (construidos en vivo en la sesión A) -------------

# Este agente es una función, no una clase: recibe datos y devuelve una acción.
# Sin estado persistente, no recuerda habitaciones visitadas ni reconoce el final de la tarea.
def simple_reflex(percept):
    """Transforma directamente la percepción actual en una acción. No tiene memoria."""
    # Desempaqueta la tupla: loc es la posición observada y dirty indica suciedad local.
    loc, dirty = percept
    if dirty:
        return "Suck"
    # Con loc=None, la condición es falsa y elige Left: no puede reconstruir la ubicación.
    return "Right" if loc == 0 else "Left"


# Una fábrica es una función que crea y devuelve un agente nuevo.
# Aquí se usa una clausura: la función interna conserva acceso a state tras terminar model_based().
# Es memoria persistente mediante funciones; no se crea una instancia de una clase de agente.
def model_based():
    """Añade estado interno para recordar qué se limpió y dónde está el agente.
    Así puede saber cuándo ha terminado (NoOp) y funcionar con el sensor de
    ubicación averiado: nunca lee `loc` de la percepción. Su posición inicial
    supuesta debe coincidir con la real para que esa memoria sea fiable."""
    # Cada llamada a la fábrica crea un diccionario nuevo, separado del de otros agentes.
    # clean indica qué habitaciones cree haber limpiado; False aquí significa que aún no lo sabe.
    # loc=0 es una creencia inicial fija, no una lectura del sensor.
    state = {"loc": 0, "clean": [False, False]}

    def agent(percept):
        # _ descarta deliberadamente la ubicación observada; se usa la posición recordada.
        _, dirty = percept
        if dirty:
            state["clean"][state["loc"]] = True
            return "Suck"
        state["clean"][state["loc"]] = True
        # all devuelve True cuando ambos registros son True: el agente considera terminada la tarea.
        if all(state["clean"]):
            return "NoOp"                  # sabe que terminó; el reactivo nunca lo reconoce
        # En dos habitaciones, 1 - loc alterna entre 0 y 1; actualiza la posición prevista.
        state["loc"] = 1 - state["loc"]
        return "Right" if state["loc"] == 1 else "Left"

    # Devuelve el objeto función, sin ejecutarlo: quien lo recibe llamará agent(percept).
    return agent


# Otra fábrica con una clausura independiente. Conserva el criterio simplificado del notebook:
# solo se desplaza hacia una habitación no registrada como limpia si move_cost < 1.0.
def utility_agent(move_cost=1.0):
    """Agente simplificado de utilidad del notebook. Con ``move_cost=1.0``
    deja RACIONALMENTE la otra habitación sucia: sigue una especificación que
    produce un resultado no deseado. Se conserva como referencia; el taller
    pide construir ``utility_based`` con parámetros de costo explícitos."""
    # Cada llamada a la fábrica crea un diccionario nuevo, separado del de otros agentes.
    # clean indica qué habitaciones cree haber limpiado; False aquí significa que aún no lo sabe.
    # loc=0 es una creencia inicial fija, no una lectura del sensor.
    state = {"loc": 0, "clean": [False, False]}

    def agent(percept):
        # _ descarta deliberadamente la ubicación observada; se usa la posición recordada.
        _, dirty = percept
        if dirty:
            state["clean"][state["loc"]] = True
            return "Suck"
        state["clean"][state["loc"]] = True
        # Calcula el índice de la otra habitación según la posición que el agente recuerda.
        other = 1 - state["loc"]
        if not state["clean"][other] and move_cost < 1.0:
            state["loc"] = other
            return "Right" if other == 1 else "Left"
        return "NoOp"          # desplazarse no compensa

    # Devuelve el objeto función, sin ejecutarlo: quien lo recibe llamará agent(percept).
    return agent


# ---- Código de evaluación compartido con el notebook ------------------------

def run(agent, steps=20, dirt=(True, True), loc=0, trace=0):
    """Ejecuta `agent` en un mundo nuevo durante `steps` acciones; devuelve el mundo."""
    # Instanciación: crea un objeto VacuumWorld con estado propio para esta ejecución.
    world = VacuumWorld(dirt, loc)
    for i in range(steps):
        # Ciclo percepción → decisión → acción: el agente recibe una tupla y devuelve una cadena.
        action = agent(world.percept())
        # trace limita cuántos pasos se imprimen; no cambia las acciones ejecutadas.
        if trace and i < trace:
            print(f"  {world}  ->  {action}")
        world.step(action)
    return world


# Polimorfismo: este evaluador usa la misma interfaz percept()/step() con ambas clases.
# Si world es BrokenSensorWorld, Python ejecuta su percept redefinido y el step heredado.
# El evaluador no necesita preguntar cuál de las dos clases recibió.
def run_in(world, agent, steps=20, trace=0):
    """Como `run`, pero usa un mundo proporcionado, por ejemplo BrokenSensorWorld."""
    for i in range(steps):
        # Ciclo percepción → decisión → acción: el agente recibe una tupla y devuelve una cadena.
        action = agent(world.percept())
        # trace limita cuántos pasos se imprimen; no cambia las acciones ejecutadas.
        if trace and i < trace:
            print(f"  {world}  ->  {action}")
        world.step(action)
    return world
