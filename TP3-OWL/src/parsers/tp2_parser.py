from rdflib import Namespace, Literal
from rdflib.namespace import RDF
from constants import BASE_URL
from utils.utils import to_turtle_fmt
# import langcodes


class OWLParser:
    dbpedia = Namespace('http://dbpedia.org/ontology/')
    baseURI = Namespace(f"{BASE_URL}#")

    def __init__(self, graph):
        self.g = graph

    def parse(self, movie_obj):
        self.build_movie(movie_obj)

    def build_movie(self, movie_obj):
        movie_title = self.baseURI[to_turtle_fmt(movie_obj.name)]
        self.g.add((movie_title, RDF.type, self.dbpedia.Film))

        self.add_synopsis(movie_title, movie_obj)
        self.add_rating(movie_title, movie_obj)
        self.add_source_urls(movie_title, movie_obj)
        self.add_production_company(movie_title, movie_obj)
        # self.add_aggregated_ratings(movie_title, movie_obj)
        # self.add_reviews(movie_title, movie_obj)
        self.add_images(movie_title, movie_obj)
        self.add_actors(movie_title, movie_obj)
        self.add_characters(movie_title, movie_obj)
        self.add_directors(movie_title, movie_obj)
        self.add_authors(movie_title, movie_obj)

    def add_synopsis(self, movie_title, movie):
        if synopsis := movie.description:
            self.g.add((movie_title, self.baseURI.synopsis, Literal(synopsis)))

    def add_rating(self, movie_title, movie):
        if rating := movie.content_rating:
            self.g.add((movie_title, self.baseURI.content_rating,
                        Literal(rating)))

    def add_source_urls(self, movie_title, movie):
        for url in movie.source_urls:
            self.g.add((movie_title, self.baseURI.sourceUrl, Literal(url)))

    def add_production_company(self, movie_title, movie):
        if prod_c := movie.production_company:
            self.g.add((movie_title, self.dbpedia.productionCompany,
                        self._create_company(prod_c, movie)))

    def add_images(self, movie_title, movie):
        for i, image in enumerate(movie.images, 1):
            encoded_image_name = f"{to_turtle_fmt(movie.name)}_cover_image_{i}"
            self.g.add((self.baseURI[encoded_image_name], RDF.type,
                        self.dbpedia.Image))

            self.g.add((self.baseURI[encoded_image_name], self.baseURI.url,
                        Literal(image)))

            self.g.add((movie_title, self.dbpedia.thumbnail,
                        self.baseURI[encoded_image_name]))

    def add_actors(self, movie_title, movie):
        for actor in movie.actors:
            actor_URI = self._create_person(actor, self.dbpedia.Actor)
            self.g.add((movie_title, self.dbpedia.starring, actor_URI))

    def add_characters(self, movie_title, movie):
        for character in movie.characters:
            # Beware of character reptition across movies. This could be a
            # problem, but fixing it sacrifices legibility. Hi future me!
            encoded_character_name = to_turtle_fmt(character)
            self.g.add((self.baseURI[encoded_character_name], RDF.type,
                        self.dbpedia.FictionalCharacter))

            self.g.add((self.baseURI[encoded_character_name],
                        self.dbpedia.Name, Literal(character)))

            self.g.add((movie_title, self.baseURI.hasCharacter,
                        self.baseURI[encoded_character_name]))

    def add_directors(self, movie_title, movie):
        for director in movie.directors:
            director_URI = self._create_person(director,
                                               self.dbpedia.MovieDirector)
            self.g.add((movie_title, self.dbpedia.director, director_URI))

    def add_authors(self, movie_title, movie):
        for i, author in enumerate(movie.authors, 1):
            if author.schema_type == "Organization":
                author_URI = self._create_company(author, movie, i=i)
            else:
                author_URI = self._create_person(author, self.dbpedia.Person)

            self.g.add((movie_title, self.dbpedia.author, author_URI))

    def _create_company(self, company, movie, i=1):
        if company.name:
            encoded_company_name = to_turtle_fmt(company.name)
        else:
            encoded_company_name = f"{to_turtle_fmt(movie.name)}_company_{i}"

        self.g.add((self.baseURI[encoded_company_name], RDF.type,
                    self.dbpedia.Company))

        if company.name:
            self.g.add((self.baseURI[encoded_company_name], self.dbpedia.Name,
                        Literal(company.name)))

        if company.url:
            self.g.add((self.baseURI[encoded_company_name], self.baseURI.url,
                        Literal(company.url)))

        return self.baseURI[encoded_company_name]

    def _create_person(self, person, person_type):
        encoded_person_name = to_turtle_fmt(person.name)
        person_URI = self.baseURI[encoded_person_name]
        self.g.add((person_URI, RDF.type, person_type))
        self.g.add((person_URI, self.dbpedia.Name, Literal(person.name)))

        if person.url:
            self.g.add((person_URI, self.baseURI.url, Literal(person.url)))

        if person.image:
            self.g.add((person_URI, self.dbpedia.thumbnail,
                        self._create_image(person)))

        return person_URI

    def _create_image(self, person):
        encoded_person_img = f"{to_turtle_fmt(person.name)}_img"
        self.g.add((self.baseURI[encoded_person_img], RDF.type,
                    self.dbpedia.Image))
        self.g.add((self.baseURI[encoded_person_img], self.baseURI.url,
                    Literal(person.image)))

        return self.baseURI[encoded_person_img]
