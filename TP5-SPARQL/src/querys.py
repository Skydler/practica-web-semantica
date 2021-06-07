TWSS_ACTORS_NAMES = """
    SELECT ?name
    WHERE {{
        ?actor a ns1:Actor ; ns1:Name ?name
    }}
    """

DBPEDIA_ACTORS_WAS_DIRECTED_BY_OSCAR_WINNER = """
    PREFIX tmp: <http://tmp.org#>
    CONSTRUCT {{
        ?actor tmp:wasDirectedByOscarWinner ?director.
        ?actor tmp:name ?actorName.
    }}
    WHERE {{
        SELECT DISTINCT ?actor ?director ?actorName
        WHERE {{
            ?movie rdf:type dbo:Film.
            ?movie dbo:starring ?actor.
            ?actor rdfs:label ?actorName.
            ?movie dbo:director ?director.
            ?oscarAward dbp:wikiPageUsesTemplate dbt:Academy_Awards.
            ?director dbo:award ?oscarAward.
            FILTER regex(?actorName, {actors_regex}, "i").
            FILTER((LANGMATCHES(LANG(?actorName), "en")) ||
                   (LANGMATCHES(LANG(?actorName), "es")))
        }}
    }}
    """

WIKIDATA_ACTORS_WAS_DIRECTED_BY_OSCAR_WINNER = """
    PREFIX tmp: <http://tmp.org#>
    CONSTRUCT {{
        ?actor tmp:wasDirectedByOscarWinner ?director.
        ?actor tmp:name ?actorName.
    }}
    WHERE {{
        SELECT DISTINCT ?actor ?director ?actorName
        WHERE {{
            ?movie wdt:P31 wd:Q11424 ; wdt:P57 ?director.
            ?director wdt:P166 wd:Q19020.
            ?movie wdt:P161 ?actor.
            ?actor rdfs:label ?actorName.
            FILTER regex(?actorName, {actors_regex}, "i").
            FILTER((LANGMATCHES(LANG(?actorName), "en")) ||
                   (LANGMATCHES(LANG(?actorName), "es")))
      }}
    }}
    """

COMBINE_REMOTE_AND_LOCAL_ACTORS = """
    PREFIX tmp: <http://tmp.org#>
    CONSTRUCT {
        ?twss_actor :wasDirectedByOscarWinner ?remote_director
    }
    WHERE {
        # Extract remote info.
        ?remote_actor tmp:wasDirectedByOscarWinner ?remote_director.
        ?remote_actor tmp:name ?remote_actor_name.
        # Extract local info.
        ?twss_actor a ns1:Actor ; ns1:Name ?twss_actor_name.
        # Match local and remote actors by name.
        FILTER regex(?remote_actor_name, ?twss_actor_name, "i")
    }
    """

TWSS_PERSONS_NAMES = """
    SELECT ?name
    WHERE {{
        ?person a ns1:Person ; ns1:Name ?name
    }}
    """

DBPEDIA_PERSONS = """
    CONSTRUCT {{
        ?person ?property ?object
    }}
    WHERE {{
        SELECT ?person ?property ?object
        WHERE {{
            ?person rdf:type dbo:Person.
            ?person foaf:name ?name.
            ?person ?property ?object.
            FILTER regex(?name, "{persons_regex}", "i")
        }}
    }}
    """

WIKIDATA_PERSONS = """
    CONSTRUCT {{
        ?person ?property ?object
    }}
    WHERE {{
        SELECT DISTINCT ?person ?property ?object
        WHERE {{
            ?person wdt:P31 wd:Q5.
            ?person wdt:P1559 ?name.
            ?person ?property ?object.
            FILTER regex(?name, "{persons_regex}", "i")
        }}
    }}
    """
