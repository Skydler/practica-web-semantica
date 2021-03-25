from bs4 import BeautifulSoup
from model import Funcion, Pelicula
from threading import Thread
import requests
import json

PARSED_MOVIES = []


def parse_movie(link):
    movie = requests.get(link).text
    soup = BeautifulSoup(movie, 'html.parser')

    titulo = soup.select_one(".page-title").text.strip()
    genero = [soup.select_one("#ctl00_cph_lblGenero").text.strip()]
    idioma = [soup.select_one("#ctl00_cph_lblIdioma").text.strip()]
    origen = [soup.select_one("#ctl00_cph_lblPaisOrigen").text.strip()]
    duracion = int(soup.select_one(
        "#ctl00_cph_lblDuracion").text.strip().split(" ")[0])
    director = soup.select_one("#ctl00_cph_lblDirector").text.strip()
    calificacion = soup.select_one("#ctl00_cph_lblCalificacion").text.strip()
    actores = soup.select_one("#ctl00_cph_lblActores").text.strip().split(", ")
    calificacion = soup.select_one("#ctl00_cph_lblCalificacion").text.strip()
    sinopsis = soup.select_one("#ctl00_cph_lblSinopsis").text.strip()
    trailer = soup.select_one(".embed-responsive-item").attrs.get("src")

    peli = Pelicula(
        cine_fuente="Cinema La Plata",
        titulo=titulo,
        genero=genero,
        idioma=idioma,
        origen=origen,
        duracion=duracion,
        director=director,
        calificacion=calificacion,
        actores=actores,
        sinopsis=sinopsis,
        trailer=trailer,
        funciones=None,
        distribuidora=None
    )
    PARSED_MOVIES.append(peli)


def main():
    billboard = requests.get(
        "http://www.cinemalaplata.com/cartelera.aspx").text
    soup = BeautifulSoup(billboard, 'html.parser')

    movies = soup.find_all('div', class_="page-container singlepost")
    links = [f"http://www.cinemalaplata.com/{movie.h4.strong.a['href']}"
             for movie in movies]

    threads = [Thread(target=parse_movie, args=(link,)) for link in links]
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    a = Pelicula.schema().dump(PARSED_MOVIES, many=True)
    print(json.dumps(a, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    main()
