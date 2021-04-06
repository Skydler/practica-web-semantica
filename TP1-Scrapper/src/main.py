import argparse
import logging
from time import time

from db.repository import MovieRepository
from pathlib import Path
from scrapers import cinemalaplata, cinepolis


ROOT = Path.cwd().parent / "data"

CINEPOLIS_FILE = ROOT / "cinepolis.json"
CINEMA_LA_PLATA_FILE = ROOT / "cinemalaplata.json"
MERGE_FILE = ROOT / "movies.json"


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
    repository = MovieRepository(MERGE_FILE)
    repository.add(movies)
    repository.save()


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
        cinepolis_movies = MovieRepository.read(CINEPOLIS_FILE)
        cinema_la_plata_movies = MovieRepository.read(CINEMA_LA_PLATA_FILE)
    else:
        cinepolis_movies = scrap_cinepolis_movies()
        MovieRepository.write(CINEPOLIS_FILE, cinepolis_movies)

        cinema_la_plata_movies = scrap_cinema_la_plata_movies()
        MovieRepository.write(CINEMA_LA_PLATA_FILE, cinema_la_plata_movies)

    movies = cinepolis_movies + cinema_la_plata_movies
    merge_movies(movies)


if __name__ == '__main__':
    main()
