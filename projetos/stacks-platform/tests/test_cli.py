"""Tests for the Stacks CLI."""

import json
from unittest.mock import Mock, patch

import httpx
import pytest
from cyclopts.exceptions import CoercionError

from stacks_cli.main import cli, deploy, health, list


class TestCLIList:
    """Tests for the 'list' command."""

    @patch("stacks_cli.main.httpx.get")
    def test_list_success(self, mock_get, capsys):
        """Test list command with successful API response."""
        # Mock API response
        mock_response = Mock()
        mock_response.json.return_value = {
            "web-app-docker": {
                "params_schema": {
                    "properties": {
                        "name": {"type": "string"},
                        "base_image": {"type": "string"},
                        "ports": {"type": "array"},
                    },
                    "required": ["name", "base_image"],
                }
            }
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        # Execute command
        list()

        # Verify API call
        mock_get.assert_called_once_with(
            "http://localhost:8000/api/v1/stacks", timeout=10.0
        )

        # Verify output contains expected data
        captured = capsys.readouterr()
        assert "Stacks Disponíveis" in captured.out
        assert "web-app-docker" in captured.out

    @patch("stacks_cli.main.httpx.get")
    def test_list_connection_error(self, mock_get, capsys):
        """Test list command when API is unreachable."""
        mock_get.side_effect = httpx.ConnectError("Connection refused")

        # Execute command and expect exit
        with pytest.raises(SystemExit) as exc_info:
            list()

        assert exc_info.value.code == 1

        # Verify error message
        captured = capsys.readouterr()
        assert "Não foi possível conectar à API" in captured.out
        assert "uv run stacks-api" in captured.out

    @patch("stacks_cli.main.httpx.get")
    def test_list_http_error(self, mock_get, capsys):
        """Test list command with HTTP error."""
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Server error", request=Mock(), response=Mock()
        )
        mock_get.return_value = mock_response

        # Execute command and expect exit
        with pytest.raises(SystemExit) as exc_info:
            list()

        assert exc_info.value.code == 1

        # Verify error message
        captured = capsys.readouterr()
        assert "✗ Erro:" in captured.out


class TestCLIDeploy:
    """Tests for the 'deploy' command."""

    @patch("stacks_cli.main.httpx.post")
    def test_deploy_success_without_database(self, mock_post, capsys):
        """Test deploy command with successful response."""
        # Mock API response
        mock_response = Mock()
        mock_response.json.return_value = {
            "status": "success",
            "message": "Stack deployed successfully",
            "resources": {
                "containers": ["test-webapp"],
                "networks": ["test-network"],
            },
        }
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response

        # Execute command
        deploy(
            stack="web-app-docker",
            name="test-webapp",
            base_image="nginx:alpine",
            ports="8080,9090",
            with_database=False,
        )

        # Verify API call
        expected_params = {
            "name": "test-webapp",
            "base_image": "nginx:alpine",
            "ports": [8080, 9090],
            "with_database": False,
        }
        mock_post.assert_called_once_with(
            "http://localhost:8000/api/v1/deploy/web-app-docker",
            json=expected_params,
            timeout=300.0,
        )

        # Verify output
        captured = capsys.readouterr()
        assert "Deploy Concluído" in captured.out
        assert "✓" in captured.out
        assert "Recursos criados" in captured.out

    @patch("stacks_cli.main.httpx.post")
    def test_deploy_success_with_database(self, mock_post, capsys):
        """Test deploy command with database enabled."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "status": "success",
            "message": "Stack deployed with database",
        }
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response

        # Execute command
        deploy(
            stack="web-app-docker",
            name="test-webapp",
            base_image="nginx:alpine",
            ports="80",
            with_database=True,
        )

        # Verify database params were added
        call_args = mock_post.call_args
        payload = call_args.kwargs["json"]
        assert payload["with_database"] is True
        assert "database" in payload
        assert payload["database"]["image"] == "postgres:16-alpine"
        assert payload["database"]["port"] == 5432

    @patch("stacks_cli.main.httpx.post")
    def test_deploy_failure(self, mock_post, capsys):
        """Test deploy command with failed deployment."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "status": "failed",
            "message": "Deployment failed: port already in use",
        }
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response

        # Execute command and expect exit
        with pytest.raises(SystemExit) as exc_info:
            deploy(
                stack="web-app-docker",
                name="test-webapp",
                base_image="nginx:alpine",
                ports="80",
                with_database=False,
            )

        assert exc_info.value.code == 1

        # Verify error message
        captured = capsys.readouterr()
        assert "✗" in captured.out
        assert "port already in use" in captured.out

    @patch("stacks_cli.main.httpx.post")
    def test_deploy_connection_error(self, mock_post, capsys):
        """Test deploy command when API is unreachable."""
        mock_post.side_effect = httpx.ConnectError("Connection refused")

        # Execute command and expect exit
        with pytest.raises(SystemExit) as exc_info:
            deploy(
                stack="web-app-docker",
                name="test-webapp",
                base_image="nginx:alpine",
                ports="80",
                with_database=False,
            )

        assert exc_info.value.code == 1

        # Verify error message
        captured = capsys.readouterr()
        assert "Não foi possível conectar à API" in captured.out

    @patch("stacks_cli.main.httpx.post")
    def test_deploy_http_error(self, mock_post, capsys):
        """Test deploy command with HTTP error."""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.text = "Stack not found"
        mock_post.return_value = mock_response
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Not found", request=Mock(), response=mock_response
        )

        # Execute command and expect exit
        with pytest.raises(SystemExit) as exc_info:
            deploy(
                stack="invalid-stack",
                name="test-webapp",
                base_image="nginx:alpine",
                ports="80",
                with_database=False,
            )

        assert exc_info.value.code == 1

        # Verify error message (check parts separately due to ANSI color codes)
        captured = capsys.readouterr()
        assert "✗ Erro HTTP" in captured.out
        assert "404" in captured.out
        assert "Stack not found" in captured.out

    @patch("stacks_cli.main.httpx.post")
    def test_deploy_invalid_ports(self, mock_post, capsys):
        """Test deploy command with invalid port format."""
        # Invalid port causes ValueError which is caught and results in SystemExit
        with pytest.raises(SystemExit) as exc_info:
            deploy(
                stack="web-app-docker",
                name="test-webapp",
                base_image="nginx:alpine",
                ports="invalid,port",
                with_database=False,
            )

        assert exc_info.value.code == 1

        # Verify error message (check parts separately due to ANSI color codes)
        captured = capsys.readouterr()
        assert "✗ Erro:" in captured.out
        assert "invalid literal" in captured.out
        assert "'invalid'" in captured.out


