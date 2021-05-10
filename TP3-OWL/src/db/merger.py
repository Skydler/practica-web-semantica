from deep_translator import GoogleTranslator
from fuzzywuzzy import fuzz


class MergeStrategy:
    def __init__(self, repository_movies):
        self.merged_movies = repository_movies
        self.titles_cache = {}
        self.translator = GoogleTranslator(source='auto', target='en')
        self.rate_rules = [
            ("N/A", ["-", "No determinado", "N/A"]),
            ("P-13", ["PG-13", "P-13", "Apta mayores de 13 años", "P13R"]),
            ("ATP", ["ATP", "Apta todo público",
                     "Apta todo público con reservas", "ATPR",
                     "Apta todo público C/L"]),
            ("P-16", ["PG-13", "P-16", "Apta mayores de 16 años", "P16R"]),
        ]

    def merge(self, movies):
        self.normalize(movies)

        for movie in movies:
            if found_movie := self.find_merged(movie):
                self.combine(found_movie, movie)
            else:
                self.add(movie)

        return self.merged_movies

    def normalize(self, movies):
        for movie in movies:
            movie.genres = self.translate_fields(movie.genres)

    def translate_fields(self, fields):
        return self.translator.translate_batch(fields) if fields else []

    def find_merged(self, movie):
        for merged_movie in self.merged_movies:
            if self.match_movies(movie, merged_movie):
                return merged_movie

    def match_movies(self, movie_1, movie_2):
        movie_id_1, movie_id_2 = self.get_id(movie_1), self.get_id(movie_2)

        ratio = fuzz.partial_ratio(movie_id_1, movie_id_2)

        return ratio > 90

    def get_id(self, movie):
        if movie_id := self.titles_cache.get(movie.name):
            return movie_id

        movie_id = self._normalize_text(movie.name)
        try:
            movie_id = self.translator.translate(movie_id)
        finally:
            self.titles_cache[movie.name] = movie_id
            return movie_id

    def _normalize_text(self, text):
        mapping_table = str.maketrans('áéíóúü', 'aeiouu')
        normalized = text.strip().lower().translate(mapping_table)
        return normalized

    def add(self, movie):
        self.merged_movies.append(movie)

    def combine(self, source_movie, target_movie):
        sm, tm = source_movie, target_movie

        sm.description = self._not_null_value(
            sm.description,
            tm.description
        )

        sm.content_rating = self._merge_rates(
            sm.content_rating,
            tm.content_rating
        )

        sm.source_urls += tm.source_urls

        sm.production_company = self._not_null_value(
            sm.production_company,
            tm.production_company
        )

        sm.aggregated_ratings += tm.aggregated_ratings

        sm.reviews += tm.reviews

        sm.images += tm.images

        sm.actors = list(set(sm.actors + tm.actors))

        sm.characters = self._merge_string_lists(
            sm.characters,
            tm.characters
        )

        sm.directors = list(set(sm.directors + tm.directors))

        sm.authors = list(set(sm.authors + tm.authors))

        sm.genres = self._merge_string_lists(sm.genres, tm.genres)

        sm.keywords = self._merge_string_lists(
            sm.keywords,
            tm.keywords
        )

        if sm.duration and tm.duration:
            sm.duration = max(sm.duration, tm.duration)
        else:
            sm.duration = sm.duration or tm.duration

        sm.video = self._not_null_value(sm.video, tm.video)

        sm.origins = self._merge_string_lists(sm.origins, tm.origins)

        sm.events += tm.events

        sm.shows += tm.shows

        sm.languages = self._merge_string_lists(sm.languages, tm.languages)

    def _not_null_value(self, source_field, target_field):
        return source_field or target_field

    def _merge_string_lists(self, source, target):
        normalized_source = [self._normalize_text(string) for string in source]
        for string in target:
            normal_string = self._normalize_text(string)
            if normal_string not in normalized_source:
                source.append(string)
        return source

    def _merge_rates(self, A_rate, B_rate):
        if A_rate and B_rate:
            A_category = self._classify_rate(A_rate)
            B_category = self._classify_rate(B_rate)

            if A_category == B_category:
                return A_category
            elif A_category == "N/A":
                return B_category
            elif B_category == "N/A":
                return A_category
            else:
                return "N/A"

        return A_rate or B_rate

    def _classify_rate(self, rate):
        for category, matches in self.rate_rules:
            if any(rate == match for match in matches):
                return category
        return "N/A"
