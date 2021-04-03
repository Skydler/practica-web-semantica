from selenium import webdriver
from scrapy.selector import Selector
from selenium.common.exceptions import NoSuchElementException
from model import Show, Movie
from datetime import datetime
import json

DOMAIN = "https://www.cinepolis.com.ar"
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
        super(MovieParser, self).__init__()
        self.link = link
        self.parsed_movies = parsed_movies

    def get_technical_fields(self):
        html = browser.find_element_by_xpath(
            self.THECNIC_XPATH).get_attribute("innerHTML")

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
            ".showtimes-filter-component-dates > ul > li > button"
        )

        shows = []
        for day in days:
            day.click()
            date_attr = day.get_attribute("value")
            date = datetime.strptime(date_attr, "%Y-%m-%d")

            locations = browser.find_elements_by_css_selector(
                ".accordion > .card"
            )

            day_shows = []
            for location in locations:
                day_shows += self.get_location_shows(location, date)

            shows += day_shows

        return shows

    def parse_movie(self):
        fields = self.get_technical_fields()
        shows = self.get_shows()
        released = len(shows) != 0
        trailer = None
        try:
            trailer = browser.find_element_by_css_selector(
                ".embed-responsive-item")
            trailer = trailer.get_attribute("src")
        except NoSuchElementException:
            print("Trailer not found for this movie")

        # TODO: all this data fetching should be in a
        # try/except in case of None values
        duration_text = fields["duracion"].split(
            " ")[0] if "duracion" in fields else ""
        duration = int(duration_text) if duration_text.isdigit() else None
        genres = fields.get('genero').split(", ") if 'genero' in fields else []
        languages = []  # Cinepolis doesn't specify languages
        origins = fields.get('origen').split(
            ", ") if 'origen' in fields else []
        actors = fields.get('actores').split(
            ", ") if 'actores' in fields else []

        synopsis = self.get_synopsis()

        movie = Movie(
            source="cinépolis",
            title=browser.find_element_by_css_selector(
                ".title > * > .title-text").text,
            genres=genres,
            languages=languages,
            origins=origins,
            duration=duration,
            director=fields.get('director'),
            rated=fields.get('calificacion'),
            actors=actors,
            synopsis=synopsis,
            trailer=trailer,
            shows=shows,
            distributor=fields.get('distribuidora'),
            released=released
        )
        self.parsed_movies.append(movie)

    def run(self):
        browser.get(self.link)
        self.parse_movie()


class FutureReleaseParser(MovieParser):
    THECNIC_XPATH = "//div[h4 and hr][2]"

    def get_synopsis(self):
        selector = browser.find_element_by_xpath("//div[h4 and hr][1]")
        lines = selector.text.split("\n")
        synopsis = "".join(lines[1:]) if len(lines) > 1 else ""

        return synopsis


class BillboardParser(MovieParser):
    THECNIC_XPATH = "//*[@id='tecnicos']"

    def get_synopsis(self):
        selector = browser.find_element_by_css_selector("#sinopsis")

        return selector.text


def parse_movies(parsers):
    parsed_movies = []

    for parser, links in parsers.items():
        for link in links:
            parser(link, parsed_movies).run()

    return parsed_movies


def get_movies(link, browser):
    browser.get(DOMAIN)

    parsers = {
        BillboardParser: browser.find_elements_by_xpath(
            "//div[contains(@class, 'movie-grid')]/div/a"),

        FutureReleaseParser: browser.find_elements_by_xpath(
            "//*[@id='upcoming-releases']//*[contains(@class, 'slick-list')]//\
            *[contains(@class, 'slick-slide') and not(contains(@class, \
            'slick-cloned'))]//a[not(div[(contains(@class, 'ribbon'))])]")
    }

    for parser, movies in parsers.items():
        parsers[parser] = [movie.get_attribute('href') for movie in movies]

    return parse_movies(parsers)


def main():
    try:
        movies = get_movies(DOMAIN, browser)
    finally:
        browser.close()

    movies_json = Movie.schema().dump(movies, many=True)

    with open("../data/cinepolis.json", "w") as file:
        file.write(json.dumps(movies_json, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    main()
