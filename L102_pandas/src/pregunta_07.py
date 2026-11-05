from pathlib import Path
import pandas as pd

# Definir la ruta del archivo CSV comprimido
RUTA_ACTIVIDAD = Path(__file__).resolve().parents[1]/"data"

# Función para abrir el archivo TSV
def abrir_tsv(nombre_archivo):
    return pd.read_csv(RUTA_ACTIVIDAD/nombre_archivo, sep='\t')

def pregunta_07():
    """
    Usando `data/tbl0.tsv`, sume los valores de la columna `c2` para cada
    categoría de la columna `c1`. Retorne una Serie de Pandas cuyo índice son
    las categorías, en orden alfabético, y cuyos valores son las sumas.

    Ejemplo del formato de la respuesta:

        c1
        A    37
        B    36
        C    27
        ...
    """

    tabla = abrir_tsv("tbl0.tsv")
    # Retornar, ordenados alfabéticamente, las sumas de la columna c2,
    #   agrupados por la columna c1.
    return tabla.groupby('c1')['c2'].sum().sort_index()

