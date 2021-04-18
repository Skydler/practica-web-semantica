from model import model
from durations import Duration
import json

DATA_PATH = "../data/metacritic.json"


class MetacriticParser:

    def __init__(self):
        self.data = self.read_data()

    @staticmethod
    def read_data():
        with open(f"{DATA_PATH}", "r") as file:
            data = json.load(file)
        return data

    def build_movie(self):
        schema_type = self.data.get("@type")
        name = self.data.get("name")
        description = self.data.get("description")
        content_rating = self.data.get("contentRating")
        source_urls = [self.data.get("url")]
        production_company = self.build_org(self.data.get("publisher"))
        aggregated_ratings = [self.build_aggregate_rating(
            self.data.get("aggregateRating"), name)]
        reviews = []
        images = [self.data.get("image")]
        actors = [self.build_person(actor) for actor in self.data.get("actor")]
        characters = []
        directors = [self.build_person(director)
                     for director in self.data.get("director")]
        authors = []
        genres = self.data.get("genre")
        keywords = []
        duration = self.parse_duration(self.data.get("duration"))
        video = self.build_video(self.data.get("trailer"))
        origin = None
        events = []

        movie = model.Movie(
            schema_type=schema_type,
            name=name,
            description=description,
            content_rating=content_rating,
            source_urls=source_urls,
            production_company=production_company,
            aggregated_ratings=aggregated_ratings,
            reviews=reviews,
            images=images,
            actors=actors,
            characters=characters,
            directors=directors,
            authors=authors,
            genres=genres,
            keywords=keywords,
            duration=duration,
            video=video,
            origin=origin,
            events=events
        )

        return movie

    def build_org(self, publisher):
        if len(publisher) != 1:
            raise Exception("There is more than one company")
        company = publisher[0]
        organization = model.Organization(
            schema_type=company.get("@type"),
            name=company.get("name"),
            url=company.get("url")
        )
        return organization

    def build_aggregate_rating(self, agg_rating, src):
        aggregate_rating = model.AggregateRating(
            schema_type=agg_rating.get("@type"),
            best_rating=float(agg_rating.get("bestRating")),
            worst_rating=float(agg_rating.get("worstRating")),
            rating_value=float(agg_rating.get("ratingValue")),
            rating_count=int(agg_rating.get("ratingCount")),
            source=src,
            name=None,
            description=None,
            review_count=None
        )
        return aggregate_rating

    def build_person(self, person):
        person = model.Person(
            schema_type=person.get("@type"),
            name=person.get("name"),
            url=person.get("url"),
            image=None
        )
        return person

    def parse_duration(self, duration):
        time = duration[2:]
        time = time.lower()
        minutes = int(Duration(time).to_minutes())
        return minutes

    def build_video(self, trailer):
        video = model.Video(
            schema_type=trailer.get("@type"),
            name=trailer.get("name"),
            description=trailer.get("description"),
            thumbnail_url=trailer.get("thumbnailUrl"),
            url=None
        )

        return video
