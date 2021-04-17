from datetime import datetime

from model.model import AggregateRating, Rating
from model.model import Organization, Person, Review
from parsers.parser import Parser


class RottenTomatoesParser(Parser):
    def name(self):
        return self.movie.get('name')

    def description(self):
        return self.movie.get('description')

    def content_rating(self):
        return self.movie.get('contentRating')

    def source_urls(self):
        return [self.movie.get('url')]

    def production_company(self):
        company = self.movie['productionCompany']
        return self.organization(company)

    def aggregated_ratings(self):
        rating = self.movie['aggregateRating']

        return [
            AggregateRating(
                schema_type=rating['@type'],
                name=rating.get('name'),
                description=rating.get('description'),
                rating_value=float(rating['ratingValue']),
                best_rating=float(rating['bestRating']),
                worst_rating=float(rating['worstRating']),
                rating_count=int(rating['ratingCount']),
                review_count=int(rating['reviewCount']),
                source=self.movie.get('url')
            )
        ]

    def reviews(self):
        reviews = []

        for serialized_review in self.movie['review']:
            review = Review(
                schema_type=serialized_review['@type'],
                review_body=serialized_review['reviewBody'],
                url=serialized_review['url'],
                date_created=self.date(serialized_review['dateCreated']),
                language=serialized_review.get('language'),
                name=serialized_review.get('name'),
                author=self.person(serialized_review['author']),
                review_rating=self.rating(serialized_review['reviewRating']),
                publisher=self.organization(serialized_review['publisher']),
                source=self.movie.get('url')
            )

            reviews.append(review)

        return reviews

    def rating(self, serialized_rating):
        return Rating(
            schema_type=serialized_rating['@type'],
            name=serialized_rating.get('name'),
            description=serialized_rating.get('description'),
            rating_value=serialized_rating['ratingValue'],
            best_rating=serialized_rating['bestRating'],
            worst_rating=serialized_rating['worstRating'],
        )

    def organization(self, serialized_organization):
        return Organization(
            schema_type=serialized_organization['@type'],
            name=serialized_organization['name'],
            url=serialized_organization.get('url')
        )

    def date(self, serialized_date):
        return datetime.fromisoformat(serialized_date)

    def images(self):
        return [self.movie['image']]

    def actors(self):
        return [self.person(actor) for actor in self.movie['actors']]

    def person(self, serialized_person):
        url = serialized_person.get('sameAs') or serialized_person.get('url')

        return Person(
            schema_type=serialized_person['@type'],
            name=serialized_person['name'],
            url=url,
            image=serialized_person.get('image')
        )

    def characters(self):
        return list(filter(bool, self.movie['character']))

    def directors(self):
        directors = self.movie['director']
        return [self.person(director) for director in directors]

    def authors(self):
        authors = self.movie['author']
        return [self.person(author) for author in authors]

    def genres(self):
        return self.movie['genre']

    def keywords(self):
        return []

    def duration(self):
        return None

    def video(self):
        return None

    def origin(self):
        return None

    def events(self):
        return []
