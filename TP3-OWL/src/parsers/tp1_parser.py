from constants import BASE_URL
import langcodes
from rdflib import Namespace, Literal  # , Bnode
from rdflib.namespace import RDF
from utils.utils import to_turtle_fmt


class OWLParser:
    dbpedia = Namespace('http://dbpedia.org/ontology/')
    baseURI = Namespace(f"{BASE_URL}#")

    def __init__(self, graph):
        self.g = graph

    def parse(self, movie_obj):
        self.build_movie(movie_obj)

    def build_movie(self, movie_obj):
        movie_title = self.baseURI[to_turtle_fmt(movie_obj.title)]
        self.g.add((movie_title, RDF.type, self.dbpedia.Film))

        self.add_genres(movie_title, movie_obj)
        self.add_languages(movie_title, movie_obj)
        self.add_origins(movie_title, movie_obj)
        self.add_duration(movie_title, movie_obj)
        self.add_directors(movie_title, movie_obj)
        self.add_rating(movie_title, movie_obj)
        self.add_actors(movie_title, movie_obj)
        self.add_synopsis(movie_title, movie_obj)
        self.add_trailer(movie_title, movie_obj)
        self.add_shows(movie_title, movie_obj)
        self.add_released_date(movie_title, movie_obj)

    def add_genres(self, movie_title, movie):
        for genre in movie.genres:
            encoded_genre = to_turtle_fmt(genre)
            self.g.add((self.baseURI[encoded_genre], RDF.type,
                        self.dbpedia.MovieGenre))

            self.g.add((self.baseURI[encoded_genre], self.dbpedia.Name,
                        Literal(genre)))

            self.g.add((movie_title, self.dbpedia.genre,
                        self.baseURI[encoded_genre]))

    def add_languages(self, movie_title, movie):
        for lang in movie.languages:
            encoded_lang = to_turtle_fmt(lang)

            # I'm sorry it's the only one it doesn't detect
            if encoded_lang == "Castellano":
                lang_code = "es"
            else:
                lang_code = langcodes.find(lang).language

            self.g.add((self.baseURI[encoded_lang], RDF.type,
                        self.dbpedia.Language))

            self.g.add((self.baseURI[encoded_lang], self.dbpedia.languageCode,
                        Literal(lang_code)))

            self.g.add((movie_title, self.dbpedia.language,
                        self.baseURI[encoded_lang]))

    def add_origins(self, movie_title, movie):
        for origin in movie.origins:
            encoded_origin = to_turtle_fmt(origin)
            self.g.add((self.baseURI[encoded_origin], RDF.type,
                        self.dbpedia.Country))

            self.g.add((self.baseURI[encoded_origin], self.dbpedia.Name,
                        Literal(origin)))

            self.g.add((movie_title, self.dbpedia.origin,
                        self.baseURI[encoded_origin]))

    def add_duration(self, movie_title, movie):
        if duration := movie.duration:
            self.g.add((movie_title, self.dbpedia.duration, Literal(duration)))

    def add_directors(self, movie_title, movie):
        for director in movie.directors:
            encoded_director = to_turtle_fmt(director)
            self.g.add((self.baseURI[encoded_director], RDF.type,
                        self.dbpedia.MovieDirector))

            self.g.add((self.baseURI[encoded_director], self.dbpedia.Name,
                        Literal(director)))

            self.g.add((movie_title, self.dbpedia.director,
                        self.baseURI[encoded_director]))

    def add_rating(self, movie_title, movie):
        if rating := movie.rated:
            self.g.add((movie_title, self.baseURI.content_rating,
                        Literal(rating)))

    def add_actors(self, movie_title, movie):
        for actor in movie.actors:
            encoded_actor = to_turtle_fmt(actor)
            self.g.add((self.baseURI[encoded_actor], RDF.type,
                        self.dbpedia.Actor))

            self.g.add((self.baseURI[encoded_actor], self.dbpedia.Name,
                        Literal(actor)))

            self.g.add((movie_title, self.dbpedia.starring,
                        self.baseURI[encoded_actor]))

    def add_synopsis(self, movie_title, movie):
        if synopsis := movie.synopsis:
            self.g.add((movie_title, self.baseURI.synopsis, Literal(synopsis)))

    def add_trailer(self, movie_title, movie):
        if trailer := movie.trailer:
            encoded_trailer_name = f"{to_turtle_fmt(movie.title)}_trailer"
            self.g.add((self.baseURI[encoded_trailer_name], RDF.type,
                        self.baseURI.trailer))

            self.g.add((self.baseURI[encoded_trailer_name], self.baseURI.url,
                        Literal(trailer)))

            self.g.add((movie_title, self.baseURI.hasTrailer,
                        self.baseURI[encoded_trailer_name]))

    def add_shows(self, movie_title, movie):
        for index, show in enumerate(movie.shows, 1):
            encoded_show_name = f"{to_turtle_fmt(movie.title)}_show_{index}"
            self.g.add((self.baseURI[encoded_show_name], RDF.type,
                        self.baseURI.film_show))

            self.g.add((self.baseURI[encoded_show_name], self.baseURI.room,
                        self._create_room(show.room, show.cinema)))

            self.g.add((self.baseURI[encoded_show_name],
                        self.dbpedia.startDateTime,
                        Literal(show.time)))

            self.g.add((self.baseURI[encoded_show_name],
                        self.dbpedia.subtitle,
                        Literal(show.language)))

            self.g.add((movie_title, self.baseURI.hasShow,
                        self.baseURI[encoded_show_name]))

    def _create_room(self, room, cinema):
        encoded_room_name = f"room_{to_turtle_fmt(room)}"
        self.g.add((self.baseURI[encoded_room_name], RDF.type,
                    self.baseURI.cinema_room))

        self.g.add((self.baseURI[encoded_room_name], self.baseURI.cinema,
                    self._create_cinema(cinema)))

        self.g.add((self.baseURI[encoded_room_name], self.dbpedia.Name,
                    Literal(room)))

        return self.baseURI[encoded_room_name]

    def _create_cinema(self, cinema):
        encoded_cinema_name = to_turtle_fmt(cinema)
        self.g.add((self.baseURI[encoded_cinema_name], RDF.type,
                    self.dbpedia.Cinema))

        self.g.add((self.baseURI[encoded_cinema_name], self.dbpedia.Name,
                    Literal(cinema)))

        return self.baseURI[encoded_cinema_name]

    def add_released_date(self, movie_title, movie):
        # https://trello.com/c/cDYvF6b9/30-released-del-modelo-1-y-released-del-modelo-2-son-dos-cosas-distintas-y-no-deber%C3%ADan-ser-mergeadas-en-owl
        # if movie.released:
        #     date_uri = f"{to_turtle_fmt(movie.title)}_released_date"

        #     self.g.add((movie_title, self.dbpedia.releaseDate,
        #                 BNode(date_uri)))
        pass
