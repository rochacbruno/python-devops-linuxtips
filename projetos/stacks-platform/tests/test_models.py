"""Tests for Pydantic models."""

import pytest
from pydantic import ValidationError

from stacks_core.models import (
    DatabaseConfig,
    DeployResult,
    DockerParams,
)


def test_docker_params_minimal():
    """Test minimal DockerParams."""
    params = DockerParams(name="test-app")
    assert params.name == "test-app"
    assert params.base_image == "nginx:latest"
    assert params.ports == [80]
    assert params.with_database is False


def test_docker_params_full():
    """Test full DockerParams."""
    params = DockerParams(
        name="full-app",
        base_image="nginx:alpine",
        ports=[8080, 8081],
        with_database=True,
        database=DatabaseConfig(
            image="postgres:16",
            port=5432,
            password="secret",
        ),
    )

    assert params.name == "full-app"
    assert params.base_image == "nginx:alpine"
    assert params.ports == [8080, 8081]
    assert params.with_database is True
    assert params.database.image == "postgres:16"


def test_docker_params_validation_error():
    """Test validation error when name is missing."""
    with pytest.raises(ValidationError) as exc_info:
        DockerParams()

    errors = exc_info.value.errors()
    assert len(errors) == 1
    assert errors[0]["loc"] == ("name",)
    assert errors[0]["type"] == "missing"


def test_deploy_result():
    """Test DeployResult model."""
    result = DeployResult(
        status="success",
        message="Deploy completed",
        stack_name="web-app-docker",
    )

    assert result.status == "success"
    assert result.message == "Deploy completed"
    assert result.stack_name == "web-app-docker"
    assert result.resources == {}
    assert result.terraform_dir is None
