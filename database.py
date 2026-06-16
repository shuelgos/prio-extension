import sqlite3
from datetime import datetime
from config import DATABASE_URL

#Conectamos a la base de datos
def get_connection():
    conn = sqlite3.connect(DATABASE_URL)
    conn.row_factory = sqlite3.Row  # devuelve filas como diccionarios
    return conn


def init_db():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS classifications (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            email_subject TEXT NOT NULL,
            area        TEXT NOT NULL,
            urgencia    TEXT NOT NULL,
            resumen     TEXT NOT NULL,
            created_at  TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

# Guardar una clasificación nueva

def save_classification(email_subject: str, area: str, urgencia: str, resumen: str):
    conn = get_connection()
    conn.execute("""
        INSERT INTO classifications (email_subject, area, urgencia, resumen, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, (email_subject, area, urgencia, resumen, datetime.now().isoformat()))
    conn.commit()
    conn.close()

# Obtener todas las clasificaciones
def get_classifications(limit: int = 50):
    conn = get_connection()
    cursor = conn.execute("""
        SELECT * FROM classifications
        ORDER BY created_at DESC
        LIMIT ?
    """, (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]