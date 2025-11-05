"""Unit tests for database functions in app.py."""

import sqlite3
import tempfile
from pathlib import Path

import pytest

from app import (
    ensure_db_initialized,
    get_db_connection,
    get_history,
    increment_counter,
    init_db,
)


def test_get_db_connection_creates_connection(use_test_database):
    """Test that get_db_connection creates a valid database connection."""
    with get_db_connection(use_test_database) as conn:
        assert isinstance(conn, sqlite3.Connection)
        # Verify connection works by executing a simple query
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        assert result == (1,)


def test_get_db_connection_closes_connection(use_test_database):
    """Test that get_db_connection closes the connection after use."""
    with get_db_connection(use_test_database) as conn:
        connection_obj = conn

    # After exiting context manager, connection should be closed
    with pytest.raises(sqlite3.ProgrammingError):
        connection_obj.execute("SELECT 1")


def test_init_db_creates_history_table(use_test_database):
    """Test that init_db creates the history table with correct schema."""
    # The use_test_database fixture already calls init_db, but let's verify
    with get_db_connection(use_test_database) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='history'
            """
        )
        result = cursor.fetchone()
        assert result is not None
        assert result[0] == "history"

        # Check table schema
        cursor.execute("PRAGMA table_info(history)")
        columns = cursor.fetchall()

        # Should have 2 columns: path (TEXT PRIMARY KEY) and count (INTEGER)
        assert len(columns) == 2
        assert columns[0][1] == "path"  # column name
        assert columns[0][2] == "TEXT"  # column type
        assert columns[1][1] == "count"
        assert columns[1][2] == "INTEGER"


def test_init_db_is_idempotent(use_test_database):
    """Test that calling init_db multiple times doesn't cause errors."""
    # First initialization already done by fixture
    # Call it again
    init_db(use_test_database)
    init_db(use_test_database)

    # Should still have a valid table
    with get_db_connection(use_test_database) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        # Should have exactly one table named 'history'
        assert len(tables) == 1
        assert tables[0][0] == "history"


def test_ensure_db_initialized_with_uninitialized_db(monkeypatch):
    """Test that ensure_db_initialized initializes an uninitialized database."""
    # Create a temporary database that hasn't been initialized
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp_file:
        test_db_path = Path(tmp_file.name)

    try:
        # Reset the initialization flag
        import app as app_module
        monkeypatch.setattr(app_module, "_db_initialized", False)

        # Call ensure_db_initialized
        ensure_db_initialized(test_db_path)

        # Verify the table was created
        with get_db_connection(test_db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='history'"
            )
            result = cursor.fetchone()
            assert result is not None
    finally:
        # Cleanup
        if test_db_path.exists():
            test_db_path.unlink()


def test_increment_counter_creates_new_entry(use_test_database):
    """Test that increment_counter creates a new entry for a path."""
    path = "/test/path"

    increment_counter(path, use_test_database)

    with get_db_connection(use_test_database) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT path, count FROM history WHERE path = ?", (path,))
        result = cursor.fetchone()

        assert result is not None
        assert result[0] == path
        assert result[1] == 1


def test_increment_counter_increments_existing_entry(use_test_database):
    """Test that increment_counter increments count for existing path."""
    path = "/test/path"

    # Increment multiple times
    increment_counter(path, use_test_database)
    increment_counter(path, use_test_database)
    increment_counter(path, use_test_database)

    with get_db_connection(use_test_database) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT count FROM history WHERE path = ?", (path,))
        result = cursor.fetchone()

        assert result is not None
        assert result[0] == 3


def test_increment_counter_handles_multiple_paths(use_test_database):
    """Test that increment_counter tracks different paths independently."""
    path1 = "/hello"
    path2 = "/hello/world"
    path3 = "/hello/python"

    increment_counter(path1, use_test_database)
    increment_counter(path1, use_test_database)
    increment_counter(path2, use_test_database)
    increment_counter(path3, use_test_database)
    increment_counter(path3, use_test_database)
    increment_counter(path3, use_test_database)

    with get_db_connection(use_test_database) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT path, count FROM history ORDER BY path")
        results = cursor.fetchall()

        assert len(results) == 3
        assert results[0] == (path1, 2)
        assert results[1] == (path3, 3)
        assert results[2] == (path2, 1)


def test_get_history_returns_empty_dict_for_empty_db(use_test_database):
    """Test that get_history returns an empty dict when no data exists."""
    history = get_history(use_test_database)

    assert isinstance(history, dict)
    assert len(history) == 0


def test_get_history_returns_all_entries(use_test_database):
    """Test that get_history returns all path-count entries."""
    # Add some test data
    paths_counts = {
        "/hello": 5,
        "/hello/world": 3,
        "/hello/python": 7,
        "/api/status": 1,
    }

    for path, count in paths_counts.items():
        for _ in range(count):
            increment_counter(path, use_test_database)

    history = get_history(use_test_database)

    assert isinstance(history, dict)
    assert history == paths_counts


def test_get_history_returns_dict_with_int_values(use_test_database):
    """Test that get_history returns integer counts."""
    increment_counter("/test", use_test_database)

    history = get_history(use_test_database)

    assert isinstance(history, dict)
    assert "/test" in history
    assert isinstance(history["/test"], int)
    assert history["/test"] == 1
