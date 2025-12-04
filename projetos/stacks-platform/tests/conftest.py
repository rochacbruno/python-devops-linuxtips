"""Pytest configuration and fixtures."""

import pytest

from stacks_core.models import DockerParams
from stacks_core.registry import registry
from stacks_core.stacks import WebAppDocker


@pytest.fixture(scope="session", autouse=True)
def setup_registry():
    """Register stacks before tests run."""
    registry.register("web-app-docker", WebAppDocker, DockerParams)
    yield
    # Cleanup if needed
