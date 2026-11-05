from pathlib import Path
import pandas as pd

# Definir la ruta del archivo CSV comprimido
RUTA_ACTIVIDAD = Path(__file__).resolve().parents[1]/"data"

# Función para abrir el archivo TSV
def abrir_tsv(nombre_archivo):
    return pd.read_csv(RUTA_ACTIVIDAD/nombre_archivo, sep='\t')

def pregunta_10():
    """
    Usando `data/tbl0.tsv`, construya para cada categoría de la columna `c1`
    un texto con todos sus valores de la columna `c2`, ordenados de menor a
    mayor y separados por `:`. Retorne un DataFrame cuyo índice son las
    categorías, en orden alfabético, con una única columna llamada `c2`.

    Ejemplo del formato de la respuesta:

                           c2
        c1
        A     1:1:2:3:6:7:8:9
        B       1:3:4:5:6:8:9
        C           0:5:6:7:9
        ...
    """

    tabla = abrir_tsv("tbl0.tsv")
    # Agrupar por la columna 'c1' y aplicar al resultado de la columna 'c2' una
    #   función lambda que ordena une con un ':' a los valores de c2 ordenados
    #   y convertidos a string. Luego se convierte el resultado a un DataFrame.
    resultado = (
        tabla.groupby('c1', sort=True)['c2'].
        apply(lambda x: ':'.join(map(str, sorted(x)))).
        to_frame()
    )

    # Se renombran el índice y la columna del DataFrame para cumplir con el
    #   formato de la respuesta.
    resultado.index.name = 'c1'
    resultado.columns = ['c2']

    return resultado
