"""Unit tests for the format_word function in app.py."""

import pytest

from app import format_word


def test_format_word_simple_lowercase():
    """Test format_word with simple lowercase word."""
    assert format_word("batata") == "Batata"


def test_format_word_simple_lowercase_multiple_chars():
    """Test format_word with longer lowercase word."""
    assert format_word("foobar") == "Foobar"


def test_format_word_camel_case():
    """Test format_word with CamelCase adds spaces before capitals."""
    assert format_word("MyHolyMother") == "My holy mother"


def test_format_word_all_uppercase():
    """Test format_word with all uppercase word converts to title case."""
    assert format_word("PYTHON") == "Python"


def test_format_word_single_uppercase_letter():
    """Test format_word with single uppercase letter."""
    assert format_word("A") == "A"


def test_format_word_single_lowercase_letter():
    """Test format_word with single lowercase letter."""
    assert format_word("a") == "A"


def test_format_word_mixed_case():
    """Test format_word with mixed case pattern."""
    assert format_word("helloWorld") == "Hello world"


def test_format_word_multiple_consecutive_capitals():
    """Test format_word with multiple consecutive capitals."""
    assert format_word("XMLParser") == "X m l parser"


def test_format_word_already_capitalized():
    """Test format_word with word already properly capitalized."""
    assert format_word("World") == "World"


def test_format_word_with_numbers():
    """Test format_word with numbers in the word."""
    assert format_word("test123") == "Test123"


def test_format_word_empty_string():
    """Test format_word with empty string."""
    assert format_word("") == ""


def test_format_word_camel_case_starting_lowercase():
    """Test format_word with camelCase starting with lowercase."""
    assert format_word("myVariableName") == "My variable name"


def test_format_word_pascal_case():
    """Test format_word with PascalCase."""
    assert format_word("MyClassName") == "My class name"


def test_format_word_all_caps_single_char():
    """Test format_word doesn't lowercase single uppercase letter."""
    # According to the code: if word.isupper() and len(word) > 1
    # Single letter won't be lowercased first
    assert format_word("X") == "X"


def test_format_word_consecutive_caps_in_middle():
    """Test format_word with consecutive capitals in the middle."""
    assert format_word("myHTTPServer") == "My h t t p server"


@pytest.mark.parametrize(
    "input_word,expected_output",
    [
        ("world", "World"),
        ("python", "Python"),
        ("linuxtips", "Linuxtips"),
        ("DevOps", "Dev ops"),
        ("API", "Api"),
        ("HTTPSConnection", "H t t p s connection"),
        ("snake_case", "Snake_case"),  # Underscores not handled specially
    ],
)
def test_format_word_parametrized(input_word, expected_output):
    """Test format_word with various inputs using parametrize."""
    assert format_word(input_word) == expected_output
