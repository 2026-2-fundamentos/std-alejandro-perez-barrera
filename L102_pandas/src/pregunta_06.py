from pathlib import Path
import pandas as pd

# Definir la ruta del archivo CSV comprimido
RUTA_ACTIVIDAD = Path(__file__).resolve().parents[1]/"data"

# Función para abrir el archivo TSV
def abrir_tsv(nombre_archivo):
    return pd.read_csv(RUTA_ACTIVIDAD/nombre_archivo, sep='\t')

def pregunta_06():
    """
    Usando `data/tbl1.tsv`, obtenga los valores distintos de la columna `c4`,
    conviértalos a mayúsculas y retórnelos como una lista ordenada
    alfabéticamente.

    Ejemplo del formato de la respuesta:

        ["A", "B", "C", "D", "E", "F", "G"]
    """

    tabla = abrir_tsv("tbl1.tsv")
    # Retornar, en orden, los valores únicos de la columna c4, tratados como
    #   string y pasados a mayúsculas.
    return sorted(tabla['c4'].str.upper().unique())

