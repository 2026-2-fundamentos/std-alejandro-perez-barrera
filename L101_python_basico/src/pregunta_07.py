from collections import defaultdict
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

def pregunta_07():
    """
    Para cada valor distinto de la segunda columna (`value`), construya la
    lista de letras de la primera columna (`letter`) que aparecen con ese
    valor. Conserve las letras repetidas y el orden en que aparecen en el
    archivo. Retorne una lista de tuplas `(valor, letras)` ordenada por el
    valor.

    Ejemplo del formato de la respuesta:

        [(0, ["C"]), (1, ["E", "B", "E"]), (2, ["A", "E"]), ...]
    """

    # Un defaultdic(list) es un diccionario que automáticamente crea una lista
    #   vacía para cada clave que aún no existe. En este ejercicio se puede
    #   aplicar para ir agregando las letras a la lista de cada valor.
    lista = defaultdict(list)
    for fila in abrir_archivo_csv_gz():
        # Simplemente defino la letra y el número para cada fila, y luego 
        #   agrego la letra a la lista correspondiente al valor.
        letra = fila[0]
        valor = int(fila[1])

        # Este truquito ahorra un montón de código, porque no hay que verificar
        #   si el número ya existe o no, ni inicializar una lista vacía.
        lista[valor].append(letra)

    return sorted(lista.items())

