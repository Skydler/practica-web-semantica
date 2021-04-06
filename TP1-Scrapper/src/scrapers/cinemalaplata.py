from datetime import datetime
from threading import Thread

from bs4 import BeautifulSoup
from models.movie import Show, Movie
import requests
from typing import List
from urllib.parse import urljoin


DOMAIN = "http://www.cinemalaplata.com/"
BILLBOARD_URL = f"{DOMAIN}Cartelera.aspx"
FUTURE_RELEASES_URL = f"{BILLBOARD_URL}?seccion=FUTURO"


class MovieParser(Thread):
    def __init__(self, link, parsed_movies):
        super(MovieParser, self).__init__()
        self.link = link
        self.parsed_movies = parsed_movies

    def get_text(self, soup, selector):
        return soup.select_one(selector).text.strip()

    def get_shows(self, movie):
        shows_soup = movie.select("#ctl00_cph_pnFunciones > .col-2")

        for show_soup in shows_soup:
            cine_and_room = list(map(
                str.strip,
                show_soup.select_one("span").text.split("-")
            ))

            if len(cine_and_room) == 2:
                cinema, room = cine_and_room

                schedules = show_soup.p.stripped_strings

                for schedule in schedules:
                    language, hours = schedule.split(": ")

                    for hour in map(str.strip, hours.split("-")):
                        yield Show(
                            cinema=cinema,
                            room=room,
                            language=language,
                            time=self.get_time(hour),
                        )

    def get_time(self, hour_time):
        year, month, day, *_ = datetime.now().timetuple()
        hour, minute = map(int, hour_time.split(':'))

        return datetime(year, month, day, hour, minute)

    def get_duration(self, movie, selector):
        duration_text = self.get_text(movie, selector).split(" ")[0]
        return int(duration_text) if duration_text.isdigit() else None

    def get_actors(self, movie, selector):
        actors = self.get_text(movie, selector).strip('.')

        # If the string still has dots, normalize it replacing "." for ","
        # where it's needed
        if dot_count := actors.count("."):
            # This will be handy for char replacement
            char_list = list(actors)
            dot_index = 0
            for _ in range(dot_count):
                # dot_index ensures that it's allways taking the next "." index
                if index := actors.find(".", dot_index):
                    dot_index = index
                    prev_char = actors[index - 1]
                    if prev_char.islower():
                        char_list[index] = ","

            actors = "".join(char_list)

        # The actors are separated by commas
        actors = actors.split(", ")

        # Filter actors with capitalized names
        actors = [actor for actor in actors if actor and actor[0].isupper()]

        return actors

    def get_directors(self, movie, selector):
        directors = self.get_text(movie, selector).strip(".").split(", ")
        return directors

    def parse_movie(self, movie):
        title = self.get_text(movie, ".page-title")
        genres = self.get_text(movie, "#ctl00_cph_lblGenero").split(", ")
        languages = self.get_text(movie, "#ctl00_cph_lblIdioma").split(", ")
        origins = self.get_text(movie, "#ctl00_cph_lblPaisOrigen").split(", ")
        duration = self.get_duration(movie, "#ctl00_cph_lblDuracion")
        directors = self.get_directors(movie, "#ctl00_cph_lblDirector")
        actors = self.get_actors(movie, "#ctl00_cph_lblActores")
        rated = self.get_text(movie, "#ctl00_cph_lblCalificacion")
        synopsis = self.get_text(movie, "#ctl00_cph_lblSinopsis")
        trailer = movie.select_one(".embed-responsive-item").attrs.get("src")
        shows = list(self.get_shows(movie))
        distributor = None
        released = len(shows) != 0

        movie = Movie(
            title=title,
            genres=genres,
            languages=languages,
            origins=origins,
            duration=duration,
            directors=directors,
            rated=rated,
            actors=actors,
            synopsis=synopsis,
            trailer=trailer,
            shows=shows,
            distributor=distributor,
            released=released
        )

        self.parsed_movies.append(movie)

    def run(self):
        response = requests.get(self.link)
        html = response.text
        movie = BeautifulSoup(html, 'html.parser')
        self.parse_movie(movie)


def parse_movies(links):
    parsed_movies = []

    threads = [MovieParser(link, parsed_movies) for link in links]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    return parsed_movies


def get_movies(link):
    response = requests.get(link)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    movies = soup.select(".page-container.singlepost")
    links = [urljoin(DOMAIN, movie.h4.strong.a['href']) for movie in movies]

    return parse_movies(links)


def scrap() -> List[Movie]:
    future_releases = get_movies(FUTURE_RELEASES_URL)
    billboard = get_movies(BILLBOARD_URL)

    movies = billboard + future_releases

    return movies
