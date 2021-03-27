from bs4 import BeautifulSoup
from model import Show, Movie
from urllib.parse import urljoin
from selenium import webdriver
from threading import Thread
import json

DOMAIN = "https://www.cinepolis.com.ar"


class MovieParser(Thread):

    def __init__(self, link, parsed_movies):
        super(MovieParser, self).__init__()
        self.link = link
        self.parsed_movies = parsed_movies

    def run(self):
        pass


def parse_movies(links):
    parsed_movies = []

    threads = [MovieParser(link, parsed_movies) for link in links]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    return parsed_movies


def get_movies(link, browser):
    html = browser.get(DOMAIN).page_source
    # The webriver is needed to get the page source because the movies in the
    # homepage are dinamically added too.
    soup = BeautifulSoup(html, 'html.parser')

    movies = soup.select(".featured-movies-grid-view-component a")
    links = [urljoin(DOMAIN, movie.h4.strong.a['href']) for movie in movies]

    return parse_movies(links)


def main():
    browser = webdriver.Chrome(executable_path="./chromedriver")
    billboard = get_movies(DOMAIN, browser)
    # future_releases = get_movies(FUTURE_RELEASES_URL, browser)
    movies = billboard  # + future_releases

    movies_json = Movie.schema().dump(movies, many=True)

    with open("../data/cinepolis.json", "w") as file:
        file.write(json.dumps(movies_json, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    main()
