from merger.full_merge import FullMerge
from model import Movie
import logging
import json


class MovieRepository:
    def __init__(self, saving_path):
        self.movies = []
        self.merge_strategy = FullMerge(self.movies)
        self.path = saving_path

    @classmethod
    def read(cls, path_file):
        with open(path_file, "r") as file:
            json_string = file.read()
        movie_objects = Movie.schema().loads(json_string, many=True)
        return movie_objects

    @classmethod
    def write(self, path_file, movies):
        logging.info(f"Saving to {path_file}")
        movies_json = Movie.schema().dump(movies, many=True)
        with open(path_file, "w") as file:
            file.write(json.dumps(movies_json, indent=4, ensure_ascii=False))

    def save(self):
        self.write(self.path, self.movies)

    def add(self, new_movies):
        self.merge_strategy.merge(new_movies)
