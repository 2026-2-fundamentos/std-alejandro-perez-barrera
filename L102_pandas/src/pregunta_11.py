from pathlib import Path
import pandas as pd

# Definir la ruta del archivo CSV comprimido
RUTA_ACTIVIDAD = Path(__file__).resolve().parents[1]/"data"

# Función para abrir el archivo TSV
def abrir_tsv(nombre_archivo):
    return pd.read_csv(RUTA_ACTIVIDAD/nombre_archivo, sep='\t')

def pregunta_11():
    """
    En `data/tbl1.tsv`, cada valor de la columna `c0` aparece en varias
    filas, una por cada letra de la columna `c4`. Construya un DataFrame con
    una fila por cada valor de `c0`, en orden ascendente, y las columnas `c0`
    y `c4`. En `c4`, escriba las letras de ese `c0` ordenadas alfabéticamente
    y separadas por comas.

    Ejemplo del formato de la respuesta:

            c0       c4
        0    0    b,f,g
        1    1    a,c,f
        2    2  a,c,e,f
        ...
    """

    df = abrir_tsv("tbl1.tsv")

    # Agrupar por la columna 'c0' y unir los valores de 'c4', ordenados 
    #   alfabéticamente, separados por comas. Se crea un nuevo DataFrame con el
    #   resultado y se reinicia el índice para que 'c0' sea una columna.
    resultado = (df.groupby('c0', sort=True)['c4'].
                    apply(lambda x: ','.join(sorted(x))).reset_index())
    
    return resultado


