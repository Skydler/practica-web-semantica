from dataclasses import dataclass
from dataclasses_json import dataclasses_json
from typing import list


@dataclasses_json
@dataclass
class Funcion:
    cine: str
    sala: str
    idioma: str
    horarios: list[str]


@dataclasses_json
@dataclass
class Pelicula:
    cine_fuente: str
    titulo: str
    genero: list[str]
    origen: list[str]
    duracion: int
    director: str
    calificacion: str
    actores: list[str]
    sinopsis: str
    trailer: str
    funciones: list[Funcion]
    distribuidora: str
