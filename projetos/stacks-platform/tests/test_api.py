"""Tests for the API."""

from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from stacks_api.main import app
from stacks_core.models import DeployResult

client = TestClient(app)


def test_health():
    """Test health endpoint."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_list_stacks():
    """Test list stacks endpoint."""
    response = client.get("/api/v1/stacks")
    assert response.status_code == 200
    data = response.json()
    assert "web-app-docker" in data
    assert "params_schema" in data["web-app-docker"]


def test_deploy_invalid_stack():
    """Test deploy with invalid stack name."""
    response = client.post("/api/v1/deploy/invalid-stack", json={"name": "test"})
    assert response.status_code == 404


def test_deploy_invalid_params():
    """Test deploy with invalid parameters."""
    response = client.post(
        "/api/v1/deploy/web-app-docker",
        json={},  # Missing required 'name' field
    )
    assert response.status_code == 422


@patch("stacks_api.routes.deploy_manager.deploy")
def test_deploy_valid_params(mock_deploy):
    """Test deploy with valid parameters (mocked, no real deployment)."""
    # Mock the deploy method to prevent real Docker deployment
    mock_deploy.return_value = DeployResult(
        status="success",
        message="Deploy de web-app-docker realizado com sucesso",
        stack_name="web-app-docker",
        resources={
            "app_container_id": "mock-container-id-123",
            "app_container_name": "test-webapp-app",
            "app_ports": [8080],
        },
    )

    params = {
        "name": "test-webapp",
        "base_image": "nginx:alpine",
        "ports": [8080],
    }

    response = client.post("/api/v1/deploy/web-app-docker", json=params)

    assert response.status_code == 200
    result = response.json()
    assert result["stack_name"] == "web-app-docker"
    assert result["status"] == "success"
    assert result["message"] == "Deploy de web-app-docker realizado com sucesso"
    assert "resources" in result
    assert result["resources"]["app_container_name"] == "test-webapp-app"

    # Verify deploy was called with correct parameters
    mock_deploy.assert_called_once()
    call_args = mock_deploy.call_args
    assert call_args.kwargs["stack_name"] == "web-app-docker"
    assert call_args.kwargs["params"].name == "test-webapp"
    assert call_args.kwargs["params"].base_image == "nginx:alpine"
    assert call_args.kwargs["params"].ports == [8080]
