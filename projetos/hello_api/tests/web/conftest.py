import socket
import subprocess
import time
from pathlib import Path

import httpx
import pytest


def is_port_in_use(port: int) -> bool:
    """Check if a port is already in use."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(("localhost", port))
            return False
        except OSError:
            return True


def wait_for_api(url: str, timeout: int = 10) -> bool:
    """Wait for the API to become available."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = httpx.get(url, timeout=1.0)
            if response.status_code == 200:
                return True
        except (httpx.ConnectError, httpx.TimeoutException):
            time.sleep(0.5)
    return False


@pytest.fixture(scope="session", autouse=True)
def api_server():
    """
    Ensure the FastAPI server is running for web tests.

    This fixture will:
    1. Check if the API is already running on port 8000
    2. If not, start it using uvicorn
    3. Wait for it to become available
    4. Yield control to the tests
    5. Clean up by terminating the server process if we started it
    """
    api_url = "http://localhost:8000"
    port = 8000
    process = None

    # Check if API is already running
    if is_port_in_use(port):
        print(f"\nAPI already running on port {port}")
        already_running = True
    else:
        print(f"\nStarting API on port {port}")
        already_running = False

        # Get the project root (where app.py is located)
        project_root = Path(__file__).parent.parent.parent

        # Start the API server
        process = subprocess.Popen(
            ["uvicorn", "app:app", "--host", "localhost", "--port", str(port)],
            cwd=project_root,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        # Wait for the API to become available
        if not wait_for_api(api_url):
            if process:
                process.terminate()
                process.wait()
            pytest.fail("Failed to start API server")

        print("API server is ready")

    # Yield to run tests
    yield

    # Cleanup: terminate the process if we started it
    if not already_running and process:
        print("\nShutting down API server")
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()
