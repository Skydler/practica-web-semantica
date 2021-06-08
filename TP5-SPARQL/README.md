# Trabajo Práctico Nº5

## Integrantes

- Milla, Andrés - 14934/6
- Mandarino, Leonel - 15379/5

## Notas

- Las respuestas se encuentran en el archivo `doc/respuestas.pdf`.
- En el directorio **data** se encuentran los siguientes archivos:
  - **enriched-graph.ttl:** Grafo final. Es decir, con la información de los TPs anteriores, información de los Oscars y personas.
  - **oscar-winners.ttl:** Grafo resultante de la consulta sobre los Oscars (Ejercicio 5).
  - **persons.ttl**: Grafo con todas las tripletas extraídas de Wikidata y DBpedia, de las personas de nuestros anteriores TPs (Ejercicio 5).
- En el directorio **src** se encuentran los siguientes scripts:
  - **main.py**: Ejecuta las consultas del ejercicio 5 y luego las une en un archivo final. Genera el archivo **enriched-graph.ttl**.
  - **enrichments/oscars.py**: Ejecuta la consulta del Oscar y genera el siguiente archivo con sus resultados: **oscar-winners.ttl**.
  - **enrichments/persons.py**: Ejecuta la consulta de las personas y genera el siguiente archivo con sus resultados: **persons.ttl**.

## Requisitos

- *Python3.8* o versiones posteriores.
- Se recomienda un entorno virtual como *virtualenv* para instalar las dependencias

## Ejecución

1. Crear y activar el entorno virtual:

   ```bash
   virtualenv -p python3 venv
   source venv/bin/activate
   ```

2. Instalar las dependencias:

   ```bash
   pip3 install -r requirements.txt
   ```

3. Ir al directorio fuente:

   ```bash
   cd src
   ```

5. Ejecutar el script principal mediante el comando (ejecutará las consultas del ejercicio 5):

   ```bash
   python3 main.py
   ```

### Opciones de ejecución

`--verbose / -v`: Permite visualizar todos los logs.

`--offline / -o`: No ejecuta las consultas remotas, es útil para trabajar de forma offline.

