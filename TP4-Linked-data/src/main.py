import argparse
import logging
import re

from concurrent.futures import ThreadPoolExecutor
from constant import DBPEDIA_DATA_URI, LINKS_FILE
from constant import NAMESPACES, MAX_REQUESTS, ORIGINAL_DATASET_FILE
from db.repository import OwlMovieRepository
from rdflib import Graph, RDF
from urllib.parse import urljoin


def actors(graph):
    return graph.triples((None, RDF.type, NAMESPACES['dbo'].Actor))


def get_actors_uris(graph):
    return [triplet[0] for triplet in actors(graph)]


def get_dbpedia_actor(twss_actor_uri):
    dbpedia_actor_name = to_dbpedia_actor_name(twss_actor_uri)

    dbpedia_actor_data_uri = urljoin(
        DBPEDIA_DATA_URI, f"{dbpedia_actor_name}.ttl")

    logging.debug(f"Request to {dbpedia_actor_data_uri}")
    return OwlMovieRepository.read(dbpedia_actor_data_uri)


def to_dbpedia_actor_name(twss_actor_uri):
    resource, actor_name = str(twss_actor_uri).split("#")

    return '_'.join(camel_case_split(actor_name))


def camel_case_split(text):
    return re.sub('([a-z])([A-Z])', r'\1 \2', text).split()


def get_dbpedia_actors(twss_actors_uris):
    with ThreadPoolExecutor(max_workers=MAX_REQUESTS) as executor:
        actors_graphs = list(executor.map(
            get_dbpedia_actor,
            twss_actors_uris
        ))

    return actors_graphs


def add_same_as_triplet(twss_actor_uri, graph):
    dbpedia_actor_name = to_dbpedia_actor_name(twss_actor_uri)

    same_as = (twss_actor_uri,
               NAMESPACES['owl'].sameAs,
               NAMESPACES['dbr'][dbpedia_actor_name])

    graph.add(same_as)


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
            add_same_as_triplet(twss_actor_uri, links_graph)

    OwlMovieRepository.write(LINKS_FILE, links_graph, namespaces=NAMESPACES)


def main():
    # Init arguments parser
    parser = argparse.ArgumentParser()

    parser.add_argument("-v", "--verbose", action="store_true")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-l", "--links", action="store_true")
    group.add_argument("-e", "--enriching", action="store_true")

    args = parser.parse_args()

    # Init logger
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    # Evaluate arguments
    if args.links or not LINKS_FILE.exists():
        logging.info("Writing links.ttl file . . .")
        write_links()
        logging.info(f"Links file written: {LINKS_FILE}")

    if args.enriching:
        logging.error("[= to-do =]")


if __name__ == '__main__':
    main()
