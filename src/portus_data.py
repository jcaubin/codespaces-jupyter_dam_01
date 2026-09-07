#Descarga de datos de portus

import pandas as pd
import requests
from pathlib import Path
import duckdb
from io import StringIO 
from datetime import datetime

URL_PORTUS = "https://portus.puertos.es/portussvr/api/lastData/station"
PORTUS_ESTACIONES_URL = "https://portus.puertos.es/portussvr/api/estaciones/rt/"
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
        estaciones = get_estaciones_from_db(conn)
        fx_data = datetime.now()
        conn.execute("TRUNCATE TABLE PORTUS_CURRENT_DATA")
        for estacion in estaciones:
            station_id = estacion["id"]
            df_portus = get_portus_current_data(station=station_id)
            df_portus['FX_DATA'] = fx_data
            if df_portus.shape[1]== 13:
                conn.register('df_portus', df_portus)
                conn.execute("INSERT INTO PORTUS_CURRENT_DATA SELECT * FROM df_portus")
                print(f"Datos de portus para la estación {station_id}, {estacion['nombre']} cargados correctamente en la tabla 'portus_current_data'.")
            else:
                print(f"Advertencia: Los datos de portus para la estación {station_id}, {estacion['nombre']} no tienen el formato esperado y no se han insertado en la tabla 'portus_current_data'.")
        print("Datos de portus cargados correctamente en la tabla 'portus'.")    
      
    except Exception as e:
        print(f"Error al obtener los datos DE PORTUS: {e}")
        raise

def get_estaciones_from_db(conn: duckdb.DuckDBPyConnection) -> list:	
	try:
		query = "SELECT id, nombre FROM PORTUS_ESTACIONES"
		df_estaciones = conn.execute(query).fetchdf()
		return df_estaciones.to_dict('records')
	except Exception as e:
		print(f"Error al obtener las estaciones de la base de datos: {e}")
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

def get_portus_estaciones() -> pd.DataFrame:
    magnitud = "WATER_TEMP"
    parameters = {
        "locale": "es",
    }
    request_url = f"{PORTUS_ESTACIONES_URL}/{magnitud}"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    response = requests.get(request_url, params=parameters, headers=headers)
    response.raise_for_status()  # Raise an exception for HTTP errors
    data = response.json()
    registros = data if isinstance(data, list) else [data]
    df = pd.json_normalize(registros, sep=".")
    return df

def store_portus_estaciones(conn: duckdb.DuckDBPyConnection) -> None:
    try:
        df_estaciones = get_portus_estaciones()
        df_estaciones['FX_DATA'] = datetime.now()
        conn.register('df_estaciones', df_estaciones)
        conn.execute("CREATE OR REPLACE TABLE PORTUS_ESTACIONES AS SELECT * FROM df_estaciones")
        print("Datos de estaciones de portus cargados correctamente en la tabla 'portus_estaciones'.")
    except Exception as e:
        print(f"Error al obtener los datos de estaciones de portus: {e}")
        raise

def connect_db() -> duckdb.DuckDBPyConnection:
    return duckdb.connect(str(DB_PATH))

def download_and_store_portus_data() -> None:
    conn = connect_db()
    try:
        store_portus_estaciones(conn) #descarga y guarda la lista de estaciones de portus en la tabla 'portus_estaciones'
        store_portus_data(conn) #descarga y guarda los datos de portus en la tabla 'portus_current_data'
        process_portus_data(conn) #procesa y guarda los datos de portus en la tabla 'portus'        
        print("Datos de portus descargados y procesados correctamente.")
    except Exception as e:
        print(f"Error al descargar y procesar los datos de portus: {e}")    
    finally:
        conn.close()

if __name__ == "__main__":
    download_and_store_portus_data()    