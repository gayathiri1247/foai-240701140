import sqlite3
from config import DATABASE_PATH

def get_db():
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(DATABASE_PATH)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys = ON")
    return db

def init_db():
    with get_db() as db:
        db.executescript("""
        CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS applications(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            reference_id TEXT NOT NULL UNIQUE,
            user_id INTEGER NOT NULL,
            loan_type TEXT NOT NULL,
            submitted_at TEXT NOT NULL,
            applicant_data_json TEXT NOT NULL,
            decision TEXT NOT NULL,
            explanation_summary TEXT NOT NULL,
            emi REAL,
            FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
        );
        CREATE TABLE IF NOT EXISTS rule_results(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            application_id INTEGER NOT NULL,
            rule_id TEXT NOT NULL,
            status TEXT NOT NULL,
            explanation TEXT NOT NULL,
            verification_status TEXT NOT NULL,
            source_url TEXT NOT NULL,
            FOREIGN KEY(application_id) REFERENCES applications(id) ON DELETE CASCADE
        );
        """)
