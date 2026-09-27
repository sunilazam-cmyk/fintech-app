import sqlite3
import pandas as pd
from datetime import datetime

DB_FILE = "fintech_app.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS calculator_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            calculator_type TEXT,
            input_summary TEXT,
            result_summary TEXT
        )
    ''')
    conn.commit()
    conn.close()

def log_calculator_activity(calculator_type: str, input_summary: str, result_summary: str):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO calculator_history (timestamp, calculator_type, input_summary, result_summary)
        VALUES (?, ?, ?, ?)
    ''', (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), calculator_type, input_summary, result_summary))
    conn.commit()
    conn.close()

def get_calculator_history() -> pd.DataFrame:
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query("SELECT timestamp as 'Timestamp', calculator_type as 'Calculator', input_summary as 'Inputs', result_summary as 'Results' FROM calculator_history ORDER BY id DESC", conn)
    conn.close()
    return df


