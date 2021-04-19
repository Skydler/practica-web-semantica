import argparse
import json
import logging
import threading
import requests

from bs4 import BeautifulSoup
from db.repository import MovieRepository
from parsers.imdb import ImdbParser
from parsers.tomatoes import RottenTomatoesParser
from parsers.metacritic import MetacriticParser
from parsers.ecartelera import EcarteleraParser


URLS = [
    ("https://www.rottentomatoes.com/m/wonder_woman_1984", "rotten_tomatoes"),
    ("https://www.imdb.com/title/tt7126948/", "imdb"),
    ("https://www.metacritic.com/movie/wonder-woman-1984", "metacritic"),
    ("https://www.ecartelera.com/peliculas/wonder-woman-1984", "ecartelera")
]


def scrap(url, source):
    response = requests.get(url, headers={"User-Agent": ""})
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    try:
        json_ld = soup.select_one("script[type='application/ld+json']")
    except Exception as e:
        print("JSON-LD NOT FOUND")
        raise e

    json_text = json_ld.string.replace("\n", "")
    movie = json.loads(json_text, strict=False)

    logging.info(f"Scraped {source}. Writing...")

    with open(f"../data/{source}.json", "w") as file:
        file.write(json.dumps(movie))


def normalize_movies():
    # TODO: Unify in a dictionary with its respective file name
    parsers = [
        (RottenTomatoesParser, "rotten_tomatoes"),
        (ImdbParser, "imdb"),
        (MetacriticParser, "metacritic"),
        (EcarteleraParser, "ecartelera"),
    ]
    movies = []
    for parser, source in parsers:
        logging.info(f"Parsing {source} movies")

        with open(f"../data/{source}.json") as file:
            serialized_movie = json.load(file)

        movie = parser(serialized_movie).run()
        movies.append(movie)
        logging.debug(movie)

    return movies


def main():
    # Init parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--offline", action="store_true")
    parser.add_argument("-v", "--verbose", action="store_true")

    args = parser.parse_args()

    # Init logger
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    if not args.offline:
        logging.info("Scraping movies . . .")

        threads = [threading.Thread(target=scrap, args=(url, source))
                   for url, source in URLS]

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

    logging.info("Parsing movies . . .")
    movies = normalize_movies()

    logging.info("Merging movies . . .")
    repository = MovieRepository(saving_path='../data/movies.json')
    repository.add(movies)
    repository.save()

    logging.info("Testing . . .")
    try:
        repository.read('../data/movies.json')
    except Exception:
        logging.error("The merged movies are corrupt", exc_info=True)
    else:
        logging.info("Succesfully merged movies")


if __name__ == '__main__':
    main()
