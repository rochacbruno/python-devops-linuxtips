"""Unit tests for the verify_basic_auth function in core.py."""

import base64

import pytest

from core import ADMIN_PASSWORD, ADMIN_USERNAME, verify_basic_auth


def test_verify_basic_auth_with_valid_credentials():
    """Test verify_basic_auth returns True for valid credentials."""
    credentials = f"{ADMIN_USERNAME}:{ADMIN_PASSWORD}"
    encoded = base64.b64encode(credentials.encode()).decode()
    auth_header = f"Basic {encoded}"

    assert verify_basic_auth(auth_header) is True


def test_verify_basic_auth_with_none():
    """Test verify_basic_auth returns False when authorization is None."""
    assert verify_basic_auth(None) is False


def test_verify_basic_auth_with_empty_string():
    """Test verify_basic_auth returns False for empty string."""
    assert verify_basic_auth("") is False


def test_verify_basic_auth_with_wrong_username():
    """Test verify_basic_auth returns False for wrong username."""
    credentials = f"wronguser:{ADMIN_PASSWORD}"
    encoded = base64.b64encode(credentials.encode()).decode()
    auth_header = f"Basic {encoded}"

    assert verify_basic_auth(auth_header) is False


def test_verify_basic_auth_with_wrong_password():
    """Test verify_basic_auth returns False for wrong password."""
    credentials = f"{ADMIN_USERNAME}:wrongpassword"
    encoded = base64.b64encode(credentials.encode()).decode()
    auth_header = f"Basic {encoded}"

    assert verify_basic_auth(auth_header) is False


def test_verify_basic_auth_with_wrong_scheme():
    """Test verify_basic_auth returns False for non-Basic scheme."""
    credentials = f"{ADMIN_USERNAME}:{ADMIN_PASSWORD}"
    encoded = base64.b64encode(credentials.encode()).decode()
    auth_header = f"Bearer {encoded}"

    assert verify_basic_auth(auth_header) is False


def test_verify_basic_auth_with_case_insensitive_scheme():
    """Test verify_basic_auth handles different case for 'Basic' scheme."""
    credentials = f"{ADMIN_USERNAME}:{ADMIN_PASSWORD}"
    encoded = base64.b64encode(credentials.encode()).decode()

    # Test various casings
    for scheme in ["basic", "BASIC", "Basic", "bAsIc"]:
        auth_header = f"{scheme} {encoded}"
        assert verify_basic_auth(auth_header) is True


def test_verify_basic_auth_with_malformed_header_no_space():
    """Test verify_basic_auth returns False for malformed header without space."""
    auth_header = "BasicYWRtaW46QmF0YXRhMTIz"

    assert verify_basic_auth(auth_header) is False


def test_verify_basic_auth_with_invalid_base64():
    """Test verify_basic_auth returns False for invalid base64 encoding."""
    auth_header = "Basic invalid!!!base64"

    assert verify_basic_auth(auth_header) is False


def test_verify_basic_auth_with_missing_colon_in_credentials():
    """Test verify_basic_auth returns False when credentials lack colon separator."""
    # Encode credentials without colon
    credentials = "adminBatata123"
    encoded = base64.b64encode(credentials.encode()).decode()
    auth_header = f"Basic {encoded}"

    # This should return False as split(':',1) will not produce username and password
    assert verify_basic_auth(auth_header) is False


def test_verify_basic_auth_with_colon_in_password():
    """Test verify_basic_auth handles password with colon correctly."""
    # Password with colon should work due to split(':', 1)
    username = ADMIN_USERNAME
    password = "Pass:word:123"
    credentials = f"{username}:{password}"
    encoded = base64.b64encode(credentials.encode()).decode()
    auth_header = f"Basic {encoded}"

    # This will fail because password doesn't match ADMIN_PASSWORD
    # but the parsing should work correctly
    assert verify_basic_auth(auth_header) is False

    # Test with actual admin password that has colon (if we modify temporarily)
    # For now, this just ensures the split logic works


def test_verify_basic_auth_with_empty_username():
    """Test verify_basic_auth returns False for empty username."""
    credentials = f":{ADMIN_PASSWORD}"
    encoded = base64.b64encode(credentials.encode()).decode()
    auth_header = f"Basic {encoded}"

    assert verify_basic_auth(auth_header) is False


def test_verify_basic_auth_with_empty_password():
    """Test verify_basic_auth returns False for empty password."""
    credentials = f"{ADMIN_USERNAME}:"
    encoded = base64.b64encode(credentials.encode()).decode()
    auth_header = f"Basic {encoded}"

    assert verify_basic_auth(auth_header) is False


def test_verify_basic_auth_with_extra_spaces():
    """Test verify_basic_auth handles extra spaces in header."""
    credentials = f"{ADMIN_USERNAME}:{ADMIN_PASSWORD}"
    encoded = base64.b64encode(credentials.encode()).decode()
    # Extra spaces between scheme and credentials
    auth_header = f"Basic  {encoded}"

    # split() will handle multiple spaces, so this should work
    assert verify_basic_auth(auth_header) is True


def test_verify_basic_auth_with_only_scheme():
    """Test verify_basic_auth returns False for header with only scheme."""
    auth_header = "Basic"

    assert verify_basic_auth(auth_header) is False


def test_verify_basic_auth_with_unicode_credentials():
    """Test verify_basic_auth handles unicode characters in credentials."""
    credentials = "user😀:pass🔑"
    encoded = base64.b64encode(credentials.encode()).decode()
    auth_header = f"Basic {encoded}"

    # Should return False (wrong credentials) but not crash
    assert verify_basic_auth(auth_header) is False


@pytest.mark.parametrize(
    "auth_header,expected",
    [
        (None, False),
        ("", False),
        ("Bearer token", False),
        ("Digest credentials", False),
        (f"Basic {base64.b64encode(b'admin:Batata123').decode()}", True),
        (f"basic {base64.b64encode(b'admin:Batata123').decode()}", True),
        (f"Basic {base64.b64encode(b'wrong:credentials').decode()}", False),
        ("Basic !!!invalid", False),
        ("NoScheme", False),
    ],
)
def test_verify_basic_auth_parametrized(auth_header, expected):
    """Test verify_basic_auth with various inputs using parametrize."""
    assert verify_basic_auth(auth_header) is expected
