import duckdb
from pathlib import Path
from .config import DB_PATH, SQL_DIR, DATA_DIR

def connect(db_path: Path = DB_PATH) -> duckdb.DuckDBPyConnection:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    return duckdb.connect(str(db_path))

def init_schema(conn: duckdb.DuckDBPyConnection) -> None:
    for sql_file in sorted(SQL_DIR.glob("*.sql")):
        conn.execute(sql_file.read_text(encoding="utf-8"))