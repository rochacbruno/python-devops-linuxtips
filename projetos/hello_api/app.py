import base64
import re
import sqlite3
from contextlib import contextmanager
from pathlib import Path

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, RootModel

app = FastAPI()

# Database path
DB_PATH = Path("history.db")

# Hardcoded credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "Batata123"

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


class ResponseModel(BaseModel):
    message: str


@app.get("/hello")
@app.get("/hello/{word}")
async def hello(word: str = "world") -> ResponseModel:
    """
    Return a greeting message with the formatted word.

    Args:
        word: The word to include in the greeting (default: "world")

    Returns:
        JSON response with the greeting message
    """
    formatted_word = format_word(word)
    path = f"/hello/{word}" if word != "world" else "/hello"

    # Track the request in history
    increment_counter(path)

    return ResponseModel(message=f"Hello {formatted_word}")


class HistoryResponse(RootModel[dict[str, int]]): ...


@app.get("/history", response_model=HistoryResponse)
async def history(authorization: str | None = Header(None)) -> dict:
    """
    Return the request history.

    Requires Basic Authentication with admin:Batata123

    Returns:
        JSON response with path counters
    """

    if not verify_basic_auth(authorization):
        raise HTTPException(
            status_code=401,
            detail="Unauthorized",
            headers={"WWW-Authenticate": "Basic"},
        )

    return get_history()
