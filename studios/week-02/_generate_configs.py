"""Generador de configuraciones iniciales del taller de la semana 2.

Ejecútalo una vez al preparar el material y guarda ``configs.json`` junto a él
en el repositorio. A diferencia del banco de cuadrículas de la semana 4, este
no usa azar: el mundo de dos habitaciones tiene 8 configuraciones iniciales,
2² estados de suciedad × 2 ubicaciones del agente. Se enumeran todas de manera
determinista, sin semilla: siempre produce las mismas 8 filas en el mismo orden.
"""
import itertools
import json
from pathlib import Path


# El módulo se organiza mediante una función; no define clases propias.
# Sí utiliza objetos de la clase Path para manipular la ruta del archivo de salida.
def main():
    # Comprensión de lista: construye un diccionario por cada combinación posible.
    # Cada fila guarda dirt como lista de booleanos y loc como índice 0 o 1.
    configs = [
        {"dirt": list(dirt), "loc": loc}
        # El producto exterior combina cada estado de suciedad con las dos ubicaciones.
        # El producto interior con repeat=2 produce (True, True), (True, False),
        # (False, True) y (False, False): 4 × 2 = 8 configuraciones, sin aleatoriedad.
        for dirt, loc in itertools.product(
            itertools.product([True, False], repeat=2),   # ¿están sucias las habitaciones 0 y 1?
            [0, 1],                                        # ubicación del agente
        )
    ]
    # Agrupa la descripción, el número de configuraciones y los datos que leerá tournament.py.
    # Las claves y los valores de salida se mantienen para conservar el archivo generado.
    out = {"note": "all 8 start configurations of the 2-room world (enumerated)",
           "n": len(configs), "configs": configs}
    # POO: Path(__file__) crea una instancia; with_name() devuelve otra ruta en la misma carpeta.
    # Así el destino depende de la ubicación del script, no del directorio desde el que se lanzó.
    dest = Path(__file__).with_name("configs.json")
    # json.dumps serializa los objetos a texto JSON; indent=2 facilita la lectura.
    # write_text() es un método del objeto Path que escribe y reemplaza el archivo de destino.
    dest.write_text(json.dumps(out, indent=2))
    print(f"wrote {dest} — {len(configs)} configurations")


# Solo genera el archivo al ejecutar este script directamente; importarlo no llama a main().
if __name__ == "__main__":
    main()
