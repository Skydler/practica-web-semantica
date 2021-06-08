import logging

from SPARQLWrapper import RDFXML, SPARQLWrapper

from constants import (
    DBPEDIA_PERSONS_FILE,
    EXTENDED_PERSONS_FILE,
    NAMESPACES,
    TWSS_RESOURCES_URI,
    WIKIDATA_PERSONS_FILE,
)
from db.repository import OwlMovieRepository
from enrichments.querys import (
    COMBINE_REMOTE_AND_LOCAL_PERSONS,
    DBPEDIA_PERSONS,
    TWSS_PERSONS_NAMES,
    WIKIDATA_PERSONS,
)


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
        path_file=DBPEDIA_PERSONS_FILE, graph=results, namespaces=NAMESPACES
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
        path_file=WIKIDATA_PERSONS_FILE,
        graph=results,
        namespaces=NAMESPACES,
    )
    return results


def merge_graphs(source, remote):
    logging.info("Merging graphs")
    merged = source + remote
    result = merged.query(COMBINE_REMOTE_AND_LOCAL_PERSONS)
    return result.graph


def main():
    logging.info(f"Request to {TWSS_RESOURCES_URI}")
    twss_graph = OwlMovieRepository.read(TWSS_RESOURCES_URI)

    # Change this flag to use local data
    local = False

    if local:
        dbpedia_graph = OwlMovieRepository.read(DBPEDIA_PERSONS_FILE)
        wiki_graph = OwlMovieRepository.read(WIKIDATA_PERSONS_FILE)
    else:
        names = get_persons_names(twss_graph)
        logging.info("Querying remote persons")
        # Warining making too many requests on dbpedia server may block you
        dbpedia_graph = query_dbpedia_persons(names)
        wiki_graph = query_wikidata_persons(names)

    remote_persons_graph = dbpedia_graph + wiki_graph
    merged_graph = merge_graphs(twss_graph, remote_persons_graph)

    logging.info(f"Done! Writing graph in {EXTENDED_PERSONS_FILE}")

    OwlMovieRepository.write(
        path_file=EXTENDED_PERSONS_FILE,
        graph=merged_graph,
        namespaces=NAMESPACES,
    )


if __name__ == "__main__":
    main()
