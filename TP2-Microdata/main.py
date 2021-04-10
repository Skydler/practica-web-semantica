from bs4 import BeautifulSoup
import json
import requests


URLS = [
    "https://www.rottentomatoes.com/m/wonder_woman_1984",
    "https://www.imdb.com/title/tt7126948/",
    "https://www.metacritic.com/movie/wonder-woman-1984",
    "https://www.ecartelera.com/peliculas/wonder-woman-1984"
]


class Movie:
    def __init__(self):
        self.movie = {}

    def merge(self, versions):
        pass


def scrap(url):
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
    return movie


if __name__ == '__main__':
    movie_versions = [scrap(url) for url in URLS]

    with open("./data.json", "w") as file:
        file.write(json.dumps(movie_versions))

    # with open("./data.json", "r") as file:
    #     movie_versions = json.loads(file.read())

    movie = Movie()
    movie.merge(movie_versions)
    print(movie.movie)
