from constants import BASE_URL
from models.tp1_model import Movie
from parser import OWLParser
from rdflib import Graph

graph = Graph()
graph.parse(BASE_URL, format="turtle")

with open("../data/tp2_movies.json", "r") as file:
    json_string = file.read()
movie_objects = Movie.schema().loads(json_string, many=True)


parser = OWLParser(graph)
for movie in movie_objects:
    parser.parse(movie)


with open("../data/generated_movies.ttl", "w") as file:
    serialized_graph = parser.serialize_graph()
    file.write(serialized_graph)
