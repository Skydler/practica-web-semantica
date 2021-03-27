from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import List


@dataclass_json
@dataclass
class Show:
    cine: str
    room: str
    language: str
    hours: List[str]


@dataclass_json
@dataclass
class Movie:
    source: str
    title: str
    genres: List[str]
    languages: List[str]
    origins: List[str]
    duration: int
    director: str
    rated: str
    actors: List[str]
    synopsis: str
    trailer: str
    shows: List[Show]
    distributor: str
    released: bool
