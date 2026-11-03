import csv
import gzip
from pathlib import Path
# Se utiliza la clase Counter para contar la cantidad de registros por letra
from collections import Counter


# Definir la ruta del archivo CSV comprimido
RUTA_ACTIVIDAD = Path(__file__).resolve().parents[1]
RUTA_ARCHIVO_DATA = RUTA_ACTIVIDAD / "data" / "data.csv.gz"

def abrir_archivo_csv_gz():
    
    # Abrir el archivo CSV.gz y leer los datos
    with gzip.open(RUTA_ARCHIVO_DATA, mode='rt', encoding='utf-8') as archivo:
        # Leer el contenido del archivo CSV y convertirlo en una lista de listas
        return list(csv.reader(archivo, delimiter='\t'))

def pregunta_02():
    """
    Cuente cuántos registros hay para cada letra de la primera columna
    (`letter`). Retorne una lista de tuplas `(letra, cantidad)` ordenada
    alfabéticamente por la letra.

    Ejemplo del formato de la respuesta:

        [("A", 8), ("B", 7), ("C", 5), ...]
    """

    # Se retorna, organizado, un conteo del primer elemento de cada fila,
    #   para cada fila del archivo CSV.gz, lo que equivaldría a la primera
    #  columna del archivo CSV.gz.
    return sorted(Counter(fila[0] for fila in abrir_archivo_csv_gz()).items())
