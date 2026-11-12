import pandas as pd
from pathlib import Path
import re

RUTA_ACTIVIDAD = Path(__file__).resolve().parents[1]/"data"

def pregunta_01():
    """
    El archivo `data/clusters_report.txt` es un reporte de clústeres de
    palabras clave pensado para ser leído por una persona, no por un programa:
    los encabezados ocupan varias líneas, las columnas están alineadas con
    espacios y la lista de palabras clave de un clúster continúa en las líneas
    siguientes.

    Su tarea es convertir ese reporte en un DataFrame de Pandas con una fila
    por clúster y las columnas:

    - `cluster`: número del clúster, como entero.
    - `cantidad_de_palabras_clave`: como entero.
    - `porcentaje_de_palabras_clave`: como número decimal; por ejemplo, el
      texto `15,9 %` debe quedar como `15.9`.
    - `principales_palabras_clave`: todas las palabras clave del clúster en un
      solo texto, separadas por una coma y un único espacio.

    Retorne el DataFrame.

    Ejemplo del formato de la respuesta (se omite la última columna):

           cluster  cantidad_de_palabras_clave  porcentaje_de_palabras_clave
        0        1                         105                          15.9
        1        2                         102                          15.4
        ...
    """

    # Leer el archivo
    with open(RUTA_ACTIVIDAD / 'clusters_report.txt', 'r', encoding='utf-8') as a:
        lineas = a.readlines()

    # Inicializar variables
    datos = []
    # Una variable para cada columna del DataFrame
    cluster = None
    cantidad_palabras = None
    porcentaje_palabras = None
    palabras_clave = []

    # Iterar sobre las líneas del archivo
    # Omitir las primeras 4 líneas que son encabezados
    for linea in lineas[4:]:
        # Ignorar líneas vacías
        if not linea.strip():
            continue

        # Detectar el inicio de un nuevo clúster con regex
        # Esta expresión busca líneas que comienzan con un número (el clúster),
        #   seguido de otro número (cantidad de palabras clave), seguido de un
        #   porcentaje y luego el resto de la línea (principales palabras 
        #   clave)
        # Un clúster no se guarda sino hasta que se detecta uno nuevo, con el
        #   objetivo de garantizar que se capturan todas las líneas de palabras
        #   clave.
        regex = '^\s*(\d+)\s+(\d+)\s+([\d,]+)\s*%\s+(.*)'
        # Buscar coincidencias en la línea
        match = re.match(regex, linea)

        if match:
            # Dado que ya se estuviese procesando otro clúster, se guarda
            if cluster is not None:
                
                # Unir las palabras clave con espacios.
                texto_palabras = ' '.join(palabras_clave)
                
                # Sustituir espacios múltiples por uno solo y quitar punto 
                #   final.
                texto_palabras = re.sub(
                    r'\s+', ' ', texto_palabras).strip().rstrip('.')
                
                # Guardar el clúster en datos.
                datos.append(
                    [cluster, 
                     cantidad_palabras, 
                     porcentaje_palabras, 
                     texto_palabras
                    ]
                )

            # Si no había un clúster antes, o si ya se terminó de procesar, se
            #   asignan los valores del nuevo clúster
            cluster = int(match.group(1))
            cantidad_palabras = int(match.group(2))
            porcentaje_palabras = float(match.group(3).replace(',', '.'))
            palabras_clave = [match.group(4).strip()]

        else:
            # Si no hace match, es una línea de las palabras clave adicional.
            palabras_clave.append(linea.strip())

    # Guardar el último cluster al terminar de escanear líneas.
    if cluster is not None:
                    
        # Unir las palabras clave con espacios.
        texto_palabras = ' '.join(palabras_clave)
        
        # Sustituir espacios múltiples por uno solo y quitar punto 
        #   final.
        texto_palabras = re.sub(r'\s+',' ', texto_palabras).strip().rstrip('.')
        
        # Guardar el clúster en datos.
        datos.append(
            [cluster, cantidad_palabras, porcentaje_palabras, texto_palabras])

    # Construir el DataFrame
    df = pd.DataFrame(
            datos, columns=[
                'cluster', 
                'cantidad_de_palabras_clave', 
                'porcentaje_de_palabras_clave', 
                'principales_palabras_clave'
            ]
        )

    return df

if __name__ == "__main__":
    print(pregunta_01().head())