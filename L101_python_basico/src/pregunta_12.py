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

def pregunta_12():
    """
    Para cada letra de la primera columna (`letter`), sume todos los valores
    numéricos de los pares `clave:valor` de la quinta columna (`metrics`).
    Retorne un diccionario `{letra: suma}` con las letras en orden alfabético.

    Ejemplo del formato de la respuesta:

        {"A": 177, "B": 187, "C": 114, ...}
    """

    # Se vuelve a repetir el truquito del defaultdict
    resultado = defaultdict(int)

    for fila in abrir_archivo_csv_gz():
        # La letra es la 1ra columna.
        letra = fila[0]

        # Sacar las metricas de la 5ta col.
        metricas = separar_metricas(fila[4])

        # Sumar los valores de las metricas a la letra correspondiente.
        resultado[letra] += sum(metricas.values())

    # Retornar el diccionario con las letras en orden alfabético
    return dict(sorted(resultado.items()))

if __name__ == "__main__":
    print(pregunta_12())