from datetime import datetime
import logging

from models.model import Show, Movie
from pathlib import Path
from scrapy.selector import Selector
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from typing import List
from utils import mapers


DOMAIN = "https://www.cinepolis.com.ar"
FUTURE_RELEASES_URL = f"{DOMAIN}/proximos-estrenos"

WEBDRIVER_ROOT_PATH = Path.cwd().parent / "bin"
WEBDRIVER_EXECUTOR_PATH = WEBDRIVER_ROOT_PATH / "chromedriver"


def normalize(s):
    replacements = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
    )

    for a, b in replacements:
        s = s.lower().replace(a, b)

    return s


class MovieParser:
    def __init__(self, link, parsed_movies, browser):
        self.link = link
        self.parsed_movies = parsed_movies
        self.browser = browser

    def run(self):
        self.browser.get(self.link)
        self.parse_movie()

    def parse_movie(self):
        fields = {}
        fields.update(self.get_title())
        fields.update(self.get_technical_fields())
        fields.update(self.get_trailer())
        fields.update(self.get_synopsis())
        fields.update(self.get_shows())

        fields = self.clean_fields(fields)

        origin = fields.get("origen")
        trailer_url = fields.get("trailer")

        movie = Movie(
            name=fields.get("title"),
            genres=fields.get("genero"),
            origins=[origin] if origin else [],
            duration=fields.get("duracion"),
            directors=mapers.to_person(fields.get('director')),
            content_rating=fields.get('calificacion'),
            actors=mapers.to_person(fields.get("actores")),
            description=fields.get("sinopsis"),
            video=mapers.to_video(trailer_url),
            languages=[],
            shows=fields.get("shows"),
            released=fields.get("shows") != [],
            schema_type='Movie',
            source_urls=[self.link],
            production_company=None,
            aggregated_ratings=[],
            reviews=[],
            images=[],
            characters=[],
            authors=[],
            keywords=[],
            events=[],
        )
        self.parsed_movies.append(movie)

    def get_title(self):
        title = self.browser.find_element_by_css_selector(
            ".title > * > .title-text").text
        return {"title": title}

    def _get_tech_fields_html(self):
        pass

    def get_technical_fields(self):
        html = self._get_tech_fields_html()

        fields_content = Selector(text=html).xpath("//p/text()").getall()
        fields_content = [field.strip(': \n')
                          for field in fields_content if field.strip()]

        fields_name = Selector(text=html).xpath("//p/strong/text()").getall()
        fields_name = map(normalize, fields_name)

        return dict(zip(fields_name, fields_content))

    def get_trailer(self):
        trailer = None
        try:
            trailer = self.browser.find_element_by_css_selector(
                ".embed-responsive-item")
            trailer = trailer.get_attribute("src")
        except NoSuchElementException:
            logging.warning("Trailer not found for this movie")

        return {"trailer": trailer}

    def get_synopsis(self):
        pass

    def get_shows(self):
        pass

    def clean_fields(self, fields):
        if (duration := fields.get("duracion")) is not None:
            duration_text = duration.split(" ")[0]
            duration = int(duration_text) if duration_text.isdigit() else None
            fields.update(duracion=duration)

        if (genres := fields.get('genero')) is not None:
            genres = [genre for genre in genres.split(", ") if genre != ""]
            fields.update(genero=genres)
        else:
            fields.update(genero=[])

        if (origins := fields.get('origen')) is not None:
            origins = origins.split(", ")
            fields.update(origen=origins)
        else:
            fields.update(origen=[])

        if (actors := fields.get('actores')) is not None:
            actors = actors.strip('.').split(", ")
            fields.update(actores=actors)
        else:
            fields.update(actores=[])

        if (directors := fields.get('director')) is not None:
            directors = directors.strip('.').split(", ")
            fields.update(director=directors)
        else:
            fields.update(director=[])

        return fields

    def make_movie(self, fields):
        pass


