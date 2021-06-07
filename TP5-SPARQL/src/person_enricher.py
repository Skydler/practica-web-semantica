import logging

from SPARQLWrapper import RDFXML, SPARQLWrapper

from constants import NAMESPACES, TWSS_RESOURCES_URI
from db.repository import OwlMovieRepository
from querys import TWSS_PERSONS_NAMES, DBPEDIA_PERSONS, WIKIDATA_PERSONS


def get_persons_names(twss_graph):
    names = twss_graph.query(TWSS_PERSONS_NAMES)
    clean_names = [triplet[0] for triplet in names]
    return clean_names


def query_dbpedia_persons(names):
    DBPEDIA_URL = "http://dbpedia.org/sparql"
    logging.info(f"Request to {DBPEDIA_URL}")
    persons_regex = "(" + "|".join(names) + ")"

    sparql = SPARQLWrapper(DBPEDIA_URL, returnFormat=RDFXML)
    sparql.setQuery(DBPEDIA_PERSONS.format(persons_regex=persons_regex))
    results = sparql.queryAndConvert()

    OwlMovieRepository.write(
        path_file="../data/dbpedia_persons.ttl", graph=results, namespaces=NAMESPACES
    )
    return results


def query_wikidata_persons(names):
    WIKIDATA_URL = "https://query.wikidata.org/sparql"
    logging.info(f"Request to {WIKIDATA_URL}")
    persons_regex = "(" + "|".join(names) + ")"

    sparql = SPARQLWrapper(WIKIDATA_URL, returnFormat=RDFXML)
    sparql.setQuery(WIKIDATA_PERSONS.format(persons_regex=persons_regex))
    results = sparql.queryAndConvert()

    OwlMovieRepository.write(
        path_file="../data/wikidata_persons.ttl",
        graph=results,
        namespaces=NAMESPACES,
    )
    return results


def merge_graphs(source, remote):
    pass


def main():
    # Init logger
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    logging.info(f"Request to {TWSS_RESOURCES_URI}")
    twss_graph = OwlMovieRepository.read(TWSS_RESOURCES_URI)
    names = get_persons_names(twss_graph)

    dbpedia_graph = query_dbpedia_persons(names)
    wiki_graph = query_wikidata_persons(names)
    remote_persons_graph = dbpedia_graph + wiki_graph
    merged_graph = merge_graphs(twss_graph, remote_persons_graph)


if __name__ == "__main__":
    main()
