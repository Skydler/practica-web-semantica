# Trabajo Práctico Nº4

## Integrantes

- Milla, Andrés - 14934/6
- Mandarino, Leonel - 15379/5

## Notas

- Las respuestas se encuentran en el archivo `doc/respuestas.pdf`.
- En el directorio **data** se encuentran los siguientes archivos:
  - **dataset-original.ttl:** Como su nombre lo indica es el dataset generado en la anterior entrega.
  - **links.ttl:** Resultado del mapeo *sameAs* de cada actor local con su actor correspondiente en Dbpedia.
  - **dataset-enriquecido.ttl:** Dataset original con el agregado de los campos requeridos por el enunciado, extraidos de los recursos en Dbpedia.

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

4. Generar un archivo *links.ttl*, mediante el comando:

   ```bash
   python3 main.py --links
   ```

5. Ejecutar el enriquecedor, mediante el comando:

   ```bash
   python3 main.py -e ../data/dataset-original.ttl ../data/links.ttl > ../data/dataset-enriquecido.ttl
   ```

### Opciones de ejecución

`--verbose`: Permite visualizar todos los logs.

`--links / -l`: Genera el archivo que linkea los datos originales con Dbpedia en `data/links.ttl`

`--enriching / -e`: Ejecuta el enriquecedor del dataset original. Espera dos parámetros, el primero indicando el path al dataset original y el segundo el path al archivo con el mapeo de actores. El resultado se imprime en la salida estándar.

