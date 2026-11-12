import sqlite3
from pathlib import Path
import pandas as pd

ACTIVITY_DIR = Path(__file__).resolve().parents[1]
INPUT_FILE = ACTIVITY_DIR / "data" / "ventas.csv"
OUTPUT_FILE = ACTIVITY_DIR / "submission" / "ventas.csv"
TEMP_DB_FILE = ACTIVITY_DIR / "temp" / "ventas.db"

# Nombre de la tabla temporal en la base de datos SQLite
TEMP_TABLE_NAME = "ventas"


# Copiar los reemplazos del P106_limpieza_pandas/src/main.py
SUPPLIER_REPLACEMENTS = {
    "amazon web services colombia": "Amazon Web Services Colombia",
    "BANCOLOMBIA S.A.": "Bancolombia S.A.",
    "Cementos Argos SA": "Cementos Argos S.A.",
    "cementos argos s.a.": "Cementos Argos S.A.",
    "Corona SAS": "Corona S.A.S.",
    "Ecopetrol  S.A.": "Ecopetrol S.A.",
    "GOOGLE COLOMBIA LTDA.": "Google Colombia Ltda.",
    "Grupo  Éxito  S.A.": "Grupo Éxito S.A.",
    "IBM Colombia SAS.": "IBM Colombia S.A.S.",
    "ibm colombia s.a.s.": "IBM Colombia S.A.S.",
    "MICROSOFT COLOMBIA INC.": "Microsoft Colombia Inc.",
    "Nutresa SA": "Nutresa S.A.",
    "nutresa s.a.": "Nutresa S.A.",
    "oracle colombia ltda.": "Oracle Colombia Ltda.",
    "POSTOBÓN S.A.": "Postobon S.A.",
    "SAP Colombia SAS": "SAP Colombia S.A.S.",
    "Schneider  Electric": "Schneider Electric",
    "SIEMENS S.A.S.": "Siemens S.A.S.",
    "siemens s.a.s.": "Siemens S.A.S.",
    "Sura  S.A.": "Sura S.A.",
    "Telefónica  Colombia": "Telefónica Colombia",
}


COUNTRY_REPLACEMENTS = {
    "CO": "COL",
    "COLOMBIA": "COL",
    "Colombia": "COL",
    "colombia": "COL",
}

CITY_REPLACEMENTS = {
    "bogotá": "Bogotá",
    "BOGOTÁ": "Bogotá",
    "Medellin": "Medellín",
    "medellín": "Medellín",
    "MEDELLÍN": "Medellín",
}

def clean_column_names(tabla, conexion):
    
    # Casos tipicos en la columna
    # ' Supplier ID ' -> "supplier_id"
    # 'City ' -> "city"
    # 'Purchase Date' -> "purchase_date"
    
    columnas = pd.read_sql(f"SELECT * FROM {tabla} LIMIT 0", conexion).columns.to_frame(name="COLUMN_NAME")
    columnas_renombradas = [columna.strip().lower().replace(" ", "_") for columna in columnas["COLUMN_NAME"]]

    # Ejecutar el renombramiento de columnas en la tabla
    for columna_original, columna_nueva in zip(columnas["COLUMN_NAME"], columnas_renombradas):
        # Si la columna original es diferente de la nueva, renombrar. Evitar
        #   queries superfluas.
        if columna_original != columna_nueva:
            renombrar_columna = f"""
                ALTER TABLE {tabla}
                RENAME COLUMN "{columna_original}" TO "{columna_nueva}";
            """
            conexion.execute(renombrar_columna)


# Limpiar columna de proveedores
def clean_supplier_column(tabla, conexion):
    # Cambiar los nombres de proveedores según el diccionario SUPPLIER_REPLACEMENTS

    # En caso de que el nombre del proveedor ya esté limpio se normaliza por si
    #   acaso con TRIM, para eliminar espacios en blanco al inicio o al final
    # REPLACE quita dobles espacios, hasta triples espacios que puedan haber.
    
    # Geniazo Copilot por enseñarme este truco.
    supplier_limpio = """
        TRIM(
            REPLACE(
                REPLACE(supplier, '  ', ' '),
                '   ', ' '
            )
        )
    """

    # Condicion para limpiar. También usa TRIM.
    condiciones = " ".join(
        f"WHEN TRIM(supplier) = '{antiguo}' THEN '{nuevo.strip()}'"
        for antiguo, nuevo in SUPPLIER_REPLACEMENTS.items()
    )

    # En la query tambien usar el TRIM.
    query = f"""
        UPDATE {tabla}
        SET supplier = TRIM(
            CASE 
                {condiciones}
                ELSE {supplier_limpio}
            END
        )
    """
    conexion.execute(query)
    conexion.commit()  # Confirmar los cambios en la base de datos


