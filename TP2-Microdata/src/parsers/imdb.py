from datetime import datetime

from durations import Duration
from model.model import AggregateRating, Review, Video
from parsers.parser import Parser


class ImdbParser(Parser):

    @property
    def BASE_URL(self):
        return "https://www.imdb.com/"

    def name(self):
        return self.movie['name']

    def description(self):
        return self.movie.get('description')

    def content_rating(self):
        return self.movie['contentRating']

    def source_urls(self):
        return [self.absolute_url(self.movie['url'])]

    def production_company(self):
        return None

    def aggregated_ratings(self):
        rating = self.movie['aggregateRating']
        review_count = rating.get('reviewCount')

        return [
            AggregateRating(
                schema_type=rating['@type'],
                name=rating.get('name'),
                description=rating.get('description'),
                rating_value=float(rating['ratingValue']),
                best_rating=float(rating['bestRating']),
                worst_rating=float(rating['worstRating']),
                rating_count=int(rating['ratingCount']),
                review_count=int(review_count) if review_count else None,
                source=self.movie['url']
            )
        ]

    def reviews(self):
        serialized_review = self.movie['review']

        review = Review(
            schema_type=serialized_review['@type'],
            review_body=serialized_review['reviewBody'],
            url=serialized_review.get('url'),
            date_created=self.date(serialized_review['dateCreated']),
            language=serialized_review.get('inLanguage'),
            name=serialized_review.get('name'),
            author=self.person(serialized_review['author']),
            review_rating=self.rating(serialized_review['reviewRating']),
            publisher=self.organization(serialized_review.get('publisher')),
            source=self.movie.get('url')
        )

        return [review]

    def date(self, serialized_date):
        return datetime.strptime(serialized_date, "%Y-%m-%d")

    def images(self):
        return [self.movie['image']]

    def actors(self):
        actors = self.movie['actor']
        return list(map(self.person, actors))

    def characters(self):
        return []

    def directors(self):
        director = self.movie['director']
        return [self.person(director)]

    def authors(self):
        creators = self.movie['creator']

        return list(map(
            lambda c: self.person(
                c) if c['@type'] == "Person" else self.organization(c),
            creators
        ))

    def genres(self):
        return self.movie['genre']

    def keywords(self):
        return self.movie['keywords'].split(',')

    def duration(self):
        if duration := self.movie.get('duration'):
            duration = duration.lower()[2:]
            return Duration(duration).to_minutes()

    def video(self):
        trailer = self.movie['trailer']

        return Video(
            schema_type=trailer['@type'],
            name=trailer['name'],
            url=self.absolute_url(trailer['embedUrl']),
            description=trailer['description'],
            thumbnail_url=trailer['thumbnailUrl']
        )

    def origin(self):
        return None

    def events(self):
        return []
