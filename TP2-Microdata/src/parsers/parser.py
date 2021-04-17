from abc import ABC, abstractmethod
from model.model import Movie


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
