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

def pregunta_05():
    """
    Para cada letra de la primera columna (`letter`), encuentre el valor
    máximo y el valor mínimo de la segunda columna (`value`). Retorne una lista
    de tuplas `(letra, máximo, mínimo)` ordenada alfabéticamente por la letra.

    Ejemplo del formato de la respuesta:

        [("A", 9, 2), ("B", 9, 1), ...]
    """

    valores = {}
    for fila in abrir_archivo_csv_gz():
        letra = fila[0]
        valor = int(fila[1])

        if letra not in valores:
            # La iteración empieza asignando el 1er valor de max y min
                              #max , min
            valores[letra] = [valor, valor]

        elif valor > valores[letra][0]:
            valores[letra][0] = valor
        elif valor < valores[letra][1]:
            valores[letra][1] = valor
        else:
            continue

    return [
        (letra, max, min) for letra, (max, min) in sorted(valores.items())
    ]
