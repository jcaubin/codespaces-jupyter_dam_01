from __future__ import annotations

import os
from pathlib import Path

import duckdb
import requests
import pandas as pd
import requests
from io import StringIO 
from datetime import datetime



PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
MAESTRAS_DIR = PROJECT_ROOT / "maestras"
SCHEMA_PATH = PROJECT_ROOT / "sql" / "001_schema.sql"

DB_PATH = '/home/jcaubin/datos/duck_test_new.db'

ULR_CALAIR_CSV = "https://datos.madrid.es/dataset/212531-0-calidad-aire-tiempo-real/resource/212531-2-calidad-aire-tiempo-real/download/212531-2-calidad-aire-tiempo-real.csv"
URL_ESTACIONES_CALAIR = "https://datos.madrid.es/dataset/212629-0-estaciones-control-aire/resource/212629-0-estaciones-control-aire-csv/download/212629-0-estaciones-control-aire-csv.csv"
URL_ESTACIONES_METEO = "https://datos.madrid.es/dataset/300360-0-meteorologicos-estaciones/resource/300360-1-meteorologicos-estaciones-csv/download/300360-1-meteorologicos-estaciones-csv.csv"
URL_METEO_CSV = "https://datos.madrid.es/dataset/300392-0-meteorologia-tiempo-real/resource/300392-2-meteorologia-tiempo-real/download/300392-2-meteorologia-tiempo-real.csv"

def download_csv_as_dataframe(url: str, separator: str = ",", decimal: str = ".") -> pd.DataFrame:
    try:    
        response = requests.get(url, timeout=60)
        response.raise_for_status()
        response.encoding = response.apparent_encoding  # Ajusta la codificación según el contenido 
        df = pd.read_csv(StringIO(response.text), sep=separator, decimal=decimal)
        return df
    except requests.RequestException as e:
        print(f"Error al descargar el CSV desde {url}: {e}")
        raise
    
def store_meteo_data(conn: duckdb.DuckDBPyConnection) -> None:
    try:
        fx_data = datetime.now()

        df_meteo = download_csv_as_dataframe(URL_METEO_CSV, separator=';', decimal='.')
        df_meteo['FX_DATA'] = fx_data
        conn.register('df_meteo', df_meteo)
        conn.execute("CREATE OR REPLACE TABLE METEO2 AS SELECT * FROM df_meteo")
        print("Datos meteorológicos cargados correctamente en la tabla 'meteo'.")

        df_estaciones = download_csv_as_dataframe(URL_ESTACIONES_METEO, separator=';', decimal='.')
        df_estaciones['FX_DATA'] = fx_data
        conn.register('df_estaciones', df_estaciones)
        conn.execute("CREATE OR REPLACE TABLE ESTACIONES_METEO2 AS SELECT * FROM df_estaciones")
        print("Datos de estaciones meteorológicas cargados correctamente en la tabla 'estaciones_meteo'.")

        df_calair = download_csv_as_dataframe(ULR_CALAIR_CSV, separator=';', decimal='.')
        df_calair['FX_DATA'] = fx_data
        conn.register('df_calair', df_calair)
        conn.execute("CREATE OR REPLACE TABLE CALAIR2 AS SELECT * FROM df_calair")
        print("Datos de calidad del aire cargados correctamente en la tabla 'calair'.")

    except Exception as e:
        print(f"Error al obtener los datos meteorológicos: {e}")
        raise

