from datetime import datetime

from durations import Duration
from models import model
from parsers.parser import Parser


class EcarteleraParser(Parser):
    @property
    def BASE_URL(self):
        return "https://www.ecartelera.com/"

    def name(self):
        return self.movie.get("name")

    def description(self):
        description = self.movie.get("description")
        description = description.replace("&#39;", "'")
        return description

    def content_rating(self):
        return None

    def source_urls(self):
        return [self.movie.get("mainEntityOfPage")]

    def production_company(self):
        publisher = self.movie.get("productionCompany")
        publisher["url"] = publisher["mainEntityOfPage"]
        return self.organization(publisher)

    def aggregated_ratings(self):
        rating = self.movie.get("aggregateRating")
        # Decimals in Spain are represented with comma
        rating_value = rating.get("ratingValue").replace(",", ".")

        return [
            model.AggregateRating(
                schema_type=rating.get("@type"),
                best_rating=float(rating.get("bestRating")),
                worst_rating=float(rating.get("worstRating")),
                rating_value=float(rating_value),
                rating_count=int(rating.get("ratingCount")),
                source=self.movie.get("mainEntityOfPage"),
                name=None,
                description=None,
                review_count=None
            )
        ]

    def reviews(self):
        return []

    def images(self):
        return [self.movie.get("image").get("url")]

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
        trailer = self.movie.get("hasPart")
        video = model.Video(
            schema_type=trailer.get("@type"),
            name=None,
            description=None,
            thumbnail_url=None,
            url=trailer.get("potentialAction").get("target").get("urlTemplate")
        )
        return video

    def origin(self):
        return self.movie.get("countryOfOrigin")

    def events(self):
        event = self.movie.get("releasedEvent")
        return [
            model.PublicationEvent(
                schema_type=event.get("@type"),
                start_date=self.date(event.get("startDate")),
                location=event.get("location").get("name")
            )
        ]

    def date(self, serialized_date):
        return datetime.strptime(serialized_date, "%Y-%m-%d")
