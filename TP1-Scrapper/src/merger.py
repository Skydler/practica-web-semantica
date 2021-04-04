from deep_translator import GoogleTranslator
from fuzzywuzzy import fuzz


class MergeStrategy:
    def __init__(self):
        self.merge = []
        self.titles_cache = {}
        self.translator = GoogleTranslator(source='auto', target='es')

    def find(self, movie):
        for merged_movie in self.merge:
            if self.match_movies(movie, merged_movie):
                return merged_movie

    def match_movies(self, movie_1, movie_2):
        movie_id_1, movie_id_2 = self.get_id(movie_1), self.get_id(movie_2)

        ratio = fuzz.ratio(movie_id_1, movie_id_2)

        return ratio > 90

    def get_id(self, movie):
        if movie_id := self.titles_cache.get(movie.title):
            return movie_id

        movie_id = movie.title.strip().lower().translate(
            str.maketrans('áéíóúü', 'aeiouu')
        )

        try:
            movie_id = self.translator.translate(movie_id)
        finally:
            self.titles_cache[movie.title] = movie_id
            return movie_id

    def add(self, movie):
        self.merge.append(movie)

    def to_list(self):
        return self.merge


def merge(movies):
    strategy = MergeStrategy()

    for movie in movies:
        if found_movie := strategy.find(movie):
            found_movie.shows += movie.shows
            # TODO: Add fields logic, e.g. union between actors
        else:
            strategy.add(movie)

    return strategy.to_list()
