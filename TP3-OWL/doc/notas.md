# Notas
En este informe se tratan algunos de los temas más interesantes que nos surgieron durante la producción del trabajo.

[TOC]

# Respondiendo las preguntas del enunciado

*Esta sección representa al archivo **respuestas.txt** que se especifica en el enunciado.*

### ¿Qué ventajas supone que hubiese obtenido si en los trabajos anteriores contaba con la información descrita en OWL?
Creemos que hubiera sido mucho más facil de procesar ya que hay herramientas como **Protégé** que nos permiten importar los datos de una forma más sencilla y automatizada. Además, como los datos están pensados para ser consumidos publicamente no tendríamos que preocuparnos por hacer el scrapeo de las páginas (contando con que el scrapeo puede variar conforme las modificaciones que presente la página en el tiempo). También, gracias al manejo de recursos a través de URIs la posibilidad de que la obtención de los datos se dificulte se minimiza en gran medida. Y en caso de que el recurso representado por una URI se modifique, esto no genera un gran problema para la estructura de datos, ya que al ser de tipo gráfo presenta una gran flexibilidad.

Esta flexibilidad sin embargo puede traer ciertas desventajas, por ejemplo durante el desarrollo notamos que en ningún momento se hace un control de los tipos ni de la información que se introduce en el gráfo, a pesar de especificarle un rango y dominio. Aún así, consideramos que esta falta de estructura es inherente a la gran dificultad que existe para representar los datos debido a su variabilidad y múltiple interpretación. Problema para el cúal todavía no encontramos solución y venimos arrastrando desde los anteriores TPs.

 ### ¿Qué ventajas tiene utilizar vocabularios existentes en lugar de crear los propios?

 Principalmente nos facilita la nomenclatura de conceptos y nos permite "estandarizar" la forma de referirnos a un determinado recurso. Consideramos que es un intento natural de solucionar el problema planteado de la gran variabilidad y múltiple interpretación de los datos, el cual busca ponerle un único nombre y en un conjunto selecto de idiomas a un determinado concepto.

Como comentario adicional de esta parte, opinamos que en ninguno de los vocabularios que vimos se opta por documentar con mayor profundidad el significado de las palabras que se definen. Creemos que esto es un problema, ya que en varias situaciones nos encontramos imaginando como pudieron haber interpretado ciertas palabras los desarrolladores de los lenguajes y evaluando si esa palabra se aplicaba a **nuestra** interpretación de esa palabra.

### ¿Utilizó solamente clases y propiedades de un único vocabulario?

No, utilizamos varios vocabularios. Principalmente partimos de DBpedia para la mayoría de los atributos relacionados con peliculas y las relaciones con los actores, autores, directores, etc. No requerimos usar FOAF para la representación de las personas. Por otra parte el vocabulario FaBiO nos sirvió bastante para representar las reviews. Adicionalmente utilizamos una pequeña parte de Schema.org para representar los ratings de las peliculas.

Si bien la mayoría de los datos representados en los anteriores trabajos se basaron en la representación de Schema.org decidimos que la ontología en OWL no nos convencía por tener muchas discrepancias con la forma de representación que necesitabamos. Un poco de esto se vió reflejado en preguntas en el foro.

### ¿Que impacto hubiese tenido al momento de almacenar la información obtenida el contar con un modelo como OWL?
Siguiendo con lo mencionado en la primer respuesta, brinda mucha más flexibilidad a la hora de cargar los datos y el hecho de contar con diferentes vocabularios desarrollados por otras personas nos permiten describir los conceptos desde un punto de vista más genérico y estandarizado.

### ¿Qué diferencia hay entre utilizar un modelo de objetos para integrar la información que obtuvo (como hizo anteriormente) con utilizar tripletas?

Principalmente se encuentra la diferencia frente a situaciones en las que se ignora la cardinalidad de los elementos. También se resuelve de forma más directa la posibilidad de tener campos opcionales. Como se comentó ya, la flexibilidad de los gráfos también permite realizar merges entre los diferentes atributos creando relaciones que en objetos podrían llegar a ser mucho más complejas. Por otra parte esto involucra un menor grado de control sobre los datos y sus tipos.

### ¿Cuán dificil es generar archivos OWL en otros formatos (por ejemplo N3, RDF/XML) a partir de la información que tiene? Y con su scrapper.

Para realizar la deserialización y serialización de los datos utilizamos Python RDFlib, esta librería acepta una cantidad considerable de formatos en los que se puede expresar un archivo OWL. Nos sorprendió la sencillez con la que se puede modificar el formato con el cual se importa y exportan los datos. Solo con el pasaje de un parámetro este asunto queda resuelto.

```python
serialized_graph = graph.serialize(format="turtle").decode("utf-8")
```
