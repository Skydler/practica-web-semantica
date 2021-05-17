from pathlib import Path
from rdflib import Namespace
from urllib.parse import urljoin


# URIs
BASE_TWSS_URI = "https://raw.githubusercontent.com/Skydler/practica-web-semantica/main/TP3-OWL/data/"

BASE_DBPEDIA_URI = "http://dbpedia.org/"
DBPEDIA_DATA_URI = urljoin(BASE_DBPEDIA_URI, "data/")


# Namespaces defined with the PREFIX as key and its URI as value
NAMESPACES = {
    "twss": Namespace(urljoin(BASE_TWSS_URI, "movie.ttl#", allow_fragments=False)),
    "dbo": Namespace(urljoin(BASE_DBPEDIA_URI, "ontology/")),
    "dbr": Namespace(urljoin(BASE_DBPEDIA_URI, "resource/")),
    "dbp": Namespace(urljoin(BASE_DBPEDIA_URI, "property/")),
    "foaf": Namespace("http://xmlns.com/foaf/0.1/"),
}


# File paths
DATA_DIR = Path.cwd().parent / "data"

ORIGINAL_DATASET_FILE = DATA_DIR / "dataset-original.ttl"
LINKS_FILE = DATA_DIR / "links.ttl"


# Requests config
MAX_REQUESTS = 40
