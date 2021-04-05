from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, config
from datetime import datetime
from marshmallow import fields
from typing import List, Optional


@dataclass_json
@dataclass
class Show:
    cine: str   # TODO: Should be changed to theater or something like that
    room: str
    language: str
    time: datetime = field(
        metadata=config(
            encoder=datetime.isoformat,
            decoder=datetime.fromisoformat,
            mm_field=fields.DateTime(format='iso')
        )
    )


@dataclass_json
@dataclass
class Movie:
    title: str
    genres: List[str]
    languages: List[str]
    origins: List[str]
    duration: Optional[int]
    directors: List[str]
    rated: Optional[str]
    actors: List[str]
    synopsis: str
    trailer: Optional[str]
    shows: List[Show]
    distributor: Optional[str]
    released: bool
