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


def get_actor_graph(actor_uri):
    actor_name = dbpedia_actor_name(actor_uri)

    actor_data_uri = urljoin(DBPEDIA_DATA_URI, f"{actor_name}.ttl")
    logging.debug(f"Request to {actor_data_uri}")

    return OwlMovieRepository.read(actor_data_uri)


def dbpedia_actor_name(actor_uri):
    resource, name = str(actor_uri).split("#")

    return '_'.join(camel_case_split(name))


def camel_case_split(text):
    return re.sub('([a-z])([A-Z])', r'\1 \2', text).split()


def get_actors_graphs(actors_uris):
    with ThreadPoolExecutor(max_workers=MAX_REQUESTS) as executor:
        actors_graphs = list(executor.map(
            get_actor_graph,
            actors_uris
        ))

    return actors_graphs


def add_same_as_triplet(actor_uri, graph):
    actor_name = dbpedia_actor_name(actor_uri)

    same_as = (actor_uri,
               NAMESPACES['owl'].sameAs,
               NAMESPACES['dbr'][actor_name])

    graph.add(same_as)


def write_links():
    graph = OwlMovieRepository.read(ORIGINAL_DATASET_FILE)

    actors_uris = get_actors_uris(graph)
    actors_graphs = get_actors_graphs(actors_uris)

    links_graph = Graph()

    for prefix, uri in NAMESPACES.items():
        links_graph.bind(prefix, uri)

    for actor_graph, actor_uri in zip(actors_graphs, actors_uris):
        actor_name = dbpedia_actor_name(actor_uri)

        if len(actor_graph) == 0:
            logging.error(f"Not found owl:sameAs for {actor_name}")
        else:
            logging.debug(f"Found owl:sameAs for {actor_name}")

            add_same_as_triplet(actor_uri, links_graph)

    OwlMovieRepository.write(LINKS_FILE, links_graph)


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
