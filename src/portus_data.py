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

ESTACIONES_PORTUS =  [
	{
		"id" : 1101,
		"nombre" : "Boya de Pasaia II"
	},
	{
		"id" : 1103,
		"nombre" : "Boya Costera de Bilbao II"
	},
	{
		"id" : 1117,
		"nombre" : "Boya de Gijon"
	},
	{
		"id" : 1135,
		"nombre" : "Boya Costera de Abra-Zierbena"
	},
	{
		"id" : 1239,
		"nombre" : "Boya de Langosteira II"
	},
	{
		"id" : 1250,
		"nombre" : "Plataforma de Cortegada-CETMAR-INTECMAR-MG"
	},
	{
		"id" : 1251,
		"nombre" : "Plataforma de Rande-CETMAR-INTECMAR-MG"
	},
	{
		"id" : 1253,
		"nombre" : "Boya de A Guarda-CETMAR-INTECMAR-MG"
	},
	{
		"id" : 1255,
		"nombre" : "Boya de Ribeira-CETMAR-INTECMAR-MG"
	},
	{
		"id" : 1256,
		"nombre" : "Boya de Muros-CETMAR-INTECMAR-MG"
	},
	{
		"id" : 1315,
		"nombre" : "Boya de Sevilla-Guadalquivir"
	},
	{
		"id" : 1414,
		"nombre" : "Boya de Las Palmas Este"
	},
	{
		"id" : 1421,
		"nombre" : "Boya de Santa Cruz de Tenerife"
	},
	{
		"id" : 1500,
		"nombre" : "Boya de Tarifa"
	},
	{
		"id" : 1504,
		"nombre" : "Boya de Algeciras-Pta. Carnero"
	},
	{
		"id" : 1512,
		"nombre" : "Boya de Ceuta"
	},
	{
		"id" : 1514,
		"nombre" : "Boya de Málaga"
	},
	{
		"id" : 1560,
		"nombre" : "Boya de Melilla"
	},
	{
		"id" : 1712,
		"nombre" : "Boya de Tarragona"
	},
	{
		"id" : 1731,
		"nombre" : "Boya de Barcelona II"
	},
	{
		"id" : 2136,
		"nombre" : "Boya de Bilbao-Vizcaya"
	},
	{
		"id" : 2242,
		"nombre" : "Boya de Cabo de Peñas"
	},
	{
		"id" : 2244,
		"nombre" : "Boya de Estaca de Bares"
	},
	{
		"id" : 2246,
		"nombre" : "Boya de Villano-Sisargas"
	},
	{
		"id" : 2248,
		"nombre" : "Boya de Cabo Silleiro"
	},
	{
		"id" : 2342,
		"nombre" : "Boya de Golfo de Cádiz"
	},
	{
		"id" : 2442,
		"nombre" : "Boya de Gran Canaria"
	},
	{
		"id" : 2446,
		"nombre" : "Boya de Tenerife Sur"
	},
	{
		"id" : 2548,
		"nombre" : "Boya de Cabo de Gata"
	},
	{
		"id" : 2610,
		"nombre" : "Boya de Cabo de Palos"
	},
	{
		"id" : 2630,
		"nombre" : "Boya de Valencia"
	},
	{
		"id" : 2720,
		"nombre" : "Boya de Tarragona"
	},
	{
		"id" : 2798,
		"nombre" : "Boya de Cabo Begur"
	},
	{
		"id" : 2801,
		"nombre" : "Boya Bahía de Palma SOCIB"
	},
	{
		"id" : 2820,
		"nombre" : "Boya de Dragonera"
	},
	{
		"id" : 2838,
		"nombre" : "Boya de Mahón"
	},
	{
		"id" : 3801,
		"nombre" : "Mareografo de Andratx-SOCIB"
	},
	{
		"id" : 3802,
		"nombre" : "Mareografo de Pollença-SOCIB"
	},
	{
		"id" : 3803,
		"nombre" : "Mareografo de Sa Rapita-SOCIB"
	},
	{
		"id" : 12110,
		"nombre" : "Boya MONICAN01-IHP"
	},
	{
		"id" : 12115,
		"nombre" : "Boya MONICAN02-IHP"
	},
	{
		"id" : 12120,
		"nombre" : "Boya Raia01-IHP"
	},
	{
		"id" : 12125,
		"nombre" : "Boya Faro"
	},
	{
		"id" : 21003,
		"nombre" : "Boya Galway-MI"
	},
	{
		"id" : 22091,
		"nombre" : "Boya M2 E of Lambay-MI"
	},
	{
		"id" : 22092,
		"nombre" : "Boya M3 SW of Mizen Head-MI"
	},
	{
		"id" : 22093,
		"nombre" : "Boya M4 Donegal Bay-MI"
	},
	{
		"id" : 22094,
		"nombre" : "Boya M5 South East-MI"
	},
	{
		"id" : 32001,
		"nombre" : "Boya de Gascogne-UKMOMF"
	},
	{
		"id" : 32029,
		"nombre" : "Boya K1-UKMO"
	},
	{
		"id" : 32052,
		"nombre" : "Boya 62052-MF"
	},
	{
		"id" : 32081,
		"nombre" : "Boya K2-UKMO"
	},
	{
		"id" : 32103,
		"nombre" : "Barco Channel-UKMO"
	},
	{
		"id" : 32105,
		"nombre" : "Boya K4-UKMO"
	},
	{
		"id" : 32107,
		"nombre" : "Barco Seven Stones-UKMO"
	},
	{
		"id" : 32163,
		"nombre" : "Boya Brittany-UKMOMF"
	},
	{
		"id" : 32301,
		"nombre" : "Boya Aberporth-UKMO"
	},
	{
		"id" : 32303,
		"nombre" : "Boya Turbot Bank-UKMO"
	},
	{
		"id" : 32304,
		"nombre" : "Barco Sandettie-UKMO"
	},
	{
		"id" : 32305,
		"nombre" : "Barco Greenwich-UKMO"
	},
	{
		"id" : 34045,
		"nombre" : "Boya K5-UKMO"
	},
	{
		"id" : 34046,
		"nombre" : "Boya K7-UKMO"
	}
]


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
        conn.execute("TRUNCATE TABLE PORTUS_CURRENT_DATA")
        for estacion in ESTACIONES_PORTUS:
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
        store_portus_estaciones(conn)
        print("Datos de portus descargados y procesados correctamente.")
    except Exception as e:
        print(f"Error al descargar y procesar los datos de portus: {e}")    
    finally:
        conn.close()

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


if __name__ == "__main__":
    download_and_store_portus_data()    