"""Tests for stack registry."""

import pytest

from stacks_core.models import DockerParams
from stacks_core.registry import StackRegistry
from stacks_core.stacks import WebAppDocker


def test_registry_register_and_get():
    """Test registering and getting a stack."""
    registry = StackRegistry()

    registry.register("test-stack", WebAppDocker, DockerParams)

    assert registry.get_stack("test-stack") == WebAppDocker
    assert registry.get_params_class("test-stack") == DockerParams


def test_registry_get_nonexistent():
    """Test getting a non-existent stack."""
    registry = StackRegistry()

    with pytest.raises(ValueError, match="Stack 'nonexistent' não encontrado"):
        registry.get_stack("nonexistent")


def test_registry_list_stacks():
    """Test listing stacks."""
    registry = StackRegistry()
    registry.register("test-stack", WebAppDocker, DockerParams)

    stacks = registry.list_stacks()

    assert "test-stack" in stacks
    assert "params_schema" in stacks["test-stack"]
    assert "properties" in stacks["test-stack"]["params_schema"]
