from abc import ABC, abstractmethod, abstractproperty
from model.model import Movie, Organization, Person, Rating
from urllib.parse import urlparse, urljoin


class Parser(ABC):
    def __init__(self, movie):
        self.movie = movie

    def run(self):
        return Movie(
            schema_type=self.movie['@type'],
            name=self.name(),
            description=self.description(),
            content_rating=self.content_rating(),
            source_urls=self.source_urls(),
            production_company=self.production_company(),
            aggregated_ratings=self.aggregated_ratings(),
            reviews=self.reviews(),
            images=self.images(),
            actors=self.actors(),
            characters=self.characters(),
            directors=self.directors(),
            authors=self.authors(),
            genres=self.genres(),
            keywords=self.keywords(),
            duration=self.duration(),
            video=self.video(),
            origin=self.origin(),
            events=self.events(),
        )

    def organization(self, serialized_organization):
        if serialized_organization is None:
            return None

        return Organization(
            schema_type=serialized_organization['@type'],
            name=serialized_organization.get('name'),
            url=self.absolute_url(serialized_organization.get('url'))
        )

    def person(self, serialized_person):
        url = serialized_person.get('sameAs') or serialized_person.get('url')

        return Person(
            schema_type=serialized_person['@type'],
            name=serialized_person['name'],
            url=self.absolute_url(url),
            image=serialized_person.get('image')
        )

    def rating(self, serialized_rating):
        return Rating(
            schema_type=serialized_rating['@type'],
            name=serialized_rating.get('name'),
            description=serialized_rating.get('description'),
            rating_value=serialized_rating['ratingValue'],
            best_rating=serialized_rating['bestRating'],
            worst_rating=serialized_rating['worstRating'],
        )

    def absolute_url(self, url):
        if urlparse(url).netloc:
            return url

        return urljoin(self.BASE_URL, url)

    @abstractproperty
    def BASE_URL(self):
        pass

    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def description(self):
        pass

    @abstractmethod
    def content_rating(self):
        pass

    @abstractmethod
    def source_urls(self):
        pass

    @abstractmethod
    def production_company(self):
        pass

    @abstractmethod
    def aggregated_ratings(self):
        pass

    @abstractmethod
    def reviews(self):
        pass

    @abstractmethod
    def images(self):
        pass

    @abstractmethod
    def actors(self):
        pass

    @abstractmethod
    def characters(self):
        pass

    @abstractmethod
    def directors(self):
        pass

    @abstractmethod
    def authors(self):
        pass

    @abstractmethod
    def genres(self):
        pass

    @abstractmethod
    def keywords(self):
        pass

    @abstractmethod
    def duration(self):
        pass

    @abstractmethod
    def video(self):
        pass

    @abstractmethod
    def origin(self):
        pass

    @abstractmethod
    def events(self):
        pass