def clean_country_column(tabla, conexion):
    # Cambiar los nombres de países según el diccionario COUNTRY_REPLACEMENTS
    condiciones = " ".join(
        f"WHEN TRIM(country) = '{antiguo}' THEN '{nuevo.strip()}'"
        for antiguo, nuevo in COUNTRY_REPLACEMENTS.items()
    )

    # En la query tambien usar el TRIM.
    query = f"""
        UPDATE {tabla}
        SET country = TRIM(
            CASE 
                {condiciones}
                ELSE TRIM(country)
            END
        )
    """
    conexion.execute(query)
    conexion.commit()  # Confirmar los cambios en la base de datos


def clean_city_column(tabla, conexion):
    # Cambiar los nombres de ciudades según el diccionario CITY_REPLACEMENTS
    condiciones = " ".join(
        f"WHEN TRIM(city) = '{antiguo}' THEN '{nuevo.strip()}'"
        for antiguo, nuevo in CITY_REPLACEMENTS.items()
    )

    # En la query tambien usar el TRIM.
    query = f"""
        UPDATE {tabla}
        SET city = TRIM(
            CASE 
                {condiciones}
                ELSE TRIM(city)
            END
        )
    """
    conexion.execute(query)
    conexion.commit()  # Confirmar los cambios en la base de datos


def clean_purchase_date_column(tabla, conexion):
    # Limpiar la columna de fecha de compra
    fecha = "TRIM(purchase_date)"
    # SQL GLOB permite usar patrones para reconocer formatos.
    query = f"""
        UPDATE {tabla}
        SET purchase_date =
            CASE
                -- YYYY/MM/DD
                WHEN {fecha} GLOB
                    '[0-9][0-9][0-9][0-9]/[0-9][0-9]/[0-9][0-9]'
                THEN
                    substr({fecha}, 1, 4) || '-' ||
                    substr({fecha}, 6, 2) || '-' ||
                    substr({fecha}, 9, 2)

                -- MM/DD/YYYY o DD/MM/YYYY
                WHEN {fecha} GLOB
                    '[0-9][0-9]/[0-9][0-9]/[0-9][0-9][0-9][0-9]'
                THEN
                    CASE
                        -- Si la segunda parte es mayor que 12,
                        -- se interpreta como DD/MM/YYYY
                        WHEN (CAST(substr({fecha}, 4, 2) AS REAL) < 12)
                        THEN
                            substr({fecha}, 7, 4) || '-' ||
                            substr({fecha}, 4, 2) || '-' ||
                            substr({fecha}, 1, 2)

                        -- En otro caso se interpreta como MM/DD/YYYY
                        ELSE
                            substr({fecha}, 7, 4) || '-' ||
                            substr({fecha}, 1, 2) || '-' ||
                            substr({fecha}, 4, 2)
                    END

                -- DD.MM.YYYY
                WHEN {fecha} GLOB
                    '[0-9][0-9].[0-9][0-9].[0-9][0-9][0-9][0-9]'
                THEN
                    substr({fecha}, 7, 4) || '-' ||
                    substr({fecha}, 4, 2) || '-' ||
                    substr({fecha}, 1, 2)

                -- DD-MM-YY
                WHEN {fecha} GLOB
                    '[0-9][0-9]-[0-9][0-9]-[0-9][0-9]'
                THEN
                    '20' || substr({fecha}, 7, 2) || '-' ||
                    substr({fecha}, 4, 2) || '-' ||
                    substr({fecha}, 1, 2)

                -- Fechas que ya están limpias, como YYYY-MM-DD
                ELSE {fecha}
            END
    """

    conexion.execute(query)
    conexion.commit()


def clean_amount_column(tabla, conexion):
    amount = "NULLIF(TRIM(amount), '')"  # NULL si está vacío o solo espacios

    # Limpiar la columna de amount según los patrones observados en el dataset
    query = f"""
        UPDATE {tabla}
        SET amount =
            CASE
                WHEN {amount} IS NULL THEN NULL

                WHEN UPPER({amount}) LIKE '%K'
                THEN CAST(REPLACE(UPPER({amount}), 'K', '') AS REAL) * 1000

                WHEN UPPER({amount}) LIKE 'COP%'
                THEN CAST(REPLACE(
                    TRIM(SUBSTR({amount}, 4)), ',', ''
                ) AS REAL)

                WHEN {amount} LIKE '$%'
                THEN CAST(REPLACE(
                    TRIM(SUBSTR({amount}, 2)), ',', ''
                ) AS REAL)

                ELSE CAST(REPLACE({amount}, '.', '') AS REAL)
            END
    """
    conexion.execute(query)
    conexion.commit()


