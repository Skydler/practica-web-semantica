from models import model
from durations import Duration
from parsers.parser import Parser


class MetacriticParser(Parser):
    @property
    def BASE_URL(self):
        return "https://www.metacritic.com/"

    def name(self):
        return self.movie.get("name")

    def description(self):
        return self.movie.get("description")

    def content_rating(self):
        return self.movie.get("contentRating")

    def source_urls(self):
        return [self.movie.get("url")]

    def production_company(self):
        publisher = self.movie.get("publisher")
        if len(publisher) > 1:
            raise Exception("There is more than one company")
        return self.organization(publisher[0])

    def aggregated_ratings(self):
        rating = self.movie.get("aggregateRating")

        return [
            model.AggregateRating(
                schema_type=rating.get("@type"),
                best_rating=float(rating.get("bestRating")),
                worst_rating=float(rating.get("worstRating")),
                rating_value=float(rating.get("ratingValue")),
                rating_count=int(rating.get("ratingCount")),
                source=self.movie.get("url"),
                name=None,
                description=None,
                review_count=None
            )
        ]

    def reviews(self):
        return []

    def images(self):
        return [self.movie.get("image")]

    def actors(self):
        actors = self.movie.get("actor")
        return [self.person(actor) for actor in actors]

    def characters(self):
        return []

    def directors(self):
        directors = self.movie.get("director")
        return [self.person(director) for director in directors]

    def authors(self):
        return []

    def genres(self):
        return self.movie.get("genre")

    def keywords(self):
        return []

    def duration(self):
        if duration := self.movie.get('duration'):
            duration = duration[2:].lower()
            return Duration(duration).to_minutes()

    def video(self):
        trailer = self.movie.get("trailer")
        video = model.Video(
            schema_type=trailer.get("@type"),
            name=trailer.get("name"),
            description=trailer.get("description"),
            thumbnail_url=trailer.get("thumbnailUrl"),
            url=None
        )
        return video

    def origin(self):
        return None

    def events(self):
        return []
