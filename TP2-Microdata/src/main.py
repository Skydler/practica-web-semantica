import argparse
import json
import logging
from threading import Thread

from db.repository import MovieRepository
from parsers.ecartelera import EcarteleraParser
from parsers.imdb import ImdbParser
from parsers.metacritic import MetacriticParser
from parsers.tomatoes import RottenTomatoesParser
from pathlib import Path
from scrapers.jsonld import scrap


SITES = {
    "rotten_tomatoes": {
        "url": "https://www.rottentomatoes.com/m/wonder_woman_1984",
        "parser": RottenTomatoesParser
    },
    "imdb": {
        "url": "https://www.imdb.com/title/tt7126948/",
        "parser": ImdbParser
    },
    "metacritic": {
        "url": "https://www.metacritic.com/movie/wonder-woman-1984",
        "parser": MetacriticParser
    },
    "ecartelera": {
        "url": "https://www.ecartelera.com/peliculas/wonder-woman-1984",
        "parser": EcarteleraParser
    }
}

DATA_ROOT = Path.cwd().parent / "data"

MERGE_FILE = DATA_ROOT / "movies.json"


def filename(site_name):
    return DATA_ROOT / f"{site_name}.json"


def scrap_sites():
    logging.info("Scraping movies . . .")

    threads = [
        Thread(
            target=scrap,
            args=(site_data['url'], filename(site_name))
        )
        for site_name, site_data in SITES.items()
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


def parse_movies():
    movies = []
    for site_name, site_data in SITES.items():
        logging.info(f"Parsing {site_name} movies")

        with open(filename(site_name)) as file:
            serialized_movie = json.load(file)

        parser = site_data['parser']

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
        scrap_sites()

    logging.info("Parsing movies . . .")
    movies = parse_movies()

    logging.info("Merging movies . . .")
    repository = MovieRepository(saving_path=MERGE_FILE)
    repository.add(movies)
    repository.save()

    logging.info("Testing . . .")
    try:
        repository.read(MERGE_FILE)
    except Exception:
        logging.error("The merged movies are corrupt", exc_info=True)
    else:
        logging.info("Succesfully merged movies")


if __name__ == '__main__':
    main()