def clean_discount_column(tabla, conexion):
    descuento = "NULLIF(TRIM(discount), '')"  # NULL si está vacío o solo espacios

    query = f"""
        UPDATE {tabla}
        SET discount =
            CASE
                WHEN {descuento} IS NULL THEN NULL

                WHEN instr({descuento}, '%') > 0
                THEN CAST(
                    REPLACE({descuento}, '%', '')
                    AS REAL
                ) / 100

                WHEN CAST({descuento} AS REAL) > 1
                THEN CAST({descuento} AS REAL) / 100

                ELSE CAST({descuento} AS REAL)
            END
    """

    conexion.execute(query)
    conexion.commit()


def clean_weight_column(tabla, conexion):
    weight = "NULLIF(TRIM(weight), '')"
    weight_comas = f"REPLACE({weight}, ',', '.')"

    query = f"""
        UPDATE {tabla}
        SET weight =
            CASE
                WHEN {weight} IS NULL THEN NULL

                WHEN lower({weight}) LIKE '% ton'
                THEN 
                    CAST(
                        TRIM(
                            SUBSTR({weight}, 1, LENGTH({weight}) - 4)
                        )
                    AS REAL
                ) * 1000

                WHEN lower({weight}) LIKE '% kg'
                THEN 
                    CAST(
                        TRIM(
                            SUBSTR({weight}, 1, LENGTH({weight}) - 3)
                        )
                    AS REAL
                )

                WHEN lower({weight}) LIKE '% g'
                THEN CAST(
                    TRIM(SUBSTR({weight}, 1, LENGTH({weight}) - 2))
                    AS REAL
                ) / 1000

                ELSE 
                    CAST(
                        {weight_comas} 
                    AS REAL
                )
            END
    """

    conexion.execute(query)
    conexion.commit()


def clean_unit_price_column(tabla, conexion):
    price = "NULLIF(TRIM(unit_price), '')"
    price_sin_peso = f"REPLACE({price}, '$', '')"
    price_sin_comas = f"REPLACE({price_sin_peso}, ',', '')"

    query = f"""
        UPDATE {tabla}
        SET unit_price =
            CASE
                WHEN {price} IS NULL THEN NULL

                -- Cuando existen varios puntos, el último separa
                -- los decimales. En la data se manejan 2 decimales.
                WHEN (
                    LENGTH({price_sin_comas}) -
                    LENGTH(REPLACE({price_sin_comas}, '.', ''))
                ) > 1
                THEN CAST(
                    REPLACE({price_sin_comas}, '.', '')
                    AS REAL
                ) / 100

                ELSE CAST({price_sin_comas} AS REAL)
            END
    """

    conexion.execute(query)
    conexion.commit()


def clean_contact_email_column(tabla, conexion):
    query = f"""
        UPDATE {tabla}
        SET contact_email =
            CASE
                WHEN contact_email IS NULL THEN NULL
                WHEN lower(TRIM(contact_email)) = 'sin correo'
                THEN NULL
                ELSE lower(TRIM(contact_email))
            END
    """

    conexion.execute(query)
    conexion.commit()


def main():
    original = pd.read_csv(INPUT_FILE)
    conexion = sqlite3.connect(TEMP_DB_FILE)
    original.to_sql(TEMP_TABLE_NAME, conexion, if_exists="replace", index=False)

    # Aplicar los cambios de limpieza en la base de datos SQLite
    clean_column_names(TEMP_TABLE_NAME, conexion)
    clean_supplier_column(TEMP_TABLE_NAME, conexion)
    clean_country_column(TEMP_TABLE_NAME, conexion)
    clean_city_column(TEMP_TABLE_NAME, conexion)
    clean_purchase_date_column(TEMP_TABLE_NAME, conexion)
    clean_amount_column(TEMP_TABLE_NAME, conexion)
    clean_discount_column(TEMP_TABLE_NAME, conexion)
    clean_weight_column(TEMP_TABLE_NAME, conexion)
    clean_unit_price_column(TEMP_TABLE_NAME, conexion)
    clean_contact_email_column(TEMP_TABLE_NAME, conexion)


    # Leer la tabla limpia desde SQLite y guardarla en CSV
    df_limpio = pd.read_sql(f"SELECT * FROM {TEMP_TABLE_NAME}", conexion)
    df_limpio.to_csv(OUTPUT_FILE, index=False)

    # Cerrar la conexión a la base de datos
    conexion.close()

if __name__ == "__main__":
    main()
