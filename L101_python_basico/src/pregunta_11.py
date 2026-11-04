import csv
import gzip
from pathlib import Path
from collections import defaultdict

# Definir la ruta del archivo CSV comprimido
RUTA_ACTIVIDAD = Path(__file__).resolve().parents[1]
RUTA_ARCHIVO_DATA = RUTA_ACTIVIDAD / "data" / "data.csv.gz"

def abrir_archivo_csv_gz():
    
    # Abrir el archivo CSV.gz y leer los datos
    with gzip.open(RUTA_ARCHIVO_DATA, mode='rt', encoding='utf-8') as archivo:
        # Leer el contenido del archivo CSV y convertirlo en una lista de listas
        return list(csv.reader(archivo, delimiter='\t')) 

def pregunta_11():
    """
    La cuarta columna (`codes`) contiene letras minúsculas separadas por
    comas. Para cada una de esas letras, sume los valores de la segunda
    columna (`value`) de los registros en los que aparece. Retorne un
    diccionario `{letra: suma}` con las letras en orden alfabético.

    Ejemplo del formato de la respuesta:

        {"a": 122, "b": 49, "c": 91, ...}
    """

    # Vuelve a jugar el truco del defaultdict.
    cantidades = defaultdict(int)

    for fila in abrir_archivo_csv_gz():
        # Definir cuales son las letras.
        letras = fila[3].split(",")
        # Definir cual es el valor
        valor = int(fila[1])
        # Sumar el valor a la letras correspondientes
        for letra in letras:
            cantidades[letra] += valor

    # Retornar el diccionario con las letras en orden alfabético
    return dict(sorted(cantidades.items()))
