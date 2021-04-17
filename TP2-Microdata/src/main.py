from bs4 import BeautifulSoup
from merger import Movie
import threading
import json
import requests


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

    print(f"Scraped {source}. Writing...")

    with open(f"../data/{source}.json", "w") as file:
        file.write(json.dumps(movie))


def normalize_movies():
    # parsers = ["TomatoParser", "IMDBParser", "..."]  # Should be clasess
    # normalized_versions = [parser.run() for parser in parsers]
    normalized_versions = []
    return normalized_versions


def main():

    threads = [threading.Thread(target=scrap, args=(url, source))
               for url, source in URLS]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    normalized_versions = normalize_movies()
    movie = Movie()
    movie.merge(normalized_versions)


if __name__ == '__main__':
    main()
