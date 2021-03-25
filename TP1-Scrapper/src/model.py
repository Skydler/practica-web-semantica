from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import List


@dataclass_json
@dataclass
class Funcion:
    cine: str
    sala: str
    idioma: str
    horarios: List[str]


@dataclass_json
@dataclass
class Pelicula:
    cine_fuente: str
    titulo: str
    genero: List[str]
    idioma: List[str]
    origen: List[str]
    duracion: int
    director: str
    calificacion: str
    actores: List[str]
    sinopsis: str
    trailer: str
    funciones: List[Funcion]
    distribuidora: str
