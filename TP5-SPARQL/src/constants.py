from pathlib import Path
from rdflib import Namespace, OWL
from urllib.parse import urljoin

# Requests
MAX_ACTORS_PER_REQUEST = 400


# URIs
BASE_TWSS_URI = "https://raw.githubusercontent.com/Skydler/practica-web-semantica/main/TP3-OWL/data/"
TWSS_RESOURCES_URI = "https://raw.githubusercontent.com/Skydler/practica-web-semantica/main/TP4-Linked-data/data/dataset-enriquecido.ttl"

BASE_DBPEDIA_URI = "http://dbpedia.org/"
DBPEDIA_RESOURCE_URI = urljoin(BASE_DBPEDIA_URI, "resource/")

BASE_WIKIDATA_URI = "http://www.wikidata.org/"

DBPEDIA_SPARQL_URL = "http://dbpedia.org/sparql"
WIKIDATA_SPARQL_URL = "https://query.wikidata.org/sparql"


# Namespaces defined with the PREFIX as key and its URI as value
NAMESPACES = {
    "twss": Namespace(urljoin(BASE_TWSS_URI, "movie.ttl#", allow_fragments=False)),
    "dbo": Namespace(urljoin(BASE_DBPEDIA_URI, "ontology/")),
    "dbr": Namespace(urljoin(BASE_DBPEDIA_URI, "resource/")),
    "dbp": Namespace(urljoin(BASE_DBPEDIA_URI, "property/")),
    "foaf": Namespace("http://xmlns.com/foaf/0.1/"),
    "owl": OWL,  # Necessary to avoid automatic renaming provided by rdflib
    "wd": Namespace(urljoin(BASE_WIKIDATA_URI, "entity/")),
}


# File paths
DATA_DIR = Path.cwd().parent / "data"

OSCAR_WINNERS_CACHE_FILE = DATA_DIR / "cache-oscars-winners.ttl"
OSCAR_WINNERS_FILE = DATA_DIR / "oscars-winners.ttl"
ENRICHED_GRAPH_FILE = DATA_DIR / "enriched-graph.ttl"
WIKIDATA_PERSONS_FILE = DATA_DIR / "wikidata_persons.ttl"
DBPEDIA_PERSONS_FILE = DATA_DIR / "dbpedia_persons.ttl"
EXTENDED_PERSONS_FILE = DATA_DIR / "extended_persons.ttl"
