from selenium import webdriver
from scrapy.selector import Selector
from selenium.common.exceptions import NoSuchElementException
from model import Show, Movie
from datetime import datetime
import json

DOMAIN = "https://www.cinepolis.com.ar"
FUTURE_RELEASES_URL = f"{DOMAIN}/proximos-estrenos"
browser = webdriver.Chrome(executable_path="./chromedriver")
browser.implicitly_wait(2)


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
    def __init__(self, link, parsed_movies):
        self.link = link
        self.parsed_movies = parsed_movies

    def run(self):
        browser.get(self.link)
        self.parse_movie()

    def parse_movie(self):
        fields = {}
        fields.update(self.get_title())
        fields.update(self.get_technical_fields())
        fields.update(self.get_trailer())
        fields.update(self.get_synopsis())
        fields.update(self.get_shows())

        self.clean_fields(fields)

        movie = Movie(
            source="cinépolis",
            title=fields.get("title"),
            genres=fields.get("genero"),
            origins=fields.get("origen"),
            duration=fields.get("duracion"),
            director=fields.get('director'),
            rated=fields.get('calificacion'),
            actors=fields.get("actores"),
            synopsis=fields.get("sinopsis"),
            trailer=fields.get("trailer"),
            distributor=fields.get("distribuidora"),
            languages=fields.get("lenguages"),
            shows=fields.get("shows"),
            released=fields.get("shows") is not None
        )
        self.parsed_movies.append(movie)

    def get_title(self):
        title = browser.find_element_by_css_selector(
            ".title > * > .title-text").text
        return {"title": title}

    def get_technical_fields(self):
        pass

    def get_trailer(self):
        trailer = None
        try:
            trailer = browser.find_element_by_css_selector(
                ".embed-responsive-item")
            trailer = trailer.get_attribute("src")
        except NoSuchElementException:
            print("Trailer not found for this movie")

        return {"trailer": trailer}

    def get_synopsis(self):
        pass

    def get_shows(self):
        pass

    def clean_fields(self, fields):
        if duration := fields.get("duracion") is not None:
            duration_text = duration.split(" ")[0]
            duration = int(duration_text) if duration_text.isdigit() else None
            fields.update(duracion=duration)

        if genres := fields.get('genero') is not None:
            genres = genres.split(", ")
            fields.update(genero=genres)

        if origins := fields.get('origen') is not None:
            origins = origins.split(", ")
            fields.update(origen=origins)

        if actors := fields.get('actores') is not None:
            actors = actors.split(", ")
            fields.update(actores=actors)

    def make_movie(self, fields):
        pass


class BillboardParser(MovieParser):
    def __init__(self, link, parsed_movies):
        super().__init__(link, parse_movies)

    def get_technical_fields(self):
        html = browser.find_element_by_xpath(
            "//*[@id='tecnicos']").get_attribute("innerHTML")

        fields_content = Selector(text=html).xpath("//p/text()").getall()
        fields_content = [field.strip(': \n')
                          for field in fields_content if field.strip()]

        fields_name = Selector(text=html).xpath("//p/strong/text()").getall()
        fields_name = map(normalize, fields_name)

        return dict(zip(fields_name, fields_content))

    def get_room_shows(self, room, cine, date):
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
                cine=cine,
                time=self.get_time(date, hour)
            )

    def get_time(self, date, time):
        year, month, day, *_ = date.timetuple()
        hour, minute = map(int, time.split(':'))
        return datetime(year, month, day, hour, minute)

    def get_location_shows(self, location, date):
        cine = location.find_element_by_css_selector(
            ".panel-title > button").text

        rooms = location.find_elements_by_css_selector(
            ".movie-showtimes-component-combination")

        room_shows = []
        for room in rooms:
            for show in self.get_room_shows(room, cine, date):
                show.cine = cine
                room_shows.append(show)

        return room_shows

    def get_shows(self):
        days = browser.find_elements_by_css_selector(
            ".showtimes-filter-component-dates > ul > li > button")

        shows = []
        for day in days:
            day.click()
            date_attr = day.get_attribute("value")
            date = datetime.strptime(date_attr, "%Y-%m-%d")

            locations = browser.find_elements_by_css_selector(
                ".accordion > .card")

            day_shows = []
            for location in locations:
                day_shows += self.get_location_shows(location, date)

            shows += day_shows

        return shows


class FutureReleaseParser(MovieParser):
    def __init__(self, link, parsed_movies):
        super().__init__(link, parse_movies)

    def get_technical_fields(self):
        data = browser.find_element_by_css_selector("p").text
        fields = {}
        for field in data.split("\n"):
            key, value = field.split(": ")
            key = normalize(key)
            fields.update({key: value})

        return fields

    def get_synopsis(self):
        synopsis = browser.find_element_by_xpath("//div[h4 and hr][1]").text
        synopsis = synopsis[9:]  # 9 chars to eliminate "Sinopsis\n"
        return {"sinopsis": synopsis}

    def get_shows(self):
        return {"shows": None}


def parse_movies(links, future=False):
    parsed_movies = []
    Parser = FutureReleaseParser if future else BillboardParser

    for link in links:
        Parser(link, parsed_movies).run()

    return parsed_movies


def get_current_movies():
    browser.get(DOMAIN)
    movies = browser.find_elements_by_xpath(
        "//div[contains(@class, 'movie-grid')]/div/a")
    movies_links = [m.get_attribute('href') for m in movies]
    return parse_movies(movies_links)


def get_future_releases():
    browser.get(FUTURE_RELEASES_URL)
    # Select all future releases
    # TODO: This works but we might want to select the specific option for all
    #       movies and not the first one
    browser.find_element_by_css_selector("select > option").click()
    xpath_selector = "//a[contains(@class, 'movie-thumb')] \
        [not(div[contains(@class, 'movie-thumb-ribbon')])]"
    movies = browser.find_elements_by_xpath(xpath_selector)
    movies_links = [m.get_attribute('href') for m in movies]
    return parse_movies(movies_links, future=True)


def main():
    # billboard = get_current_movies()
    billboard = []
    future_releases = get_future_releases()
    movies = billboard + future_releases
    movies_json = Movie.schema().dump(movies, many=True)

    browser.close()

    with open("../data/cinepolis.json", "w") as file:
        file.write(json.dumps(movies_json, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    main()
