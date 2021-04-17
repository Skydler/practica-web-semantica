from abc import abstractmethod
from model.model import Movie


class Parser:
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
    def name():
        pass

    @abstractmethod
    def description():
        pass

    @abstractmethod
    def content_rating():
        pass

    @abstractmethod
    def source_urls():
        pass

    @abstractmethod
    def production_company():
        pass

    @abstractmethod
    def aggregated_ratings():
        pass

    @abstractmethod
    def reviews():
        pass

    @abstractmethod
    def images():
        pass

    @abstractmethod
    def actors():
        pass

    @abstractmethod
    def characters():
        pass

    @abstractmethod
    def directors():
        pass

    @abstractmethod
    def authors():
        pass

    @abstractmethod
    def genres():
        pass

    @abstractmethod
    def keywords():
        pass

    @abstractmethod
    def duration():
        pass

    @abstractmethod
    def video():
        pass

    @abstractmethod
    def origin():
        pass

    @abstractmethod
    def events():
        pass
