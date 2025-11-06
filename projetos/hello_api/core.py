"""Core functionality for the Hello API application.

This module contains all business logic, database operations, authentication,
and utility functions used by the FastAPI application.
"""

import base64
import re
import sqlite3
from contextlib import contextmanager
from pathlib import Path

from config import ADMIN_PASSWORD, ADMIN_USERNAME, DB_PATH

# Track if database is initialized
_db_initialized = False


@contextmanager
def get_db_connection(db_path: Path | None = None):
    """Context manager for database connections."""

    if db_path is None:
        db_path = DB_PATH
    conn = sqlite3.connect(db_path)
    try:
        yield conn
    finally:
        conn.close()


def init_db(db_path: Path | None = None):
    """Initialize the database with the history table."""
    global _db_initialized

    if db_path is None:
        db_path = DB_PATH

    with get_db_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS history (
                path TEXT PRIMARY KEY,
                count INTEGER DEFAULT 0
            )
            """
        )
        conn.commit()
    _db_initialized = True


def ensure_db_initialized(db_path: Path | None = None):
    """Ensure database is initialized before use."""
    global _db_initialized

    if not _db_initialized:
        init_db(db_path)


def increment_counter(path: str, db_path: Path | None = None):
    """Increment the counter for a given path."""
    ensure_db_initialized(db_path)
    with get_db_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO history (path, count) VALUES (?, 1)
            ON CONFLICT(path) DO UPDATE SET count = count + 1
            """,
            (path,),
        )
        conn.commit()


def get_history(db_path: Path | None = None) -> dict:
    """Retrieve the complete history."""
    ensure_db_initialized(db_path)
    with get_db_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT path, count FROM history")

        return dict(cursor.fetchall())


def format_word(word: str) -> str:
    """
    Format a word by capitalizing it and adding spaces before uppercase letters.

    Examples:
        batata -> Batata
        foobar -> Foobar
        MyHolyMother -> My Holy Mother
        PYTHON -> Python
    """
    # If word is all uppercase, convert to lowercase first

    if word.isupper() and len(word) > 1:
        word = word.lower()

    # Add space before uppercase letters (except the first one)
    spaced = re.sub(r"(?<!^)(?=[A-Z])", " ", word)
    # Capitalize the first letter

    return spaced.capitalize()


def verify_basic_auth(authorization: str | None) -> bool:
    """Verify Basic Authentication credentials."""

    if not authorization:
        return False

    try:
        scheme, credentials = authorization.split()

        if scheme.lower() != "basic":
            return False

        decoded = base64.b64decode(credentials).decode("utf-8")
        username, password = decoded.split(":", 1)

        return username == ADMIN_USERNAME and password == ADMIN_PASSWORD
    except Exception:
        return False
