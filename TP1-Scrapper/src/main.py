from bs4 import BeautifulSoup
from model import Show, Movie
from threading import Thread
from urllib.parse import urljoin
import requests
import json


FUTURE_RELEASES_URL = "http://www.cinemalaplata.com/Cartelera.aspx?seccion=FUTURO"
BILLBOARD_URL = "http://www.cinemalaplata.com/Cartelera.aspx"
DOMAIN = "http://www.cinemalaplata.com/"


class MovieParser(Thread):
    def __init__(self, link, parsed_movies):
        super(MovieParser, self).__init__()
        self.link = link
        self.parsed_movies = parsed_movies

    def get_text(self, soup, selector):
        return soup.select_one(selector).text.strip()

    def get_shows(self, movie):
        shows = []

        shows_soup = movie.select("#ctl00_cph_pnShowes > .col-2")
        for show_soup in shows_soup:
            cine_and_room = list(map(
                str.strip,
                show_soup.select_one("span").text.split("-")
            ))

            if len(cine_and_room) == 2:
                cine, room = cine_and_room

                schedules = show_soup.p.stripped_strings

                for schedule in schedules:
                    language, hours = schedule.split(": ")

                    show = Show(
                        cine=cine,
                        room=room,
                        language=language,
                        hours=map(str.strip, hours.split("-"))
                    )

                    shows.append(show)

        return shows

    def get_duration(self, movie, selector):
        duration_text = self.get_text(movie, selector).split(" ")[0]
        return int(duration_text) if duration_text.isdigit() else None

    def parse_movie(self, movie):
        source = "Cinema La Plata"
        title = self.get_text(movie, ".page-title")
        genres = self.get_text(movie, "#ctl00_cph_lblGenero").split(", ")
        languages = self.get_text(movie, "#ctl00_cph_lblIdioma").split(", ")
        origins = self.get_text(movie, "#ctl00_cph_lblPaisOrigen").split(", ")
        duration = self.get_duration(movie, "#ctl00_cph_lblDuracion")
        director = self.get_text(movie, "#ctl00_cph_lblDirector")
        actors = self.get_text(movie, "#ctl00_cph_lblActores").split(", ")
        rated = self.get_text(movie, "#ctl00_cph_lblCalificacion")
        synopsis = self.get_text(movie, "#ctl00_cph_lblSinopsis")
        trailer = movie.select_one(".embed-responsive-item").attrs.get("src")
        shows = self.get_shows(movie)
        distributor = None
        realeased = len(shows) != 0

        movie = Movie(
            source=source,
            title=title,
            genres=genres,
            languages=languages,
            origins=origins,
            duration=duration,
            director=director,
            rated=rated,
            actors=actors,
            synopsis=synopsis,
            trailer=trailer,
            shows=shows,
            distributor=distributor,
            realeased=realeased
        )

        self.parsed_movies.append(movie)

    def run(self):
        response = requests.get(self.link)
        html = response.text
        movie = BeautifulSoup(html, 'html.parser')

        return self.parse_movie(movie)


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


def main():
    future_releases = get_movies(FUTURE_RELEASES_URL)
    billboard = get_movies(BILLBOARD_URL)

    movies = future_releases + billboard

    movies_json = Movie.schema().dump(movies, many=True)
    print(json.dumps(movies_json, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    main()
