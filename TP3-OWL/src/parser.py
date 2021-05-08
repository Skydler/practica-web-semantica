# from urllib import parse
from rdflib import Namespace, Literal
from rdflib.namespace import RDF  # , OWL, RDFS, XSD
from constants import BASE_URL


class OWLParser:
    dbpedia = Namespace('http://dbpedia.org/ontology/')
    baseURI = Namespace(f"{BASE_URL}#")

    def __init__(self, graph):
        self.g = graph
        self.serialize_fmt = "turtle"

    def parse(self, movie_obj):
        # breakpoint()
        self.build_movie(movie_obj)

    def serialize_graph(self):
        serialized_graph = self.g.serialize(
            format=self.serialize_fmt).decode("utf-8")
        return serialized_graph

    def build_movie(self, movie_obj):
        m = self.baseURI
        dbp = self.dbpedia
        # Usando el urleconding algún caracter como el % hace que
        # el parseo a turtle language se bugee y muestre la url completa
        # en vez de la abreviación. Por eso opté hasta que encuentre una
        # mejor forma hacer el replace de abajo. Igualmente algúnos caracteres
        # especiales como las tíldes, porcentajes, etc me generan desconfianza.
        # Se me ocurre que hay que buscar la manera de normalizar las palabras
        # y también ponerlas en lowercase.
        #
        # movie_title = m[parse.quote(movie_obj.title)]
        movie_title = m[movie_obj.title.replace(" ", "_")]
        self.g.add((movie_title, RDF.type, dbp.Film))

        self.add_genres(movie_title, movie_obj)
        self.add_origins(movie_title, movie_obj)

    def add_genres(self, movie_title, movie):
        for genre in movie.genres:
            # encoded_genre = parse.quote(genre)
            encoded_genre = genre.replace(" ", "_")
            self.g.add((self.baseURI[encoded_genre], RDF.type,
                        self.dbpedia.MovieGenre))

            self.g.add((self.baseURI[encoded_genre], self.dbpedia.Name,
                        Literal(genre)))

            self.g.add((movie_title, self.dbpedia.genre,
                        self.baseURI[encoded_genre]))

    def add_origins(self, movie_title, movie):
        for origin in movie.origins:
            # encoded_origin = parse.quote(origin)
            encoded_origin = origin.replace(" ", "_")
            self.g.add((self.baseURI[encoded_origin], RDF.type,
                        self.dbpedia.Country))

            self.g.add((self.baseURI[encoded_origin], self.dbpedia.Name,
                        Literal(origin)))

            self.g.add((movie_title, self.dbpedia.origin,
                        self.baseURI[encoded_origin]))
