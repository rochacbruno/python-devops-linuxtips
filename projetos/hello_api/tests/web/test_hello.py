"""
Browser-based tests for the Hello API web interface using Playwright.
"""

from playwright.sync_api import Page, expect


BASE_URL = "http://localhost:8000"


def test_page_loads(page: Page):
    """Test that the root page loads correctly."""
    page.goto(BASE_URL)

    # Check page title
    expect(page).to_have_title("Hello API")

    # Check main heading
    heading = page.locator("h1")
    expect(heading).to_have_text("Hello API")


def test_input_and_button_exist(page: Page):
    """Test that the input field and button are present."""
    page.goto(BASE_URL)

    # Check input field exists
    input_field = page.locator("#wordInput")
    expect(input_field).to_be_visible()
    expect(input_field).to_have_attribute("placeholder", "Type a word...")

    # Check button exists
    button = page.locator("button")
    expect(button).to_be_visible()
    expect(button).to_have_text("Say Hello")


def test_submit_word_and_get_response(page: Page):
    """Test typing a word and getting a response."""
    page.goto(BASE_URL)

    # Type a word in the input field
    input_field = page.locator("#wordInput")
    input_field.fill("python")

    # Click the button
    button = page.locator("button")
    button.click()

    # Wait for and check the response
    response_div = page.locator("#response")
    expect(response_div).to_be_visible()

    response_text = page.locator("#responseText")
    expect(response_text).to_have_text("Hello Python")


def test_submit_with_enter_key(page: Page):
    """Test submitting by pressing Enter key."""
    page.goto(BASE_URL)

    # Type a word and press Enter
    input_field = page.locator("#wordInput")
    input_field.fill("world")
    input_field.press("Enter")

    # Check the response
    response_text = page.locator("#responseText")
    expect(response_text).to_have_text("Hello World")


def test_empty_input_defaults_to_world(page: Page):
    """Test that empty input defaults to 'world'."""
    page.goto(BASE_URL)

    # Click button without typing anything
    button = page.locator("button")
    button.click()

    # Check the response
    response_text = page.locator("#responseText")
    expect(response_text).to_have_text("Hello World")


def test_camel_case_word(page: Page):
    """Test formatting of CamelCase word."""
    page.goto(BASE_URL)

    # Type a CamelCase word
    input_field = page.locator("#wordInput")
    input_field.fill("MyHolyMother")

    # Click the button
    button = page.locator("button")
    button.click()

    # Check the response
    response_text = page.locator("#responseText")
    expect(response_text).to_have_text("Hello My holy mother")


def test_uppercase_word(page: Page):
    """Test formatting of all-uppercase word."""
    page.goto(BASE_URL)

    # Type an uppercase word
    input_field = page.locator("#wordInput")
    input_field.fill("PYTHON")

    # Click the button
    button = page.locator("button")
    button.click()

    # Check the response
    response_text = page.locator("#responseText")
    expect(response_text).to_have_text("Hello Python")
