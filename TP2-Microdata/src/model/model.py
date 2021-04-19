from datetime import datetime

from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from typing import Optional, Union, List


@dataclass_json
@dataclass
class Schema:
    schema_type: str


@dataclass_json
@dataclass(unsafe_hash=True)
class Organization(Schema):
    name: Optional[str]
    url: Optional[str]

    def __eq__(self, other):
        if not isinstance(other, Organization) or other.name is None:
            return False

        return self.name == other.name


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
@dataclass(unsafe_hash=True)
class Person(Schema):
    name: str
    url: Optional[str] = field(compare=False)
    image: Optional[str] = field(compare=False)


@dataclass_json
@dataclass
class Review(Schema):
    review_body: str
    url: Optional[str]
    date_created: datetime
    language: Optional[str]
    name: Optional[str]
    author: Person
    review_rating: Optional[Rating]
    publisher: Optional[Organization]
    source: str


@dataclass_json
@dataclass
class Video(Schema):
    name: Optional[str]
    url: Optional[str]
    description: Optional[str]
    thumbnail_url: Optional[str]


@dataclass_json
@dataclass
class PublicationEvent(Schema):
    start_date: datetime
    location: str


@dataclass_json
@dataclass
class Movie(Schema):
    name: str
    description: Optional[str]
    content_rating: str
    source_urls: List[str]              # main entity in ecartelera
    production_company: Optional[Organization]    # publisher in metacritic
    aggregated_ratings: List[AggregateRating]
    reviews: List[Review]
    images: List[str]
    actors: List[Person]
    characters: List[str]
    directors: List[Person]
    authors: List[Union[Person, Organization]]
    genres: List[str]
    keywords: List[str]
    duration: int                       # In minutes
    video: Optional[Video]
    origin: Optional[str]
    events: List[PublicationEvent]
    schema_context: str = "http://schema.org"
