import argparse
import cinemalaplata
import cinepolis
import json
import logging
from merger import MergeStrategy

from model import Movie
from pathlib import Path
from time import time


ROOT = Path.cwd().parent / "data"

CINEPOLIS_FILE = ROOT / "cinepolis.json"
CINEMA_LA_PLATA_FILE = ROOT / "cinemalaplata.json"
MERGE_FILE = ROOT / "movies.json"


def read(filename):
    with open(filename, "r") as file:
        json_string = file.read()
    movie_objects = Movie.schema().loads(json_string, many=True)
    return movie_objects


def save(filename, movies):
    movies_json = Movie.schema().dump(movies, many=True)

    with open(filename, "w") as file:
        file.write(json.dumps(movies_json, indent=4, ensure_ascii=False))


def log(function):
    operation = function.__name__

    def decorate(*args):
        logging.info(f"Running {operation}")

        movies = []

        start_time = time()

        try:
            movies = function(*args)
        except Exception:
            logging.error(f"An error ocurred in {operation}", exc_info=True)
        finally:
            duration = time() - start_time
            logging.info(f"Finish {operation} took {duration:.2f}s")

            return movies

    return decorate


@log
def scrap_cinepolis_movies():
    return cinepolis.scrap()


@log
def scrap_cinema_la_plata_movies():
    return cinemalaplata.scrap()


@log
def merge_movies(movies):
    merger = MergeStrategy()
    merger.merge(movies)
    return merger.to_list()


def main():
    # Init parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("-o", "--offline", action="store_true")

    args = parser.parse_args()

    # Init logger
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    # Run scrapers
    if args.offline:
        cinepolis_movies = read(CINEPOLIS_FILE)
        cinema_la_plata_movies = read(CINEMA_LA_PLATA_FILE)
    else:
        cinepolis_movies = scrap_cinepolis_movies()
        cinema_la_plata_movies = scrap_cinema_la_plata_movies()

    movies = cinepolis_movies + cinema_la_plata_movies
    merged_movies = merge_movies(movies)

    # Save data
    logging.info(f"Saving data in {ROOT}")

    save(CINEPOLIS_FILE, cinepolis_movies)
    logging.info(f"Cinepolis: {CINEPOLIS_FILE}")

    save(CINEMA_LA_PLATA_FILE, cinema_la_plata_movies)
    logging.info(f"Cinema La Plata: {CINEMA_LA_PLATA_FILE}")

    save(MERGE_FILE, merged_movies)
    logging.info(f"Merge: {MERGE_FILE}")


if __name__ == '__main__':
    main()
