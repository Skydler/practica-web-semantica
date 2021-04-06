# Requisitos

- *Python3.8* o versiones posteriores.
- *Chromedriver*: https://chromedriver.chromium.org/downloads
- Se recomienda un entorno virtual como *virtualenv* para instalar las dependencias

# Ejecución

1. Copiar el binario de *Chromedriver* en el directorio **bin**

2. Crear y activar el entorno virtual:

   ```bash
   virtualenv -p python3 venv
   source venv/bin/activate
   ```

3. Instalar las dependencias:

   ```bash
   pip3 install -r requirements.txt
   ```

4. Ir al directorio fuente:

   ```bash
   cd src
   ```

5. Ejecutar el script:

   ```bash
   python3 main.py
   ```

## Opciones de ejecución

`--verbose`: Permite visualizar todos los logs.

`--offline`: Ejecuta solo el merge, es útil para no scrapear de nuevo.