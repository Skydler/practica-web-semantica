import argparse
import logging

from constant import LINKS_FILE
from links_generator import write_links
from ontology_enricher import enrich_base_graph


def main():
    # Init arguments parser
    parser = argparse.ArgumentParser()

    parser.add_argument("-v", "--verbose", action="store_true")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-l", "--links", action="store_true")
    group.add_argument("-e", "--enriching", nargs=2)

    args = parser.parse_args()

    # Init logger
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    # Evaluate arguments
    if args.links or not LINKS_FILE.exists():
        logging.info("Writing links.ttl file . . .")
        write_links()
        logging.info(f"Links file written: {LINKS_FILE}")

    if paths := args.enriching:
        # logging.info("Reading actors from link dataset")
        graph = enrich_base_graph(*paths)
        print(graph.serialize(format="turtle").decode("utf-8"))


if __name__ == "__main__":
    main()
