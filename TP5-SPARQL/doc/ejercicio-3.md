# Ejercicio 3

A continuación se describen las siguientes consultas mediante SPARQL:

**a)** Obtener a los escritores que hayan nacido en una ciudad de Argentina. 

```SPARQL
SELECT DISTINCT ?writer WHERE {
    ?writer rdf:type dbo:Writer. 
    ?writer dbo:birthPlace / dbo:country dbr:Argentina.
}
```

El resultado se puede ver haciendo click en este [link](https://dbpedia.org/isparql/execute.html?query=SELECT%20DISTINCT%20%3Fwriter%20WHERE%20%7B%0A%20%20%20%20%3Fwriter%20rdf%3Atype%20dbo%3AWriter.%20%0A%20%20%20%20%3Fwriter%20dbo%3AbirthPlace%20%2F%20dbo%3Acountry%20dbr%3AArgentina.%0A%7D&endpoint=%2Fsparql&maxrows=50&timeout=&default-graph-uri=http%3A%2F%2Fdbpedia.org&view=1&amode=0&raw_iris=true).

**b)** Obtener a los escritores que hayan nacido en una ciudad de Uruguay.

```SPARQL
SELECT DISTINCT ?writer WHERE {
    ?writer rdf:type dbo:Writer. 
    ?writer dbo:birthPlace / dbo:country dbr:Uruguay.
}
```

El resultado se puede ver haciendo click en este [link](https://dbpedia.org/isparql/execute.html?query=SELECT%20DISTINCT%20%3Fwriter%20WHERE%20%7B%0A%20%20%20%20%3Fwriter%20rdf%3Atype%20dbo%3AWriter.%20%0A%20%20%20%20%3Fwriter%20dbo%3AbirthPlace%20%2F%20dbo%3Acountry%20dbr%3AUruguay.%0A%7D&endpoint=%2Fsparql&maxrows=50&timeout=&default-graph-uri=http%3A%2F%2Fdbpedia.org&view=1&amode=0&raw_iris=true). 

**c)** Utilizando el **keyword filter** (vea sección 6.3.2.6 del libro), obtener a los escritores que hayan nacido en una ciudad de Argentina o de Uruguay.

```SPARQL
SELECT DISTINCT ?writer WHERE {
    ?writer rdf:type dbo:Writer. 
    ?writer dbo:birthPlace / dbo:country ?country
    FILTER(?country = dbr:Argentina || ?country = dbr:Uruguay).
}
```

El resultado se puede ver haciendo click en este [link](https://dbpedia.org/isparql/execute.html?query=SELECT%20DISTINCT%20%3Fwriter%20%3Fcountry%20WHERE%20%7B%0A%20%20%20%20%3Fwriter%20rdf%3Atype%20dbo%3AWriter.%20%0A%20%20%20%20%3Fwriter%20dbo%3AbirthPlace%20%2F%20dbo%3Acountry%20%3Fcountry%0A%20%20%20%20FILTER(%3Fcountry%20%3D%20dbr%3AArgentina%20%7C%7C%20%3Fcountry%20%3D%20dbr%3AUruguay).%0A%7D&endpoint=%2Fsparql&maxrows=50&timeout=&default-graph-uri=http%3A%2F%2Fdbpedia.org&view=1&amode=0&raw_iris=true).

* Nota: Se proyectan los países para que sea más fácil la verificación de la unión.

**d)** Utilizando el **keyword union** (vea sección 6.3.2.6 del libro), obtener a los escritores que hayan nacido en una ciudad de Argentina o de Uruguay

```SPARQL
SELECT DISTINCT ?writer WHERE {
    { ?writer rdf:type dbo:Writer. 
      ?writer dbo:birthPlace / dbo:country dbr:Argentina. }
    UNION
    { ?writer rdf:type dbo:Writer. 
      ?writer dbo:birthPlace / dbo:country dbr:Uruguay.}
}
```