def process_meteo_data(conn: duckdb.DuckDBPyConnection) -> None:
    try:
        #pivota los datos de calidad del aire para obtener una tabla con columnas HORA y VALOR
        conn.execute(
            """
            CREATE OR REPLACE TABLE CALAIR24_PIVOT_D AS
            SELECT
                PROVINCIA,
                MUNICIPIO,
                ESTACION,
                MAGNITUD,
                PUNTO_MUESTREO,
                ANO,
                MES,
                DIA,
                CAST(RIGHT(HORA, 2) AS INTEGER) AS H,
                VALOR
            FROM CALAIR2
            UNPIVOT (
                VALOR FOR HORA IN (
                    H01, H02, H03, H04, H05, H06, H07, H08, H09, H10,
                    H11, H12, H13, H14, H15, H16, H17, H18, H19, H20,
                    H21, H22, H23, H24
                )
            );
            """
        )

        conn.execute(
            """
            CREATE OR REPLACE TABLE CALAIR24_PIVOT_V AS
            SELECT
                PROVINCIA,
                MUNICIPIO,
                ESTACION,
                MAGNITUD,
                PUNTO_MUESTREO,
                ANO,
                MES,
                DIA,
                CAST(RIGHT(HORA, 2) AS INTEGER) AS H,
                VALIDEZ
            FROM CALAIR2
            UNPIVOT (
                VALIDEZ FOR HORA IN (
                    V01, V02, V03, V04, V05, V06, V07, V08, V09, V10,
                    V11, V12, V13, V14, V15, V16, V17, V18, V19, V20,
                    V21, V22, V23, V24
                )
            );
            """
        )

        conn.execute(
            """
            CREATE OR REPLACE TABLE CALAIR24_PIVOT AS
            SELECT
                td.*,
                tv.VALIDEZ,
                e.ESTACION AS ESTACION_DESC,
                e.ALTITUD,
                m.PARAMETRO
            FROM CALAIR24_PIVOT_D td
            INNER JOIN CALAIR24_PIVOT_V tv
                ON td.PROVINCIA = tv.PROVINCIA
            AND td.MUNICIPIO = tv.MUNICIPIO
            AND td.ESTACION = tv.ESTACION
            AND td.MAGNITUD = tv.MAGNITUD
            AND td.PUNTO_MUESTREO = tv.PUNTO_MUESTREO
            AND td.ANO = tv.ANO
            AND td.MES = tv.MES
            AND td.DIA = tv.DIA
            AND td.H = tv.H
            INNER JOIN ESTACIONES_METEO2 e
                ON td.ESTACION = e.CÓDIGO_CORTO
            INNER JOIN magnitudes m
                ON m.CODIGO = tv.MAGNITUD;
            """
        )
  
        #pivota los datos de meteo para obtener una tabla con columnas HORA y VALOR
        conn.execute(
            """
            CREATE OR REPLACE TABLE METEO24_PIVOT_D AS
            SELECT
                PROVINCIA,
                MUNICIPIO,
                ESTACION,
                MAGNITUD,
                concat(PROVINCIA, MUNICIPIO, ESTACION,  '_' ,MAGNITUD, '_98') PUNTO_MUESTREO,
                ANO,
                MES,
                DIA,
                CAST(RIGHT(HORA, 2) AS INTEGER) AS H,
                VALOR
            FROM METEO2
            UNPIVOT (
                VALOR FOR HORA IN (
                    H01, H02, H03, H04, H05, H06, H07, H08, H09, H10,
                    H11, H12, H13, H14, H15, H16, H17, H18, H19, H20,
                    H21, H22, H23, H24
                )
            );
            """
        )

        conn.execute(
            """
            CREATE OR REPLACE TABLE METEO24_PIVOT_V AS
            SELECT
                PROVINCIA,
                MUNICIPIO,
                ESTACION,
                MAGNITUD,
                concat(PROVINCIA, MUNICIPIO, ESTACION,  '_' ,MAGNITUD, '_98') PUNTO_MUESTREO,
                ANO,
                MES,
                DIA,
                CAST(RIGHT(HORA, 2) AS INTEGER) AS H,
                VALIDEZ
            FROM METEO2
            UNPIVOT (
                VALIDEZ FOR HORA IN (
                    V01, V02, V03, V04, V05, V06, V07, V08, V09, V10,
                    V11, V12, V13, V14, V15, V16, V17, V18, V19, V20,
                    V21, V22, V23, V24
                )
            );
            """
        )

        conn.execute(
            """
            CREATE OR REPLACE TABLE METEO24_PIVOT AS
            SELECT
                td.*,
                tv.VALIDEZ,
                e.ESTACION AS ESTACION_DESC,
                e.ALTITUD,
                m.PARAMETRO
            FROM METEO24_PIVOT_D td
            INNER JOIN METEO24_PIVOT_V tv
                ON td.PROVINCIA = tv.PROVINCIA
            AND td.MUNICIPIO = tv.MUNICIPIO
            AND td.ESTACION = tv.ESTACION
            AND td.MAGNITUD = tv.MAGNITUD
            AND td.PUNTO_MUESTREO = tv.PUNTO_MUESTREO
            AND td.ANO = tv.ANO
            AND td.MES = tv.MES
            AND td.DIA = tv.DIA
            AND td.H = tv.H
            INNER JOIN ESTACIONES_METEO2 e
                ON td.ESTACION = e.CÓDIGO_CORTO
            INNER JOIN magnitudes m
                ON m.CODIGO = tv.MAGNITUD;
            """
        )

        # Inserta los datos procesados en la tabla calair
        conn.execute(
            """
            INSERT OR REPLACE INTO calair BY NAME
            SELECT
                PROVINCIA,
                MUNICIPIO,
                ESTACION,
                MAGNITUD,
                PUNTO_MUESTREO,
                ANO,
                MES,
                DIA,
                H,
                VALOR,
                VALIDEZ,
                ESTACION_DESC,
                ALTITUD,
                PARAMETRO,
                CURRENT_TIMESTAMP AS fx_data
            FROM CALAIR24_PIVOT
            UNION ALL
            SELECT
                PROVINCIA,
                MUNICIPIO,
                ESTACION,
                MAGNITUD,
                PUNTO_MUESTREO,
                ANO,
                MES,
                DIA,
                H,
                VALOR,
                VALIDEZ,
                ESTACION_DESC,
                ALTITUD,
                PARAMETRO,
                CURRENT_TIMESTAMP AS fx_data
            FROM METEO24_PIVOT;
            """
        )
        print("Datos meteorológicos procesados correctamente.")
    except Exception as e:
        print(f"Error al procesar los datos meteorológicos: {e}")
        raise

