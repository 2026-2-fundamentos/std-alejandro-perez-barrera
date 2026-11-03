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

def pregunta_08():
    """
    Repita la pregunta 7, pero ahora cada lista de letras debe contener cada
    letra una sola vez y estar ordenada alfabéticamente. Retorne una lista de
    tuplas `(valor, letras)` ordenada por el valor.

    Ejemplo del formato de la respuesta:

        [(0, ["C"]), (1, ["B", "E"]), (2, ["A", "E"]), ...]
    """

    # Ahora 😈, en lugar de una lista en el defaultdict pongo un set.
    #   En un set los elementos no se repiten y no tienen un orden específico.
    #   Por eso, al final, hay que convertir el set en una lista y ordenarla.
    lista = defaultdict(set)
    for fila in abrir_archivo_csv_gz():
        # Repetir lo del punto 7.
        letra = fila[0]
        valor = int(fila[1])
        lista[valor].add(letra)

    return [
        # Retornar una lista de tuplas (valor, letras) con las letras ordenadas
        #   alfabéticamente.
        (valor, sorted(letras)) 
        # Por cada tupla (valor, letras) en los items del diccionario, 
        #   ordenados por el valor.
        for valor, letras in sorted(lista.items())
    ]
