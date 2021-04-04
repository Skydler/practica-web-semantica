import cinemalaplata
import cinepolis
import json
import logging
import merger

from model import Movie
from pathlib import Path


ROOT = Path.cwd().parent / "data"

CINEPOLIS_FILE = ROOT / "cinepolis.json"
CINEMA_LA_PLATA_FILE = ROOT / "cinemalaplata.json"
MERGE_FILE = ROOT / "movies.json"


def save(filename, movies):
    movies_json = Movie.schema().dump(movies, many=True)

    with open(filename, "w") as file:
        file.write(json.dumps(movies_json, indent=4, ensure_ascii=False))


def main():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    logging.debug("Scraping Cinepolis")

    cinepolis_movies = []

    try:
        cinepolis_movies = cinepolis.scrap()
    except Exception:
        logging.error(
            "An error occurred while scraping Cinepolis", exc_info=True)

    logging.debug("Scraping Cinema La Plata")

    cinema_la_plata_movies = []

    try:
        cinema_la_plata_movies = cinemalaplata.scrap()
    except Exception:
        logging.error(
            "An error occurred while scraping Cinema La Plata", exc_info=True)

    logging.debug("Merging the movies")

    movies = cinepolis_movies + cinema_la_plata_movies
    merged_movies = []

    try:
        merged_movies = merger.merge(movies)
    except Exception:
        logging.error(
            "An error ocurred while merging the movies", exc_info=True)

    logging.debug(f"Saving data in {ROOT}")

    save(CINEPOLIS_FILE, cinepolis_movies)
    logging.debug(f"Cinepolis: {CINEPOLIS_FILE}")

    save(CINEMA_LA_PLATA_FILE, cinema_la_plata_movies)
    logging.debug(f"Cinema La Plata: {CINEMA_LA_PLATA_FILE}")

    save(MERGE_FILE, merged_movies)
    logging.debug(f"Merge: {MERGE_FILE}")


if __name__ == '__main__':
    main()
