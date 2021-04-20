import json
import logging

from bs4 import BeautifulSoup
import requests


def scrap(url, filename):
    response = requests.get(url, headers={"User-Agent": ""})
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    try:
        json_ld = soup.select_one("script[type='application/ld+json']")
    except Exception as e:
        logging.error("JSON-LD NOT FOUND")
        raise e

    json_text = json_ld.string.replace("\n", "")
    movie = json.loads(json_text, strict=False)

    logging.info(f"Scraped {url}. Writing...")

    with open(filename, "w") as file:
        file.write(json.dumps(movie))
