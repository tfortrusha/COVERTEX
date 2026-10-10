import sqlite3
from datetime import datetime

DB_FILE = "../data/covortex_audit.db"


def initialize_database():
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS audit_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        sender TEXT,
        receiver TEXT,
        event TEXT,
        message_id TEXT,
        status TEXT
    )
    """)

    connection.commit()
    connection.close()


def log_event(sender, receiver, event, message_id, status):
    connection = sqlite3.connect(DB_FILE)
    cursor = connection.cursor()

    cursor.execute("""
    INSERT INTO audit_logs
    (timestamp, sender, receiver, event, message_id, status)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        datetime.now().isoformat(),
        sender,
        receiver,
        event,
        message_id,
        status
    ))

    connection.commit()
    connection.close()