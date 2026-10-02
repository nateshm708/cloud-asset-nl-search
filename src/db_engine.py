import sqlite3
import os
import pandas as pd

DB_PATH = os.path.join("data", "cloud_inventory.db")

def execute_query(sql_query: str) -> pd.DataFrame:
    """
    Executes a read-only SQL query against the SQLite cloud inventory database.
    Returns the result set as a Pandas DataFrame.
    """
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(
            f"Database file not found at '{DB_PATH}'. Run 'python db/init_db.py' first."
        )

    conn = sqlite3.connect(DB_PATH)
    try:
        df = pd.read_sql_query(sql_query, conn)
        return df
    except Exception as e:
        raise RuntimeError(f"Database query error: {str(e)}")
    finally:
        conn.close()