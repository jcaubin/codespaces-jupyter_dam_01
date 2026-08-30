from datetime import datetime

import duckdb
import pandas as pd

from src.pato_calair_data import (
    DB_PATH,
    ULR_CALAIR_CSV,
    URL_ESTACIONES_METEO,
    URL_METEO_CSV,
    download_csv_as_dataframe,
    store_meteo_data,
)


def test_download_csv_as_dataframe_real_url_returns_expected_shape():
    df = download_csv_as_dataframe(ULR_CALAIR_CSV, separator=';', decimal='.')

    assert isinstance(df, pd.DataFrame)
    assert len(df.index) == 123
    assert len(df.columns) == 56


def test_download_csv_as_dataframe_meteo():
    df = download_csv_as_dataframe(URL_METEO_CSV, separator=';', decimal='.')

    assert isinstance(df, pd.DataFrame)
    assert len(df.index) == 87
    assert len(df.columns) == 56


def test_store_meteo_data_persists_to_database_with_expected_fx_data(monkeypatch):
    expected_dt = datetime(2024, 1, 2, 3, 4, 5)

    class FrozenDateTime(datetime):
        @classmethod
        def now(cls, tz=None):
            return expected_dt

    monkeypatch.setattr("src.pato_calair_data.datetime", FrozenDateTime)

    conn = duckdb.connect(DB_PATH)
    try:
        for table in ["METEO2", "ESTACIONES_METEO2", "CALAIR2"]:
            conn.execute(f"DROP TABLE IF EXISTS {table}")

        store_meteo_data(conn)

        tables = {row[0] for row in conn.execute("SHOW TABLES").fetchall()}
        assert {"METEO2", "ESTACIONES_METEO2", "CALAIR2"}.issubset(tables)

        for table in ["METEO2", "ESTACIONES_METEO2", "CALAIR2"]:
            count = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            assert count > 0

            values = conn.execute(f"SELECT DISTINCT FX_DATA FROM {table}").fetchall()
            assert len(values) == 1
            assert values[0][0] == expected_dt
    finally:
        cleanup_tables = []#["METEO2", "ESTACIONES_METEO2", "CALAIR2"]
        for table in cleanup_tables:
            conn.execute(f"DROP TABLE IF EXISTS {table}")
        conn.close()