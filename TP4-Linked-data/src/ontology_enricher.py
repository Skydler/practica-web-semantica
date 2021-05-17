from concurrent.futures import ThreadPoolExecutor
import logging

from rdflib import OWL
from rdflib.term import Literal

from constant import MAX_REQUESTS, NAMESPACES
from db.repository import OwlMovieRepository


def get_remote_actor(actor_uri):
    logging.debug(f"Request to {actor_uri}")
    actor_graph = OwlMovieRepository.read(actor_uri)
    return actor_graph


def clean_occupation(ocupation_literal):
    ocupation = ocupation_literal.toPython()
    striped_ocup = ocupation.replace("http://dbpedia.org/resource/", "")
    literal_ocup = Literal(striped_ocup, lang="en")
    return literal_ocup


def clean_objects(prop_objects):
    occupations = prop_objects["occupations"]
    # Filters occupations="" and clears resource indirections
    clean_ocups = [clean_occupation(ocup) for ocup in occupations if ocup]
    prop_objects["occupations"] = clean_ocups


def get_objects_from_predicates(actor, predicates):
    objects = {
        key: list(actor.objects(predicate=pred)) for key, pred in predicates.items()
    }
    clean_objects(objects)
    return objects


def enrich_base_graph(base_dataset, link_dataset):
    linked_graph = OwlMovieRepository.read(link_dataset)
    base_graph = OwlMovieRepository.read(base_dataset)

    predicates = {
        "birth_date": NAMESPACES["dbp"].birthDate,
        "occupations": NAMESPACES["dbp"].occupation,
        # FOAF Namespace of RDFLIB dosn't have "isPrimaryTopicOf" property
        "wikipedia_page": NAMESPACES["foaf"].isPrimaryTopicOf,
    }

    subject_objects = linked_graph.subject_objects(OWL.sameAs)
    local_actors_uri, remote_actors_uri = zip(*subject_objects)

    with ThreadPoolExecutor(max_workers=MAX_REQUESTS) as executor:
        remote_actors = list(executor.map(get_remote_actor, remote_actors_uri))

    for local_actor, remote_actor in zip(local_actors_uri, remote_actors):
        prop_objects = get_objects_from_predicates(remote_actor, predicates)
        for key, objects in prop_objects.items():
            for obj in objects:
                base_graph.add((local_actor, predicates[key], obj))

    return base_graph
