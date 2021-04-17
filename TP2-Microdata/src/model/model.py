from datetime import datetime

from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, config
from typing import Optional, Union, List
from marshmallow import fields


SCHEMA = "http://schema.org"

iso_datetime = field(
    metadata=config(
        encoder=datetime.isoformat,
        decoder=datetime.fromisoformat,
        mm_field=fields.DateTime(format='iso')
    )
)


class Schema:
    schema_type: str


@dataclass_json
@dataclass
class Organization(Schema):
    name: str
    url: Optional[str]


@dataclass_json
@dataclass
class Rating(Schema):
    name: Optional[str]
    description: Optional[str]
    rating_value: float
    best_rating: float
    worst_rating: float


@dataclass_json
@dataclass
class AggregateRating(Rating):
    rating_count: int
    review_count: Optional[int]
    source: str


@dataclass_json
@dataclass
class Person(Schema):
    name: str
    url: Optional[str]
    image: Optional[str]


@dataclass_json
@dataclass
class Review(Schema):
    review_body: str
    url: str
    date_created: iso_datetime
    language: Optional[str]
    name: Optional[str]
    author: Person
    review_rating: Rating
    publisher: Organization
    source: str


@dataclass_json
@dataclass
class Video(Schema):
    name: str
    url: Optional[str]
    description: str
    thumbnail_url: str


@dataclass_json
@dataclass
class PublicationEvent(Schema):
    start_date: iso_datetime
    location: str


@dataclass_json
@dataclass
class Movie(Schema):
    name: str
    description: Optional[str]
    content_rating: str
    source_urls: List[str]  # main entity in ecartelera
    production_company: Organization  # publisher in metacritic
    aggregated_ratings: List[AggregateRating]
    reviews: List[Review]
    images: List[str]
    actors: List[Person]
    characters: List[str]
    directors: List[Person]
    authors: List[Union[Person, Organization]]
    genres: List[str]
    keywords: List[str]
    duration: int  # In minutes
    video: Optional[Video]
    origin: Optional[str]
    events: List[PublicationEvent]
    schema_context: str = "http://schema.org"
