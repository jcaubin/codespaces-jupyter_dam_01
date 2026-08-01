from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
MAESTRAS_DIR = PROJECT_ROOT / "maestras"
SQL_DIR = PROJECT_ROOT / "sql"

DB_PATH = DATA_DIR / "duck_test.db"

URLS = {
    "meteo": "https://datos.madrid.es/egob/catalogo/300392-11041819-meteorologia-tiempo-real.csv",
    "calair": "https://datos.madrid.es/egob/catalogo/212531-10515086-calidad-aire-tiempo-real.csv",
    "estaciones": "https://datos.madrid.es/egob/catalogo/300360-1-meteorologicos-estaciones.csv",
}

MAGNITUDES_CSV = MAESTRAS_DIR / "parametros_meteo.csv"