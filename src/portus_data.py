#Descarga de datos de portus

import pandas as pd
import requests
from pathlib import Path
import duckdb
from io import StringIO 
from datetime import datetime

URL_PORTUS = "https://portus.puertos.es/portussvr/api/lastData/station"
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
DB_PATH = DATA_DIR / 'duck_test.db'



def get_portus_current_data(station: int=2820) -> pd.DataFrame:
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    params = {
        "locale": "es",
    }
    payload = ["WATER_TEMP"]
    url_api = f"{URL_PORTUS}/{station}"
    response = requests.post(url_api, headers=headers, params=params, json=payload)
    response.raise_for_status()  # Raise an exception for HTTP errors
    data = response.json()
    df = pd.DataFrame(data["datos"])
    df.insert(0, "fecha", pd.to_datetime(data["fecha"]))
    df.insert(1, "station", station)
    return df   


def store_portus_data(conn: duckdb.DuckDBPyConnection) -> None:
    try:
        fx_data = datetime.now()

        df_portus = get_portus_current_data(station=2820)
        df_portus['FX_DATA'] = fx_data
        conn.register('df_portus', df_portus)
        conn.execute("CREATE OR REPLACE TABLE PORTUS_CURRENT_DATA AS SELECT * FROM df_portus")
        print("Datos de portus cargados correctamente en la tabla 'portus'.")

    except Exception as e:
        print(f"Error al obtener los datos DE PORTUS: {e}")
        raise


def process_portus_data(conn: duckdb.DuckDBPyConnection) -> None:
    try:
                # Inserta los datos procesados en la tabla portus
        conn.execute(
            """
            INSERT OR REPLACE INTO PORTUS BY NAME
            SELECT 
                fecha, station, id, nombreParametro, nombreColumna, paramEseoo, valor, factor, unidad, paramQC, "variable", averia, FX_DATA
            FROM PORTUS_CURRENT_DATA;
            """
        )
        print("Datos de portus procesados correctamente.")
    except Exception as e:
        print(f"Error al procesar los datos de portus: {e}")
        raise



def connect_db() -> duckdb.DuckDBPyConnection:
    return duckdb.connect(str(DB_PATH))

def download_and_store_portus_data() -> None:
    conn = connect_db()
    try:
        store_portus_data(conn)
        process_portus_data(conn)
        print("Datos de portus descargados y procesados correctamente.")
    except Exception as e:
        print(f"Error al descargar y procesar los datos de portus: {e}")    
    finally:
        conn.close()

if __name__ == "__main__":
    download_and_store_portus_data()    