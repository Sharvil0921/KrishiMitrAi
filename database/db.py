import sqlite3
import os
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# Database file lives at the project root
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'kisanmitr.db')


def get_conn():
    """Return a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Create tables if they don't exist yet."""
    with get_conn() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS farmers (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                name         TEXT    NOT NULL,
                mobile       TEXT    NOT NULL UNIQUE,
                password_hash TEXT   NOT NULL,
                created_at   TEXT    DEFAULT (datetime('now','localtime'))
            );

            CREATE TABLE IF NOT EXISTS chat_history (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                farmer_id    INTEGER NOT NULL,
                user_message TEXT    NOT NULL,
                bot_response TEXT    NOT NULL,
                intent       TEXT,
                timestamp    TEXT    DEFAULT (datetime('now','localtime')),
                FOREIGN KEY (farmer_id) REFERENCES farmers(id)
            );
        """)


def register_farmer(name: str, mobile: str, password: str):
    """
    Register a new farmer.
    Returns the new farmer's row dict on success, or None if mobile already exists.
    """
    pw_hash = generate_password_hash(password)
    try:
        with get_conn() as conn:
            conn.execute(
                "INSERT INTO farmers (name, mobile, password_hash) VALUES (?, ?, ?)",
                (name.strip(), mobile.strip(), pw_hash)
            )
            row = conn.execute(
                "SELECT * FROM farmers WHERE mobile = ?", (mobile.strip(),)
            ).fetchone()
            return dict(row)
    except sqlite3.IntegrityError:
        return None  # mobile already registered


def login_farmer(mobile: str, password: str):
    """
    Verify credentials.
    Returns the farmer's row dict on success, or None on failure.
    """
    with get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM farmers WHERE mobile = ?", (mobile.strip(),)
        ).fetchone()
    if row and check_password_hash(row['password_hash'], password):
        return dict(row)
    return None


def save_message(farmer_id: int, user_msg: str, bot_resp: str, intent: str):
    """Persist a single Q&A exchange for the given farmer."""
    conn = get_conn()
    try:
        conn.execute(
            """INSERT INTO chat_history
               (farmer_id, user_message, bot_response, intent)
               VALUES (?, ?, ?, ?)""",
            (farmer_id, user_msg, bot_resp, intent)
        )
        conn.commit()
    finally:
        conn.close()


def get_history(farmer_id: int, limit: int = 50):
    """Return the last `limit` messages for a farmer, oldest-first."""
    with get_conn() as conn:
        rows = conn.execute(
            """SELECT user_message, bot_response, intent, timestamp
               FROM chat_history
               WHERE farmer_id = ?
               ORDER BY id DESC
               LIMIT ?""",
            (farmer_id, limit)
        ).fetchall()
    return [dict(r) for r in reversed(rows)]
