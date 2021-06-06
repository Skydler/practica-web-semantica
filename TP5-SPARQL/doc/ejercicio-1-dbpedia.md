
Lectura recomendada:
http://svn.aksw.org/papers/2013/SWJ_DBpedia/public.pdf

1. ¿Qué es dbpedia?

Dbpedia es un proyecto que se encarga de extraer la información disponible en Wikipedia para luego hacerla pública utilizando tecnologías de Web Semántica y Linked Data. Así, de esta forma se puede llegar a formar bases de conocimientos que permitan responder consultas expresivas e interesantes sobre los datos.

2. ¿De donde sale la información disponible en dbpedia?

La información es extraida de Wikipedia. El proyecto DBpedia se enfoca en construir una base de conocimiento de gran escala, orientada a multiples lenguajes. Esto lo logra obteniendo la información de artículos los cuales llegan a tener ediciones en hasta 111 lenguajes.

3. ¿Que partes de los artículos de Wikipedia se transforman en tripletas?

La mayor parte de los artículos de Wikipedia es compuesta por texto simple, sin embargo existe información que está representada con otros mecanísmos. Algunos de estos son fichas de información, categorías, imagenes, coordenadas geográficas, links a páginas externas, links de desambiguación, redirecciones y links a ediciones de Wikipedia en diferentes lenguajes.
Para realizar la extracción de toda esta información DBpedia posee un framework con varias etapas de extracción. Primero se obtienen las páginas de Wikipedia, luego se realiza un parseo de la información generando un Abstract Syntax Tree (AST) con los diferentes componentes de la página, a continuación se pasa el AST por varios mecanísmos de extracción especificos para los diferentes componentes de los artículos. Por último la información extraida se almacena en forma de tripletas en diferentes formatos para su posterior explotación semántica.

4. ¿Cual es el esquema de URIs que utiliza dbpedia?

Por cada artículo en Wikipedia se introducen varias URIs para representar los conceptos que aparecen en la página. Hasta 2011, DBpedia publicó las URIs bajo el dominio http://dbpedia.org. Los principales subdominios eran:
- http://dbpedia.org/resource/ : Con el prefijo **dbr** para representar los datos de los artículos.
- http://dbpedia.org/property/ : Con el prefijo **dbp** para representar las propiedades extraidas sin modificaciones de la *infobox* o ficha de información principal de la página.
- http://dbpedia.org/ontology/ : Con el prefijo **dbo** para representar la ontología de DBpedia

De esta forma, en caso de haber información adicional de un recurso en ediciones cuyo idioma fuera diferente al Inglés, solo se agregaría al recurso en cuestión en caso de existir una versión en Inglés linkeada a la correspondiente información adicional.

A partir de la versión 3.7 de DBpedia, se decidió que esta forma de procesar los datos omitía mucha información importante y se optó por generar dos tipos de datasets diferentes.
- *Localized data sets*: Contienen todas las cosas que están descriptas en un lenguaje determinado. Estos recursos pasarían en alojarse en URIs del tipo http://\<lang\>.dbpedia.org/resource/ y sus propiedades en http://\<lang\>.dbpedia.org/property/
- *Canonicalized data sets*: Contienen toda la información representada por las versiones en inglés de los artículos de Wikipedia. Estos recursos se identifican de la misma manera que en las versiones previas (http://dbpedia.org/resource/)


5. ¿Dado el articulo en Wikipedia de "National University of La Plata", como infiero la URL del recurso correspondiente en dbpedia? ¿Cuál sería para Argentina? ¿Y para Uruguay? (exprese su respuesta aprovechando el prefijo dbr:  para referirse a http://dbpedia.org/resource/)

Es posible inferir su correspondiente recurso en DBpedia dado el título del artículo. Esto es así dado que existe un mapeo uno a uno entre las páginas de Wikipedia y los recursos de DBpedia basados en el título.
De esta forma si el artículo correspondiente con la Universidad Nacional de La Plata en Wikipedia está representado por https://en.wikipedia.org/wiki/National_University_of_La_Plata en DBpedia estará representado por dbr:National_University_of_La_Plata

6. ¿cuál es la diferencia entre las propiedades definidas en dbo: y las propiedades definidas en dbp:?

Una de las partes fundamentales de los artículos en Wikipedia son las fichas informativas que aparecen al principio del artículo en la esquina superior derecha (para los idiomas que se leen de izquierda a derecha). En estas fichas se resumen los datos más importantes del artículo o del concepto en cuestión.

Como esta tabla informativa no está normalizada y no respeta tipos de datos en sus atributos puede resultar complejo de parsear (ej: un atributo número puede estar representado como numero: mil o numero: 1000). Debido a esta problemática se decidió realizar dos parseos diferentes de los datos. 
Uno que recolecta la información de forma literal tolerando todas las inconsistencias que esta información pueda tener. Y otro que realiza una interpretación más profunda de los datos encontrados,  este parseo mantiene diferentes versiones de las tablas y trata de mergear la información de la manera más coherente posible, incluso llegando a crear recursos adicionales con los datos que se encuentran.

En el primer caso se habla de atributos que poseen el prefijo dbp: y en el segundo caso de los atributos prefijados con dbo:

7.  ¿Cuantas clases y cuantas propiedades tiene la ontología de dbpedia de acuerdo a lo reportado en el artículo?

La ontología de DBpedia consiste de 320 clases las cuales incorporan una jerarquía descripta por 1.650 propiedades diferentes.

8. ¿En que URL puedo ver el listado completo de Clases en la ontología de dbpedia?

Se pueden ver y navegar todas las clases definidas en la ontología de DBpedia en la siguiente URL: http://mappings.dbpedia.org/server/ontology/classes/