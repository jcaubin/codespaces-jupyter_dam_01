import pandas as pd

from src.portus_data import  get_portus_current_data

def test_get_portus_current_data_returns_current_data_as_dataframe():
    fecha_ejecucion = pd.Timestamp.now(tz="UTC").floor("h")

    rdf = get_portus_current_data(station=2820)

    fecha_maxima = pd.to_datetime(rdf["fecha"], utc=True).max()

    assert isinstance(rdf, pd.DataFrame)
    assert fecha_maxima == fecha_ejecucion 