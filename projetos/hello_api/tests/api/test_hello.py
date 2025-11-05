import base64


class TestHelloEndpoint:
    """Test suite for /hello endpoint."""

    def test_hello_default(self, client):
        """Test /hello without path parameter returns 'Hello World'."""
        response = client.get("/hello")
        assert response.status_code == 200
        assert response.json() == {"message": "Hello World"}

    def test_hello_with_simple_word(self, client):
        """Test /hello with simple lowercase word."""
        response = client.get("/hello/batata")
        assert response.status_code == 200
        assert response.json() == {"message": "Hello Batata"}

    def test_hello_with_another_simple_word(self, client):
        """Test /hello with another simple lowercase word."""
        response = client.get("/hello/foobar")
        assert response.status_code == 200
        assert response.json() == {"message": "Hello Foobar"}

    def test_hello_with_camel_case(self, client):
        """Test /hello with CamelCase word - should add spaces."""
        response = client.get("/hello/MyHolyMother")
        assert response.status_code == 200
        assert response.json() == {"message": "Hello My holy mother"}

    def test_hello_with_uppercase_word(self, client):
        """Test /hello with all uppercase word."""
        response = client.get("/hello/PYTHON")
        assert response.status_code == 200
        assert response.json() == {"message": "Hello Python"}

    def test_hello_with_mixed_case(self, client):
        """Test /hello with mixed case variations."""
        response = client.get("/hello/HelloWorld")
        assert response.status_code == 200
        assert response.json() == {"message": "Hello Hello world"}

    def test_hello_counter_increments(self, client):
        """Test that calling /hello increments the counter."""
        # Call the endpoint multiple times
        client.get("/hello/test")
        client.get("/hello/test")
        client.get("/hello/test")

        # Get authenticated client to check history
        credentials = base64.b64encode(b"admin:Batata123").decode()
        response = client.get(
            "/history", headers={"Authorization": f"Basic {credentials}"}
        )

        assert response.status_code == 200
        history = response.json()
        assert "/hello/test" in history
        assert history["/hello/test"] == 3

    def test_hello_different_paths_tracked_separately(self, client):
        """Test that different paths are tracked separately in history."""
        client.get("/hello/foo")
        client.get("/hello/bar")
        client.get("/hello/foo")

        credentials = base64.b64encode(b"admin:Batata123").decode()
        response = client.get(
            "/history", headers={"Authorization": f"Basic {credentials}"}
        )

        assert response.status_code == 200
        history = response.json()
        assert history["/hello/foo"] == 2
        assert history["/hello/bar"] == 1


class TestHistoryEndpoint:
    """Test suite for /history endpoint."""

    def test_history_without_auth(self, client):
        """Test /history without authentication returns 401."""
        response = client.get("/history")
        assert response.status_code == 401
        assert "WWW-Authenticate" in response.headers

    def test_history_with_wrong_password(self, client):
        """Test /history with incorrect password returns 401."""
        credentials = base64.b64encode(b"admin:WrongPassword").decode()
        response = client.get(
            "/history", headers={"Authorization": f"Basic {credentials}"}
        )
        assert response.status_code == 401

    def test_history_with_wrong_username(self, client):
        """Test /history with incorrect username returns 401."""
        credentials = base64.b64encode(b"wronguser:Batata123").decode()
        response = client.get(
            "/history", headers={"Authorization": f"Basic {credentials}"}
        )
        assert response.status_code == 401

    def test_history_with_correct_auth(self, authenticated_client):
        """Test /history with correct authentication returns history."""
        response = authenticated_client.get("/history")
        assert response.status_code == 200
        assert isinstance(response.json(), dict)

    def test_history_returns_empty_dict_initially(self, authenticated_client):
        """Test /history returns empty dict when no requests have been made."""
        response = authenticated_client.get("/history")
        assert response.status_code == 200
        assert response.json() == {}

    def test_history_tracks_requests(self, client, authenticated_client):
        """Test that /history correctly tracks all requests."""
        # Make some requests
        client.get("/hello")
        client.get("/hello/python")
        client.get("/hello/python")
        client.get("/hello/devops")

        # Check history
        response = authenticated_client.get("/history")
        assert response.status_code == 200

        history = response.json()
        assert len(history) == 3
        assert history["/hello"] == 1
        assert history["/hello/python"] == 2
        assert history["/hello/devops"] == 1

    def test_history_with_malformed_auth_header(self, client):
        """Test /history with malformed Authorization header."""
        response = client.get(
            "/history", headers={"Authorization": "NotBasic credentials"}
        )
        assert response.status_code == 401

    def test_history_with_invalid_base64(self, client):
        """Test /history with invalid base64 in Authorization header."""
        response = client.get(
            "/history", headers={"Authorization": "Basic not-valid-base64!!!"}
        )
        assert response.status_code == 401

    def test_authenticated_client_fixture(self, authenticated_client):
        """Test that authenticated_client fixture works correctly."""
        response = authenticated_client.get("/history")
        assert response.status_code == 200


class TestDatabaseIsolation:
    """Test suite to verify database isolation between tests."""

    def test_database_starts_empty(self, authenticated_client):
        """Test that each test starts with an empty database."""
        response = authenticated_client.get("/history")
        assert response.status_code == 200
        assert response.json() == {}

    def test_database_still_empty_in_new_test(self, authenticated_client):
        """Test that database is empty even in a different test (isolation)."""
        response = authenticated_client.get("/history")
        assert response.status_code == 200
        assert response.json() == {}
