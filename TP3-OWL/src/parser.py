from rdflib import Namespace, Literal
from rdflib.namespace import RDF  # , OWL, RDFS, XSD
from constants import BASE_URL


class OWLParser:
    dbpedia = Namespace('http://dbpedia.org/ontology/')
    movie = Namespace(f"{BASE_URL}#")

    def __init__(self, graph):
        self.g = graph
        self.serialize_fmt = "turtle"

    def parse(self, movie_obj):
        pass
        # self.build_movie(movie_obj)

    def serialize_graph(self):
        serialized_graph = self.g.serialize(
            format=self.serialize_fmt).decode("utf-8")
        return serialized_graph

    def build_movie(self, movie_obj):
        m = self.movie
        dbp = self.dbpedia
        self.g.add((m[movie_obj.name], RDF.type, dbp.Film))
        self.g.add((m.pepe, m.url, Literal(
            "https://rdflib.readthedocs.io/en/stable/index.html")))
