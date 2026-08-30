import duckdb
import pandas as pd
import pytest

from src.pato_calair_data import (
    ULR_CALAIR_CSV,
    URL_ESTACIONES_METEO,
    URL_METEO_CSV,
    download_csv_as_dataframe,
    store_meteo_data,
)


class DummyResponse:
    def __init__(self, text: str):
        self.text = text
        self.encoding = None
        self.apparent_encoding = "utf-8"

    def raise_for_status(self):
        return None


@pytest.mark.parametrize(
    ("csv_data", "separator", "decimal", "expected"),
    [
        (
            "nombre,valor\nMadrid,10\nSevilla,20\n",
            ",",
            ".",
            {"nombre": ["Madrid", "Sevilla"], "valor": [10, 20]},
        ),
        (
            "nombre;valor\nMadrid;10\nSevilla;20\n",
            ";",
            ".",
            {"nombre": ["Madrid", "Sevilla"], "valor": [10, 20]},
        ),
        (
            'nombre,valor\nMadrid,"10,5"\nSevilla,"20,5"\n',
            ",",
            ",",
            {"nombre": ["Madrid", "Sevilla"], "valor": [10.5, 20.5]},
        ),
        (
            'nombre;valor\nMadrid;"10,5"\nSevilla;"20,5"\n',
            ";",
            ",",
            {"nombre": ["Madrid", "Sevilla"], "valor": [10.5, 20.5]},
        ),
    ],
)
def test_download_csv_as_dataframe_supports_separator_and_decimal_variants(
    monkeypatch, csv_data, separator, decimal, expected
):
    def fake_get(url: str, timeout: int):
        assert url == "https://example.com/datos.csv"
        assert timeout == 60
        return DummyResponse(csv_data)

    monkeypatch.setattr("requests.get", fake_get)

    df = download_csv_as_dataframe(
        "https://example.com/datos.csv",
        separator=separator,
        decimal=decimal,
    )

    assert isinstance(df, pd.DataFrame)
    assert df.to_dict("list") == expected


def test_store_meteo_data_creates_expected_tables(monkeypatch):
    def fake_download_csv_as_dataframe(url: str, separator: str = ",", decimal: str = "."):
        data = {
            URL_METEO_CSV: pd.DataFrame(
                [{"ESTACION": 1, "TEMPERATURA": 18.5, "HUMEDAD": 65.0}]
            ),
            URL_ESTACIONES_METEO: pd.DataFrame(
                [{"CODIGO": 1, "NOMBRE": "Estación 1", "ALTITUD": 600}]
            ),
            ULR_CALAIR_CSV: pd.DataFrame(
                [{
                    "PROVINCIA": 28,
                    "MUNICIPIO": 79,
                    "ESTACION": 11,
                    "MAGNITUD": 12,
                    "H01": 0,
                    "V01": "N",
                }]
            ),
        }
        return data[url].copy()

    monkeypatch.setattr(
        "src.pato_calair_data.download_csv_as_dataframe",
        fake_download_csv_as_dataframe,
    )

    conn = duckdb.connect(":memory:")

    store_meteo_data(conn)

    tables = {row[0] for row in conn.execute("SHOW TABLES").fetchall()}
    assert {"METEO2", "ESTACIONES_METEO2", "CALAIR2"}.issubset(tables)
    assert conn.execute("SELECT COUNT(*) FROM METEO2").fetchone()[0] == 1
    assert conn.execute("SELECT COUNT(*) FROM ESTACIONES_METEO2").fetchone()[0] == 1
    assert conn.execute("SELECT COUNT(*) FROM CALAIR2").fetchone()[0] == 1
    assert "FX_DATA" in conn.execute("DESCRIBE METEO2").fetchdf()["column_name"].tolist()