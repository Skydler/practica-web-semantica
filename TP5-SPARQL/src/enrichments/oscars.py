import logging

from SPARQLWrapper import SPARQLWrapper
from rdflib import Graph

from constants import (
    DBPEDIA_SPARQL_URL,
    MAX_ACTORS_PER_REQUEST,
    NAMESPACES,
    OSCAR_WINNERS_CACHE_FILE,
    OSCAR_WINNERS_FILE,
    TWSS_RESOURCES_URI,
    WIKIDATA_SPARQL_URL,
)
from db.repository import OwlMovieRepository
from enrichments.querys import (
    COMBINE_REMOTE_AND_LOCAL_ACTORS,
    DBPEDIA_ACTORS_WAS_DIRECTED_BY_OSCAR_WINNER,
    TWSS_ACTORS_NAMES,
    WIKIDATA_ACTORS_WAS_DIRECTED_BY_OSCAR_WINNER,
)


def get_twss_resources_graph():
    logging.info(f"Request to {TWSS_RESOURCES_URI}")

    return OwlMovieRepository.read(TWSS_RESOURCES_URI)


def get_oscar_winners_graph(twss_resources):
    logging.info("Looking for actors who were directed by Oscar winners.")

    if OSCAR_WINNERS_CACHE_FILE.exists():
        logging.info("Reading Oscar winners from cache")

        oscar_winners_graph = OwlMovieRepository.read(source=OSCAR_WINNERS_CACHE_FILE)
    else:
        logging.info("Reading Oscar winners from web")

        oscar_winners_graph = build_oscar_winners_graph(twss_resources)

        logging.info(
            f"Writing the cache file of Oscar winners "
            f"in {OSCAR_WINNERS_CACHE_FILE}."
        )

        OwlMovieRepository.write(
            path_file=OSCAR_WINNERS_CACHE_FILE,
            graph=oscar_winners_graph,
            namespaces=NAMESPACES,
        )

    return oscar_winners_graph


def build_oscar_winners_graph(twss_resources):
    results = Graph()
    actors_names = get_actors_names(twss_resources)

    for chunk_of_names in chunks(actors_names, MAX_ACTORS_PER_REQUEST):
        actors_regex = f'"({"|".join(chunk_of_names)})"'

        logging.info("Request to DBpedia sparql")

        dbpedia_results = get_sparql_query(
            source=DBPEDIA_SPARQL_URL,
            query=DBPEDIA_ACTORS_WAS_DIRECTED_BY_OSCAR_WINNER.format(
                actors_regex=actors_regex
            ),
        )

        logging.info(f"DBpedia results: {len(dbpedia_results)}")

        logging.info("Request to Wikidata sparql")

        wikidata_results = get_sparql_query(
            source=WIKIDATA_SPARQL_URL,
            query=WIKIDATA_ACTORS_WAS_DIRECTED_BY_OSCAR_WINNER.format(
                actors_regex=actors_regex
            ),
        )

        logging.info(f"Wikidata results: {len(wikidata_results)}")

        results += dbpedia_results + wikidata_results

    return results


def chunks(items, chunk_size):
    total_chunks = range(0, len(items), chunk_size)

    for chunk_number in total_chunks:
        start = chunk_number
        end = chunk_number + chunk_size
        yield items[start:end]


def get_actors_names(twss_graph):
    actors_names = twss_graph.query(TWSS_ACTORS_NAMES)
    cleaned_actors_names = [name[0].toPython() for name in actors_names]

    return cleaned_actors_names


def get_sparql_query(source, query):
    sparql = SPARQLWrapper(source)

    sparql.setQuery(query)
    results = sparql.query().convert()

    return results


def main():
    logging.info("Reading graphs")

    twss_resources = get_twss_resources_graph()
    oscar_winners_graph = get_oscar_winners_graph(twss_resources)

    logging.info("Matching remote actors with locals")

    merged_graph = twss_resources + oscar_winners_graph
    result = merged_graph.query(COMBINE_REMOTE_AND_LOCAL_ACTORS)

    logging.info(f"Done! Writing graph in {OSCAR_WINNERS_FILE}")

    OwlMovieRepository.write(
        path_file=OSCAR_WINNERS_FILE, graph=result.graph, namespaces=NAMESPACES
    )


if __name__ == "__main__":
    main()
