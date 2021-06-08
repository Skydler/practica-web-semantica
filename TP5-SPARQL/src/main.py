import argparse
import logging

from constants import (
    TWSS_RESOURCES_URI,
    OSCAR_WINNERS_FILE,
    EXTENDED_PERSONS_FILE,
    ENRICHED_GRAPH_FILE,
    NAMESPACES,
)
from db.repository import OwlMovieRepository
from enrichments import oscars, person_enricher
from rdflib import Graph


GRAPH_LOCATIONS_TO_ENRICH = [
    TWSS_RESOURCES_URI,
    OSCAR_WINNERS_FILE,
    EXTENDED_PERSONS_FILE,
]


def build_enrichment_graph():
    enriched_graph = Graph()

    for graph_location in GRAPH_LOCATIONS_TO_ENRICH:
        enriched_graph += OwlMovieRepository.read(graph_location, namespaces=NAMESPACES)

    return enriched_graph


def main():
    # Init arguments parser
    parser = argparse.ArgumentParser()

    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("-o", "--offline", action="store_true")

    args = parser.parse_args()

    # Init logger
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    # Evaluate arguments
    if not args.offline:
        logging.info("Running Oscar script")
        oscars.main()
        logging.info("Running person enricher script")
        person_enricher.main()

    # Merge enrichments
    logging.info("Enriching the graph")
    enriched_graph = build_enrichment_graph()

    OwlMovieRepository.write(
        path_file=ENRICHED_GRAPH_FILE, graph=enriched_graph, namespaces=NAMESPACES
    )

    logging.info(f"Done! Enriched graph saved in {ENRICHED_GRAPH_FILE}")


if __name__ == "__main__":
    main()