class BillboardParser(MovieParser):
    def __init__(self, link, parsed_movies, browser):
        super().__init__(link, parsed_movies, browser)

    def get_room_shows(self, room, cinema, date):
        room_description = room.find_element_by_css_selector(
            "small").get_attribute("textContent")
        room_description = [element.strip()
                            for element in room_description.split("•")]

        hall, _format, language = room_description
        title = f"{hall} - {_format}"

        movie_hours = room.find_elements_by_css_selector(
            ".btn-detail-showtime")
        movie_hours = [hour.get_attribute(
            "textContent").strip() for hour in movie_hours]

        for hour in movie_hours:
            yield Show(
                room=title,
                language=language,
                cinema=cinema,
                time=self.get_time(date, hour)
            )

    def get_time(self, date, time):
        year, month, day, *_ = date.timetuple()
        hour, minute = map(int, time.split(':'))
        return datetime(year, month, day, hour, minute)

    def get_location_shows(self, location, date):
        cinema = location.find_element_by_css_selector(
            ".panel-title > button").text

        rooms = location.find_elements_by_css_selector(
            ".movie-showtimes-component-combination")

        room_shows = []
        for room in rooms:
            for show in self.get_room_shows(room, cinema, date):
                show.cinema = cinema
                room_shows.append(show)

        return room_shows

    def get_shows(self):
        days = self.browser.find_elements_by_css_selector(
            ".showtimes-filter-component-dates > ul > li > button")

        shows = []
        for day in days:
            day.click()
            date_attr = day.get_attribute("value")
            date = datetime.strptime(date_attr, "%Y-%m-%d")

            locations = self.browser.find_elements_by_css_selector(
                ".accordion > .card")

            day_shows = []
            for location in locations:
                day_shows += self.get_location_shows(location, date)

            shows += day_shows

        return {"shows": shows}

    def get_synopsis(self):
        synopsis = self.browser.find_element_by_css_selector("#sinopsis").text
        return {"sinopsis": synopsis}

    def _get_tech_fields_html(self):
        node = self.browser.find_element_by_xpath("//*[@id='tecnicos']")
        return node.get_attribute("innerHTML")


class FutureReleaseParser(MovieParser):
    def __init__(self, link, parsed_movies, browser):
        super().__init__(link, parsed_movies, browser)

    def _get_tech_fields_html(self):
        node = self.browser.find_element_by_xpath("//div[h4 and hr][2]")
        return node.get_attribute("innerHTML")

    def get_synopsis(self):
        synopsis = self.browser.find_element_by_xpath(
            "//div[h4 and hr][1]").text
        synopsis = synopsis[9:]  # 9 chars to eliminate "Sinopsis\n"
        return {"sinopsis": synopsis}

    def get_shows(self):
        return {"shows": []}


def parse_movies(links, browser, future=False):
    Parser = FutureReleaseParser if future else BillboardParser
    parsed_movies = []
    for link in links:
        Parser(link, parsed_movies, browser).run()

    return parsed_movies


def get_current_movies(browser):
    browser.get(DOMAIN)
    movies = browser.find_elements_by_xpath(
        "//div[contains(@class, 'movie-grid')]/div/a")
    movies_links = [m.get_attribute('href') for m in movies]
    return parse_movies(movies_links, browser)


def get_future_releases(browser):
    browser.get(FUTURE_RELEASES_URL)
    browser.find_element_by_css_selector("select > option").click()
    xpath_selector = "//a[contains(@class, 'movie-thumb')] \
        [not(div[contains(@class, 'movie-thumb-ribbon')])]"
    movies = browser.find_elements_by_xpath(xpath_selector)
    movies_links = [m.get_attribute('href') for m in movies]
    return parse_movies(movies_links, browser, future=True)


def scrap() -> List[Movie]:
    movies = []

    if not WEBDRIVER_EXECUTOR_PATH.exists():
        logging.error(f"Not found chromedriver in {WEBDRIVER_EXECUTOR_PATH}")
        return movies

    browser = webdriver.Chrome(
        executable_path=WEBDRIVER_EXECUTOR_PATH
    )
    browser.implicitly_wait(2)

    try:
        billboard = get_current_movies(browser)
        future_releases = get_future_releases(browser)
        movies = billboard + future_releases
    except Exception as e:
        import traceback
        traceback.print_exc()
        breakpoint()
    finally:
        browser.close()
        return movies
