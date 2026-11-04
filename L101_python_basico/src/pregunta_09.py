import csv
import gzip
from pathlib import Path
from collections import Counter


# Definir la ruta del archivo CSV comprimido
RUTA_ACTIVIDAD = Path(__file__).resolve().parents[1]
RUTA_ARCHIVO_DATA = RUTA_ACTIVIDAD / "data" / "data.csv.gz"

def abrir_archivo_csv_gz():
    
    # Abrir el archivo CSV.gz y leer los datos
    with gzip.open(RUTA_ARCHIVO_DATA, mode='rt', encoding='utf-8') as archivo:
        # Leer el contenido del archivo CSV y convertirlo en una lista de listas
        return list(csv.reader(archivo, delimiter='\t')) 

def separar_metricas(metricas):
    
    return {
        # Retorna un diccionario clave valor (int)
        clave: int(valor) 
        # Para cada par clave:valor
        for clave, valor in (
            # En la columna metrics, donde se separan clave y valor con un ':'
            par.split(":",1) 
            # Para cada par separado por comas en la columna metrics
            for par in metricas.split(",")
        )
    }

def pregunta_09():
    """
    Cuente cuántas veces aparece cada clave en la quinta columna (`metrics`)
    de todo el archivo. Retorne un diccionario `{clave: cantidad}` con las
    claves en orden alfabético.

    Ejemplo del formato de la respuesta:

        {"aaa": 13, "bbb": 16, "ccc": 23, ...}
    """

    # En este caso para contar cuantas veces salen las claves, se usa un 
    #   Counter.
    contador = Counter()

    # Por cada fila en el csv, se separan las metricas y se actualiza el 
    #   contador con las claves.
    for fila in abrir_archivo_csv_gz():
        contador.update(separar_metricas(fila[4]).keys())

    return {
        # Retornar un diccionario con las claves, y su conteo registrado en el
        #   contador, ordenadas alfabéticamente.
        clave: contador[clave]
        for clave in sorted(contador)
    }
