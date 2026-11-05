from pathlib import Path
import pandas as pd

# Definir la ruta del archivo CSV comprimido
RUTA_ACTIVIDAD = Path(__file__).resolve().parents[1]/"data"

# Función para abrir el archivo TSV
def abrir_tsv(nombre_archivo):
    return pd.read_csv(RUTA_ACTIVIDAD/nombre_archivo, sep='\t')

def pregunta_13():
    """
    Combine las tablas `data/tbl0.tsv` y `data/tbl2.tsv` usando la columna
    `c0`, que ambas comparten. Luego, sume los valores de la columna `c5b`
    para cada categoría de la columna `c1`. Retorne una Serie de Pandas cuyo
    índice son las categorías, en orden alfabético, y cuyos valores son las
    sumas.

    Ejemplo del formato de la respuesta:

        c1
        A    146
        B    134
        C     81
        ...
    """

    tabla_0 = abrir_tsv("tbl0.tsv")
    tabla_2 = abrir_tsv("tbl2.tsv")

    # Para unir las tablas, usar el merge.
    tabla_combinada = pd.merge(tabla_0, tabla_2, on='c0')

    # Agrupar por la columna c1 la columna c5b, y sumar los valores de c5b para
    #   cada categoría de c1. Luego se ordena el índice alfabéticamente.
    resultado = (tabla_combinada.groupby('c1', sort=True)['c5b'].
                            sum().sort_index())
            
    return resultado
