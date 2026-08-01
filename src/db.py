import duckdb
from pathlib import Path
from config import DB_PATH, SQL_DIR, DATA_DIR

SQL_FILES = [
    "001_schema.sql",
    "002_views.sql",
]

def connect(db_path: Path = DB_PATH) -> duckdb.DuckDBPyConnection:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    return duckdb.connect(str(db_path))

def init_schema(conn: duckdb.DuckDBPyConnection) -> None:
    for file_name in SQL_FILES:
        sql_file = SQL_DIR / file_name
        conn.execute(sql_file.read_text(encoding="utf-8"))

if __name__ == "__main__": 
    conn = connect()
    init_schema(conn)
    conn.close()
    