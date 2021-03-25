from bs4 import BeautifulSoup
import requests


def main():
    billboard = requests.get(
        "http://www.cinemalaplata.com/cartelera.aspx").text
    soup = BeautifulSoup(billboard, 'html.parser')

    for link in soup.find_all(''):
        pass


if __name__ == "__main__":
    main()
