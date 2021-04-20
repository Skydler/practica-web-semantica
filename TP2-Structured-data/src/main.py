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


SITES = [
    {
        "url": "https://www.rottentomatoes.com/m/wonder_woman_1984",
        "parser": RottenTomatoesParser,
        "filename": "ww-rotten-tomatoes"
    },
    {
        "url": "https://www.imdb.com/title/tt7126948/",
        "parser": ImdbParser,
        "filename": "ww-imdb"
    },
    {
        "url": "https://www.metacritic.com/movie/wonder-woman-1984",
        "parser": MetacriticParser,
        "filename": "ww-metacritic"
    },
    {
        "url": "https://www.ecartelera.com/peliculas/wonder-woman-1984",
        "parser": EcarteleraParser,
        "filename": "ww-ecartelera"
    },
]

EXTRA_SITES = [
    {
        "url": "https://www.rottentomatoes.com/m/tenet",
        "parser": RottenTomatoesParser,
        "filename": "tenet-rotten-tomatoes"
    },
    {
        "url": "https://www.metacritic.com/movie/tenet",
        "parser": MetacriticParser,
        "filename": "tenet-metacritic"
    },
    {
        "url": "https://www.imdb.com/title/tt6723592/",
        "parser": ImdbParser,
        "filename": "tenet-imdb"
    },
    {
        "url": "https://www.ecartelera.com/peliculas/tenet/",
        "parser": EcarteleraParser,
        "filename": "tenet-ecartelera"
    },
]

DATA_ROOT = Path.cwd().parent / "data"
SCRAP_ROOT = DATA_ROOT / "scrap"

MERGE_FILE = DATA_ROOT / "movies.json"


def path(filename):
    return SCRAP_ROOT / f"{filename}.json"


def scrap_sites():
    logging.info("Scraping movies . . .")

    threads = [
        Thread(
            target=scrap,
            args=(site['url'], path(site['filename']))
        )
        for site in SITES
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


def parse_movies():
    movies = []
    for site in SITES:
        logging.info(f"Parsing {site['url']} movies")

        with open(path(site['filename'])) as file:
            serialized_movie = json.load(file)

        parser = site['parser']

        movie = parser(serialized_movie).run()

        movies.append(movie)
        logging.debug(movie)

    return movies


def main():
    # Init parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--offline", action="store_true")
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("-e", "--extra", action="store_true")

    args = parser.parse_args()

    # Init logger
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    if args.extra:
        SITES.extend(EXTRA_SITES)

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
        logging.error("Invalid types, unable to load model", exc_info=True)
    else:
        logging.info("Succesfully merged movies")


if __name__ == '__main__':
    main()
