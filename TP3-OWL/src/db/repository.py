from abc import ABC, abstractmethod
import json
import logging

from constants import BASE_URL
from db.merger import MergeStrategy
from db.parser import OWLParser
from models.model import Movie
from rdflib import Graph


class MovieRepository(ABC):
    def __init__(self, saving_path):
        self.movies = []
        self.merge_strategy = MergeStrategy(self.movies)
        self.path = saving_path

    @classmethod
    @abstractmethod
    def read(cls, path_file):
        pass

    @classmethod
    @abstractmethod
    def write(cls, path_file, movies):
        pass

    def save(self):
        self.write(self.path, self.movies)

    def add(self, new_movies):
        self.merge_strategy.merge(new_movies)


class JsonMovieRepository(MovieRepository):
    @classmethod
    def read(cls, path_file):
        with open(path_file, "r") as file:
            json_string = file.read()
        movie_objects = Movie.schema().loads(json_string, many=True)
        return movie_objects

    @classmethod
    def write(cls, path_file, movies):
        logging.info(f"Saving to {path_file}")
        movies_json = Movie.schema().dump(movies, many=True)
        with open(path_file, "w") as file:
            file.write(json.dumps(movies_json, indent=4, ensure_ascii=False))


class OwlMovieRepository(MovieRepository):
    @classmethod
    def read(cls, path_file):
        # TO-DO
        print("to-do")

    @classmethod
    def write(self, path_file, movies):
        graph = Graph()
        graph.parse(BASE_URL, format="turtle")

        parser = OWLParser(graph)

        for movie in movies:
            parser.parse(movie)

        with open(path_file, "w") as file:
            serialized_graph = graph.serialize(format="turtle").decode("utf-8")
            file.write(serialized_graph)