El resultado se puede ver haciendo click en este [link](https://dbpedia.org/isparql/execute.html?query=SELECT%20DISTINCT%20%3Fwriter%20WHERE%20%7B%0A%20%20%20%20%7B%20%3Fwriter%20rdf%3Atype%20dbo%3AWriter.%20%0A%20%20%20%20%20%20%3Fwriter%20dbo%3AbirthPlace%20%2F%20dbo%3Acountry%20dbr%3AArgentina.%20%7D%0A%20%20%20%20UNION%0A%20%20%20%20%7B%20%3Fwriter%20rdf%3Atype%20dbo%3AWriter.%20%0A%20%20%20%20%20%20%3Fwriter%20dbo%3AbirthPlace%20%2F%20dbo%3Acountry%20dbr%3AUruguay.%7D%0A%7D&endpoint=%2Fsparql&maxrows=50&timeout=&default-graph-uri=http%3A%2F%2Fdbpedia.org&view=1&amode=0&raw_iris=true).

**e)** ¿Qué diferencia hay entre c y d? ¿En cual se deben recuperar/analizar menor número de tripletas?

La diferencia es que en la **unión** se deben evaluar 2 conjuntos de tripletas y luego unirlas. Por lo tanto, haríamos 3 operaciones sobre el conjunto de tripletas. En cambio en el **filter** solo se aplica la condición del filtro una vez, por lo que a priori parece más eficiente, luego habrá que ver, porque quizás el motor de SPARQL aplica técnicas de optimización en la unión para equiparar los tiempos.

También la diferencia está en la sintaxis, quizás en este caso resulte redundante utilizar la unión, pero podemos tener querys más complicadas y simplemente con el operador UNION podemos unirlas, sin necesidad de "tocar" las querys que lo componen.

Por lo tanto, utilizar UNION o FILTER dependerá del caso y habrá que hacer un balance entre esfuerzo de programación y eficiencia para decidir cual es el más adecuado.

**f)** ¿Cuantos empleados tiene la compañía mas grande en dbpedia, y en que país está ubicada? (obtenga la lista de todas las compañías y los países donde están ubicadas ordenada de forma descendiente por numero de empleados)

```SPARQL
SELECT DISTINCT ?company ?country ?employees WHERE {
    ?company rdf:type dbo:Company ; dbo:numberOfEmployees ?employees.

    OPTIONAL { # DBO location -> Most priority
        ?company dbo:location / dbo:country ?country.
    }
    OPTIONAL { # DBP Location with Country as RDF type
        ?company dbp:locationCity / dbo:country ?country.
    }
    OPTIONAL { # DBP Location with Country as string
        VALUES (?dbpProperty) { (dbp:locationCountry) (dbp:hqLocationCountry) }
        ?company ?dbpProperty ?country.
    }
}
ORDER BY DESC(?employees)
```

La compañía más grande registrada en dbpedia es Ritek con 59003000 empleados y es de Taiwán.  El país no está registrado oficialmente en **dbo**. Sin embargo, si está registrado en **dbp**.

El resultado se puede ver haciendo click en este [link](https://dbpedia.org/isparql/execute.html?query=SELECT%20DISTINCT%20%3Fcompany%20%3Fcountry%20%3Femployees%20WHERE%20%7B%0A%20%20%20%20%3Fcompany%20rdf%3Atype%20dbo%3ACompany%20%3B%20dbo%3AnumberOfEmployees%20%3Femployees.%0A%0A%20%20%20%20OPTIONAL%20%7B%20%23%20DBO%20location%20-%3E%20Most%20priority%0A%20%20%20%20%20%20%20%20%3Fcompany%20dbo%3Alocation%20%2F%20dbo%3Acountry%20%3Fcountry.%0A%20%20%20%20%7D%0A%20%20%20%20OPTIONAL%20%7B%20%23%20DBP%20Location%20with%20Country%20as%20RDF%20type%0A%20%20%20%20%20%20%20%20%3Fcompany%20dbp%3AlocationCity%20%2F%20dbo%3Acountry%20%3Fcountry.%0A%20%20%20%20%7D%0A%20%20%20%20OPTIONAL%20%7B%20%23%20DBP%20Location%20with%20Country%20as%20string%0A%20%20%20%20%20%20%20%20VALUES%20(%3FdbpProperty)%20%7B%20(dbp%3AlocationCountry)%20(dbp%3AhqLocationCountry)%20%7D%0A%20%20%20%20%20%20%20%20%3Fcompany%20%3FdbpProperty%20%3Fcountry.%0A%20%20%20%20%7D%0A%7D%0AORDER%20BY%20DESC(%3Femployees)&endpoint=%2Fsparql&maxrows=50&timeout=&default-graph-uri=http%3A%2F%2Fdbpedia.org&view=1&amode=0&raw_iris=true).