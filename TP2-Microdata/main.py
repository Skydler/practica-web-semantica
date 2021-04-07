from bs4 import BeautifulSoup
import json
import requests


URLS = [
    "https://www.rottentomatoes.com/m/wonder_woman_1984",
    "https://www.imdb.com/title/tt7126948/",
    "https://www.metacritic.com/movie/wonder-woman-1984",
    "https://www.ecartelera.com/peliculas/wonder-woman-1984"
]


def scrap(url):
    print(url)

    headers = {
        "User-Agent": ""
    }

    response = requests.get(url, headers=headers)
    html = response.text

    soup = BeautifulSoup(html, 'html.parser')

    import pdb
    pdb.set_trace()

    if (json_ld := soup.select_one("script[type='application/ld+json']")):
        movie = json.loads(json_ld.text)

        print(movie)
    else:
        print("Json ld not found")


if __name__ == '__main__':
    # for url in URLS:
    #    scrap(url[2])
    scrap(URLS[2])
