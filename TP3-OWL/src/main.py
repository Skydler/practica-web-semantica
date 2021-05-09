from constants import BASE_URL
from models.tp1_model import Movie as TP1_Movie
from models.tp2_model import Movie as TP2_Movie
from parsers.tp1_parser import OWLParser as TP1_Parser
from parsers.tp2_parser import OWLParser as TP2_Parser
from rdflib import Graph
import logging


def parse_tp1_movies(graph):
    parser = TP1_Parser(graph)

    logging.info("Reading TP1 movies...")
    with open("../data/tp1_movies.json", "r") as file:
        json_string = file.read()
    movie_objects = TP1_Movie.schema().loads(json_string, many=True)

    logging.info("Parsing...")
    for movie in movie_objects:
        parser.parse(movie)


def parse_tp2_movies(graph):
    parser = TP2_Parser(graph)

    logging.info("Reading TP2 movies...")
    with open("../data/tp2_movies.json", "r") as file:
        json_string = file.read()
    movie_objects = TP2_Movie.schema().loads(json_string, many=True)

    logging.info("Parsing...")
    for movie in movie_objects:
        parser.parse(movie)


def main():
    # Init logging
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s')

    graph = Graph()
    graph.parse(BASE_URL, format="turtle")

    parse_tp1_movies(graph)
    parse_tp2_movies(graph)

    with open("../data/movie_individuals.ttl", "w") as file:
        serialized_graph = graph.serialize(
            format="turtle").decode("utf-8")
        file.write(serialized_graph)


if __name__ == "__main__":
    main()
