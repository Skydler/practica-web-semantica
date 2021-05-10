from constants import BASE_URL
import langcodes
from rdflib import Namespace, Literal
from rdflib.namespace import RDF
from utils.utils import to_turtle_fmt


class OWLParser:
    dbpedia = Namespace('http://dbpedia.org/ontology/')
    fabio = Namespace('http://purl.org/spar/fabio/')
    dcterms = Namespace('http://purl.org/dc/terms/')
    frbr = Namespace('http://purl.org/vocab/frbr/core#')
    schema = Namespace('https://schema.org/')
    baseURI = Namespace(f"{BASE_URL}#")

    def __init__(self, graph):
        self.g = graph

    def parse(self, movie_obj):
        self.build_movie(movie_obj)

    def build_movie(self, movie_obj):
        movie_title = self.baseURI[to_turtle_fmt(movie_obj.name)]
        self.g.add((movie_title, RDF.type, self.dbpedia.Film))

        self.add_synopsis(movie_title, movie_obj)
        self.add_content_rating(movie_title, movie_obj)
        self.add_source_urls(movie_title, movie_obj)
        self.add_production_company(movie_title, movie_obj)
        self.add_aggregated_ratings(movie_title, movie_obj)
        self.add_reviews(movie_title, movie_obj)
        self.add_images(movie_title, movie_obj)
        self.add_actors(movie_title, movie_obj)
        self.add_characters(movie_title, movie_obj)
        self.add_directors(movie_title, movie_obj)
        self.add_authors(movie_title, movie_obj)
        self.add_genres(movie_title, movie_obj)
        self.add_keywords(movie_title, movie_obj)
        self.add_duration(movie_title, movie_obj)
        self.add_video(movie_title, movie_obj)
        self.add_origins(movie_title, movie_obj)
        self.add_released_date(movie_title, movie_obj)
        self.add_languages(movie_title, movie_obj)

    def add_synopsis(self, movie_title, movie):
        if synopsis := movie.description:
            self.g.add((movie_title, self.baseURI.synopsis, Literal(synopsis)))

    def add_content_rating(self, movie_title, movie):
        if rating := movie.content_rating:
            self.g.add((movie_title, self.baseURI.content_rating,
                        Literal(rating)))

    def add_source_urls(self, movie_title, movie):
        for url in movie.source_urls:
            self.g.add((movie_title, self.dcterms.source, Literal(url)))

    def add_production_company(self, movie_title, movie):
        if prod_c := movie.production_company:
            self.g.add((movie_title, self.dbpedia.productionCompany,
                        self._create_company(prod_c, movie)))

    def add_aggregated_ratings(self, movie_title, movie):
        for index, rating in enumerate(movie.aggregated_ratings, 1):
            rating_uri = self._create_rating(
                to_turtle_fmt(movie.name), rating, index)

            self.g.add((rating_uri, self.schema.ratingCount,
                        Literal(rating.rating_count)))

            if review_count := rating.review_count:
                self.g.add((rating_uri, self.schema.reviewCount,
                            Literal(review_count)))

            self.g.add((rating_uri, self.dcterms.source,
                        Literal(rating.source)))

            self.g.add((movie_title, self.schema.aggregateRating, rating_uri))

    def add_reviews(self, movie_title, movie):
        for index, review in enumerate(movie.reviews, 1):
            encoded_review_name = f"{to_turtle_fmt(movie.name)}_review_{index}"
            review_uri = self.baseURI[encoded_review_name]

            self.g.add((review_uri, RDF.type, self.baseURI.movie_review))

            self.g.add((review_uri, self.baseURI.has_body,
                        Literal(review.review_body)))

            if site := review.url:
                site_uri = self._create_site(site, encoded_review_name)
                self.g.add((review_uri, self.fabio.hasManifestation, site_uri))

            self.g.add((review_uri, self.dcterms.source,
                        Literal(review.source)))

            self.g.add((review_uri, self.dcterms.created,
                        Literal(review.date_created)))

            if language := review.language:
                language_uri = self._create_language(movie_title, language)
                self.g.add((review_uri, self.dcterms.language, language_uri))

            if name := review.name:
                self.g.add((review_uri, self.dbpedia.Name, Literal(name)))

            author_uri = self._create_person(review.author,
                                             self.dbpedia.Person)
            self.g.add((review_uri, self.dcterms.creator, author_uri))

            if rating := review.review_rating:
                rating_uri = self._create_rating(encoded_review_name, rating)
                self.g.add((review_uri, self.baseURI.hasRating, rating_uri))

            if publisher := review.publisher:
                publisher_uri = self._create_company(publisher, movie)
                self.g.add((review_uri, self.dcterms.publisher, publisher_uri))

            self.g.add((review_uri, self.frbr.realization, movie_title))

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

    def add_genres(self, movie_title, movie):
        for genre in movie.genres:
            encoded_genre = to_turtle_fmt(genre)
            self.g.add((self.baseURI[encoded_genre], RDF.type,
                        self.dbpedia.MovieGenre))

            self.g.add((self.baseURI[encoded_genre], self.dbpedia.Name,
                        Literal(genre)))

            self.g.add((movie_title, self.dbpedia.genre,
                        self.baseURI[encoded_genre]))

    def add_keywords(self, movie_title, movie):
        for keyword in movie.keywords:
            self.g.add((movie_title, self.baseURI.keyword, Literal(keyword)))

    def add_duration(self, movie_title, movie):
        if duration := movie.duration:
            self.g.add((movie_title, self.dbpedia.duration, Literal(duration)))

    def add_video(self, movie_title, movie):
        if trailer := movie.video:
            encoded_trailer_name = f"{to_turtle_fmt(movie.name)}_trailer"
            trailer_uri = self.baseURI[encoded_trailer_name]

            self.g.add((trailer_uri, RDF.type, self.baseURI.trailer))

            if trailer.name:
                self.g.add(
                    (trailer_uri, self.dbpedia.Name, Literal(trailer.name)))

            if trailer.url:
                self.g.add(
                    (trailer_uri, self.baseURI.url, Literal(trailer.url)))

            if trailer.description:
                self.g.add((trailer_uri, self.dbpedia.description,
                            Literal(trailer.description)))

            if thumbnail_url := trailer.thumbnail_url:
                image_uri = self._create_image(trailer_uri, thumbnail_url)
                self.g.add((trailer_uri, self.dbpedia.thumbnail, image_uri))

            self.g.add((movie_title, self.baseURI.hasTrailer, trailer_uri))

    def add_origins(self, movie_title, movie):
        for origin in movie.origins:
            encoded_origin = to_turtle_fmt(origin)
            origin_uri = self.baseURI[encoded_origin]

            self.g.add((origin_uri, RDF.type, self.dbpedia.Country))
            self.g.add((origin_uri, self.dbpedia.Name, Literal(origin)))

            self.g.add((movie_title, self.dbpedia.origin, origin_uri))

    def add_released_date(self, movie_title, movie):
        if movie.events:
            publication_event = movie.events[0]
            release_date = publication_event.start_date

            self.g.add((movie_title, self.dbpedia.releaseDate,
                        Literal(release_date)))

    def add_shows(self, movie_title, movie):
        for index, show in enumerate(movie.shows, 1):
            encoded_show_name = f"{to_turtle_fmt(movie.name)}_show_{index}"
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

    def add_languages(self, movie_title, movie):
        for lang in movie.languages:

            language_uri = self._create_language(movie_title, lang)
            self.g.add((movie_title, self.dbpedia.language, language_uri))

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
            image_uri = self._create_image(person_URI, image_url=person.image)
            self.g.add((person_URI, self.dbpedia.thumbnail, image_uri))

        return person_URI

    def _create_image(self, subject_uri, image_url):
        encoded_person_img = f"{to_turtle_fmt(subject_uri)}_img"
        image_uri = self.baseURI[encoded_person_img]

        self.g.add((image_uri, RDF.type, self.dbpedia.Image))
        self.g.add((image_uri, self.baseURI.url, Literal(image_url)))

        return image_uri

    def _create_language(self, movie_uri, lang):
        encoded_lang = to_turtle_fmt(lang)

        # I'm sorry it's the only one it doesn't detect
        if encoded_lang == "Castellano":
            lang_code = "es"
        else:
            lang_code = langcodes.find(lang).language

        language_uri = self.baseURI[encoded_lang]

        self.g.add((language_uri, RDF.type, self.dbpedia.Language))

        self.g.add((language_uri, self.dbpedia.languageCode,
                    Literal(lang_code)))

        return language_uri

    def _create_site(self, site, encoded_review_name):
        encoded_site_name = f"{encoded_review_name}_site"
        site_uri = self.baseURI[encoded_site_name]

        self.g.add((site_uri, RDF.type, self.fabio.WebPage))
        self.g.add((site_uri, self.fabio.hasURL, Literal(site)))

        return site_uri

    def _create_rating(self, prefix, rating, index=None):
        encoded_rating_name = f"{prefix}_rating"

        if index:
            encoded_rating_name += f'_{index}'

        rating_URI = self.baseURI[encoded_rating_name]

        # This could be AggregateRating or just Rating
        schema_type = self.schema[rating.schema_type]
        self.g.add((rating_URI, RDF.type, schema_type))

        if name := rating.name:
            self.g.add((rating_URI, self.dbpedia.Name, Literal(name)))

        if description := rating.description:
            self.g.add((rating_URI, self.dbpedia.description,
                        Literal(description)))

        self.g.add((rating_URI, self.baseURI.ratingValue,
                    Literal(rating.rating_value)))

        self.g.add((rating_URI, self.baseURI.bestRating,
                    Literal(rating.best_rating)))

        self.g.add((rating_URI, self.baseURI.worstRating,
                    Literal(rating.worst_rating)))

        return rating_URI
