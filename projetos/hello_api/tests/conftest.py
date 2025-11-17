import base64
import tempfile
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

import app as app_module
import core as core_module


@pytest.fixture(scope="function", autouse=True)
def use_test_database(monkeypatch):
    """
    Fixture to enforce tests to run on a test database.

    This fixture is automatically used for all tests (autouse=True).
    It creates a temporary database file and patches the DB_PATH.
    Each test gets its own fresh database.
    """
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp_file:
        test_db_path = Path(tmp_file.name)

    # Patch the DB_PATH in the core module BEFORE creating the client
    monkeypatch.setattr(core_module, "DB_PATH", test_db_path)

    # Reset the database initialization flag
    monkeypatch.setattr(core_module, "_db_initialized", False)

    # Initialize the test database
    core_module.init_db(test_db_path)

    yield test_db_path

    # Reset the flag after the test
    core_module._db_initialized = False

    # Cleanup: remove the test database file
    if test_db_path.exists():
        test_db_path.unlink()


@pytest.fixture
def client():
    """
    Fixture that returns a TestClient without authentication.

    Returns:
        TestClient: FastAPI test client
    """
    # Use raise_server_exceptions=False to not raise exceptions during tests
    # This allows us to test error responses properly
    return TestClient(app_module.app, raise_server_exceptions=False)


@pytest.fixture
def authenticated_client():
    """
    Fixture that returns a TestClient with Basic Auth credentials.

    The client has admin:Batata123 properly encoded in the Authorization header.

    Returns:
        TestClient: FastAPI test client with authentication headers
    """
    # Encode credentials
    credentials = f"{core_module.ADMIN_USERNAME}:{core_module.ADMIN_PASSWORD}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()

    test_client = TestClient(app_module.app, raise_server_exceptions=False)
    # Add Authorization header
    test_client.headers.update({"Authorization": f"Basic {encoded_credentials}"})

    return test_client
