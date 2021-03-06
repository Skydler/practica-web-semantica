from concurrent.futures import ThreadPoolExecutor
import logging
import re
from urllib.parse import urljoin

from rdflib import Graph, RDF, OWL

from constant import (
    DBPEDIA_RESOURCE_URI,
    LINKS_FILE,
    MAX_REQUESTS,
    NAMESPACES,
    ORIGINAL_DATASET_FILE,
)
from db.repository import OwlMovieRepository


def actors(graph):
    return graph.triples((None, RDF.type, NAMESPACES["dbo"].Actor))


def get_actors_uris(graph):
    return [triplet[0] for triplet in actors(graph)]


def get_dbpedia_actor(twss_actor_uri):
    dbpedia_actor_name = to_dbpedia_actor_name(twss_actor_uri)
    dbpedia_actor_data_uri = urljoin(DBPEDIA_RESOURCE_URI, dbpedia_actor_name)
    logging.debug(f"Request to {dbpedia_actor_data_uri}")
    actor_graph = OwlMovieRepository.read(dbpedia_actor_data_uri)
    return actor_graph


def to_dbpedia_actor_name(twss_actor_uri):
    _, actor_name = str(twss_actor_uri).split("#")

    return "_".join(camel_case_split(actor_name))


def camel_case_split(text):
    return re.sub("([a-z])([A-Z])", r"\1 \2", text).split()


def get_dbpedia_actors(twss_actors_uris):
    with ThreadPoolExecutor(max_workers=MAX_REQUESTS) as executor:
        actors_graphs = list(executor.map(get_dbpedia_actor, twss_actors_uris))

    return actors_graphs


def get_dbpedia_actor_uri(actor_graph, dbpedia_actor_name):
    dbr = NAMESPACES["dbr"]

    if redirects := get_dbpedia_redirects(actor_graph):
        return redirects.pop()

    return dbr[dbpedia_actor_name]


def get_dbpedia_redirects(graph):
    dbo = NAMESPACES["dbo"]

    return list(graph.objects(predicate=dbo.wikiPageRedirects))


def write_links():
    twss_graph = OwlMovieRepository.read(ORIGINAL_DATASET_FILE)
    links_graph = Graph()

    twss_actors_uris = get_actors_uris(twss_graph)
    dbpedia_actors = get_dbpedia_actors(twss_actors_uris)

    for dbpedia_actor, twss_actor_uri in zip(dbpedia_actors, twss_actors_uris):
        dbpedia_actor_name = to_dbpedia_actor_name(twss_actor_uri)

        if len(dbpedia_actor) == 0:
            logging.error(f"Not found owl:sameAs for {dbpedia_actor_name}")
        else:
            logging.debug(f"Found owl:sameAs for dbpedia_{dbpedia_actor_name}")

            links_graph.add(
                (
                    twss_actor_uri,
                    OWL.sameAs,
                    get_dbpedia_actor_uri(dbpedia_actor, dbpedia_actor_name),
                )
            )

    OwlMovieRepository.write(LINKS_FILE, links_graph, namespaces=NAMESPACES)
