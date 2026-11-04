import csv
import gzip
from pathlib import Path


# Definir la ruta del archivo CSV comprimido
RUTA_ACTIVIDAD = Path(__file__).resolve().parents[1]
RUTA_ARCHIVO_DATA = RUTA_ACTIVIDAD / "data" / "data.csv.gz"

def abrir_archivo_csv_gz():
    
    # Abrir el archivo CSV.gz y leer los datos
    with gzip.open(RUTA_ARCHIVO_DATA, mode='rt', encoding='utf-8') as archivo:
        # Leer el contenido del archivo CSV y convertirlo en una lista de listas
        return list(csv.reader(archivo, delimiter='\t')) 

def pregunta_10():
    """
    Para cada registro del archivo, en el mismo orden en que aparecen,
    retorne una tupla con la letra de la primera columna (`letter`), la
    cantidad de elementos de la cuarta columna (`codes`) y la cantidad de
    pares de la quinta columna (`metrics`). El resultado es una lista con una
    tupla por registro.

    Ejemplo del formato de la respuesta:

        [("E", 3, 5), ("A", 3, 4), ("B", 4, 4), ...]
    """

    # Lista para guardar el resultado
    resultado = []

    # Por cada fila en el csv
    for fila in abrir_archivo_csv_gz():
        # La letra es la 1ra columna.
        letra = fila[0]
        # En la 4ta columna, los elementos están separados por comas, por lo
        #   que se puede usar split para contar cuantos hay.
        cantidad_codes = len(fila[3].split(","))
        # Lo mismo en la 5ta columna, pero ahora los elementos son pares 
        #   clave:valor, igual separados por comas.
        cantidad_metrics = len(fila[4].split(","))

        # Cada tupla se agrega a la lista resultado.
        resultado.append((letra, cantidad_codes, cantidad_metrics))
    # return resultado.
    return resultado
