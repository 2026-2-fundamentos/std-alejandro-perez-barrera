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

def pregunta_06():
    """
    La quinta columna (`metrics`) contiene pares `clave:valor` separados por
    comas. Para cada clave, encuentre el valor mínimo y el valor máximo que
    aparecen en todo el archivo. Retorne una lista de tuplas
    `(clave, mínimo, máximo)` ordenada alfabéticamente por la clave.

    Observe que el orden es mínimo y luego máximo, al contrario de la
    pregunta 5.

    Ejemplo del formato de la respuesta:

        [("aaa", 1, 9), ("bbb", 1, 9), ...]
    """

    valores = {}
    for fila in abrir_archivo_csv_gz():
        # Tengo las metricas separadas para cada fila en un diccionario
        metricas = separar_metricas(fila[4])

        for clave, valor in metricas.items():
            if clave not in valores:
                # La iteración empieza asignando el 1er valor de max y min
                valores[clave] = [valor, valor]
            else:
                if valor < valores[clave][0]:
                    valores[clave][0] = valor
                elif valor > valores[clave][1]:
                    valores[clave][1] = valor
                else:
                    continue

    return [
        (clave, min, max) for clave, (min, max) in sorted(valores.items())
    ]

