from pathlib import Path
import pandas as pd

# Definir la ruta del archivo CSV comprimido
RUTA_ACTIVIDAD = Path(__file__).resolve().parents[1]/"data"

# Función para abrir el archivo TSV
def abrir_tsv(nombre_archivo):
    return pd.read_csv(RUTA_ACTIVIDAD/nombre_archivo, sep='\t')

def pregunta_01():
    """
    ¿Cuántos registros tiene la tabla `data/tbl0.tsv`? Retorne la cantidad
    como un número entero.

    Ejemplo del formato de la respuesta:

        40
    """

    # Cargar la tabla
    tabla = abrir_tsv("tbl0.tsv")
    # El tamaño se saca con len()
    return len(tabla)