class TestCLIHealth:
    """Tests for the 'health' command."""

    @patch("stacks_cli.main.httpx.get")
    def test_health_success(self, mock_get, capsys):
        """Test health command with healthy API."""
        # Mock API response
        mock_response = Mock()
        mock_response.json.return_value = {"status": "healthy"}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        # Execute command
        health()

        # Verify API call
        mock_get.assert_called_once_with(
            "http://localhost:8000/api/v1/health", timeout=5.0
        )

        # Verify output
        captured = capsys.readouterr()
        assert "✓ API está healthy" in captured.out

    @patch("stacks_cli.main.httpx.get")
    def test_health_connection_error(self, mock_get, capsys):
        """Test health command when API is unreachable."""
        mock_get.side_effect = httpx.ConnectError("Connection refused")

        # Execute command and expect exit
        with pytest.raises(SystemExit) as exc_info:
            health()

        assert exc_info.value.code == 1

        # Verify error message
        captured = capsys.readouterr()
        assert "✗ API não está acessível" in captured.out

    @patch("stacks_cli.main.httpx.get")
    def test_health_http_error(self, mock_get, capsys):
        """Test health command with HTTP error."""
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Server error", request=Mock(), response=Mock()
        )
        mock_get.return_value = mock_response

        # Execute command and expect exit
        with pytest.raises(SystemExit) as exc_info:
            health()

        assert exc_info.value.code == 1

        # Verify error message
        captured = capsys.readouterr()
        assert "✗ Erro:" in captured.out


class TestCLIIntegration:
    """Integration tests for the CLI app."""

    def test_cli_app_exists(self):
        """Test that CLI app is properly initialized."""
        # cli.name is a tuple in cyclopts
        assert "stacks" in cli.name
        assert "Deploy and manage stacks" in cli.help

    @patch("stacks_cli.main.httpx.get")
    def test_cli_invocation_list(self, mock_get, capsys):
        """Test CLI can be invoked with list command."""
        mock_response = Mock()
        mock_response.json.return_value = {}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        # Invoke CLI with list command
        try:
            cli(["list"])
        except SystemExit:
            pass

        # Verify the command was executed
        mock_get.assert_called_once()

    @patch("stacks_cli.main.httpx.post")
    def test_cli_invocation_deploy(self, mock_post, capsys):
        """Test CLI can be invoked with deploy command."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "status": "success",
            "message": "Deployed",
        }
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response

        # Invoke CLI with deploy command
        try:
            cli(["deploy", "web-app-docker", "test-app"])
        except SystemExit:
            pass

        # Verify the command was executed
        mock_post.assert_called_once()

    @patch("stacks_cli.main.httpx.get")
    def test_cli_invocation_health(self, mock_get, capsys):
        """Test CLI can be invoked with health command."""
        mock_response = Mock()
        mock_response.json.return_value = {"status": "healthy"}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        # Invoke CLI with health command
        try:
            cli(["health"])
        except SystemExit:
            pass

        # Verify the command was executed
        mock_get.assert_called_once()
