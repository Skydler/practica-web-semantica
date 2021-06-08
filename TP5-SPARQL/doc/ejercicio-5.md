# Ejercicio 5

## Consultas sobre los directores ganadores del Oscar

Para implementar esta parte, se realizaron 2 consultas `CONSTRUCT`, la cual arma un grafo temporal tanto para DBpedia, como para Wikidata:

```SPARQL
PREFIX tmp: <http://tmp.org#>
CONSTRUCT {
    ?actor tmp:wasDirectedByOscarWinner ?director.
    ?actor tmp:name ?actorName.
}
WHERE {
    SELECT DISTINCT ?actor ?director ?actorName
    WHERE {
        # Match movies
        ?movie rdf:type dbo:Film.
        # Match the actors of the movies
        ?movie dbo:starring ?actor.
        # Extract the labels of the actors
        ?actor rdfs:label ?actorName.
        # Match the directors of the movies
        ?movie dbo:director ?director.
        # Match the directors who won an Oscar
        ?oscarAward dbp:wikiPageUsesTemplate dbt:Academy_Awards.
        ?director dbo:award ?oscarAward.
        # Filter the actors by label (spanish and english)
        FILTER regex(?actorName, {actors_regex}, "i").
        FILTER (LANGMATCHES(LANG(?actorName), "en")) || (LANGMATCHES(LANG(?actorName), "es"))
    }
}
```

```SPARQL
PREFIX tmp: <http://tmp.org#>
CONSTRUCT {
    ?actor tmp:wasDirectedByOscarWinner ?director.
    ?actor tmp:name ?actorName.
}
WHERE {
    SELECT DISTINCT ?actor ?director ?actorName
    WHERE {
        # Match the directors of the movies
        ?movie wdt:P31 wd:Q11424 ; wdt:P57 ?director.
        # Match the directors who won an Oscar
        ?director wdt:P166 wd:Q19020.
        # Match the actors of the movies
        ?movie wdt:P161 ?actor.
        # Extract the labels of the actors
        ?actor rdfs:label ?actorName.
        # Filter the actors by label (spanish and english)
        FILTER regex(?actorName, {actors_regex}, "i").
        FILTER((LANGMATCHES(LANG(?actorName), "en")) || (LANGMATCHES(LANG(?actorName), "es")))
  }
}
```

- Se utiliza `DISTINCT` porque puede haber resultados repetidos en el caso de que un actor haya sido dirigido por un director que ganó un Oscar en más de una película.
- La variable {actors_regex} representa la siguiente regex: `(actor_name_1|actor_name_2|..)`, esta misma es seteada por Python en ejecución a medida que se leen los actores de nuestra base de conocimiento. La razón de utilizar un grupo de regex es para generar la menor cantidad de consultas posibles, ya que los motores de SPARQL ponen restricciones en su uso. La discusión más detallada se puede ver en el siguiente hilo del foro: https://asignaturas.info.unlp.edu.ar/mod/forum/discuss.php?d=204#p533 .

Al armar un subgrafo, esto nos permite manejar un cierto "polimorfismo" entre dbpedia y wikidata. Lo único que falta es relacionar cada actor de nuestra base de conocimiento con los resultados que obtuvimos anteriormente ¿Por qué? Porque recordamos que utilizamos regex para traer toda la información en la menor cantidad de consultas posibles, en cambio, si traíamos la información recorriendo cada actor en específico, podíamos relacionarlos de una forma más fácil, pero el costo era muy grande en términos de rendimiento. Por lo tanto, se combinaron ambos grafos obtenidos previamente y se realizó la siguiente consulta local mediante `rdflib`:

```SPARQL
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
```

Como podemos notar, la consulta genera el grafo que queremos como resultado. Para ello, se matchea el nombre de wikidata/dbpedia con el nombre del actor de nuestra base de conocimiento.

- Nota: En esta consulta queda claro el uso de "polimorfismo" entre dbpedia y wikidata a través del prefijo **tmp**.

## Respuestas

**¿Qué diferencias, ventajas y desventajas le encuentra al uso de SPARQL?**

Como diferencia al TP anterior, podemos notar que no tuvimos que usar dereferenciamiento en ningún caso, por lo tanto, esto es una ventaja de utilizar SPARQL, ya que al trabajar con pattern matching no se necesita ingresar uno por uno a cada archivo ttl y extraer la información.

Otra ventaja es que los motores de SPARQL generalmente están sobre base de datos (como en dbpedia/wikidata) y no sobre archivos de texto, esto permite que las consultas se ejecuten mucho más rápido. También SPARQL se asemeja mucho a SQL, por lo que el salto de aprendizaje de uno a otro es muy leve en términos de esfuerzo. 

También, a diferencia del TP anterior, SPARQL utiliza un paradigma declarativo, lo que refleja mucho mejor la información que queremos obtener frente a un paradigma imperativo que llevaría muchas más líneas de código.

Como desventaja notamos que los motores piden muchas restricciones sobre su uso, y se necesitan hacer algunas "estrategias" para ejecutar la información en el menor tiempo posible.

Otra desventaja que observamos fue la complejidad que se torna al usar la sentencia `OPTIONAL`, al ser una cláusula común en la Web Semántica (ya que es un mundo libre) consideramos que se podría implementar de otra forma, ya que hay consultas que están anidadas con optionals y se vuelven muy complicadas de entender. Si bien esto corre por el lado del programador, nos pareció un punto para destacar

**Si utilizó alguna librería específica comente brevemente las ventajas que encontró, y cómo le ayudo en su solución.**

Utilizamos rdflib como en las anteriores entregas para guardar y actualizar nuestra base de conocimiento. Nos permitió abrir y manipular nuestros grafos de una forma más programática.

Para las consultas SPARQL utilizamos la librería **sparqlwrapper**, la cual permitió hacer las consultas a los motores SPARQL desde Python con mayor abstracción. Particularmente se encapsuló esta lógica en la siguiente función:

```python
def get_sparql_query(source, query):
    sparql = SPARQLWrapper(source)

    sparql.setQuery(query)
    results = sparql.query().convert()

    return results
```