def ensure_schema(conn: duckdb.DuckDBPyConnection) -> None:
    if not SCHEMA_PATH.exists():
        raise FileNotFoundError(f"No se encontró el esquema en {SCHEMA_PATH}")

    schema_sql = SCHEMA_PATH.read_text(encoding="utf-8")
    conn.execute(schema_sql)


def download_csv(url: str, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    response = requests.get(url, timeout=60)
    response.raise_for_status()

    with output_path.open("wb") as f:
        f.write(response.content)

    print(f"Descargado: {output_path}")

def connect_db() -> duckdb.DuckDBPyConnection:
    return duckdb.connect(str(DB_PATH))

def create_tables_maestras(conn: duckdb.DuckDBPyConnection) -> None:
    conn.execute(
        f"""
        CREATE OR REPLACE TABLE magnitudes AS
        SELECT
            CAST(CODIGO AS INTEGER) AS CODIGO,
            PARAMETRO,
            UNIDAD,
            CAST(COD_TECNICA AS INTEGER) AS COD_TECNICA,
            TECNICA
        FROM read_csv_auto('{MAESTRAS_DIR / "parametros_meteo.csv"}');
        """
    )

def download_and_store_meteo_data() -> None:
    conn = connect_db()
    try:
        ensure_schema(conn)
        create_tables_maestras(conn)
        store_meteo_data(conn)
        process_meteo_data(conn)
        print("Datos meteorológicos descargados y procesados correctamente.")
    finally:
        conn.close()

if __name__ == "__main__":
    download_and_store_meteo_data()