from textual.app import App, ComposeResult
from textual.widgets import Button, Header, Input, Static


class StacksAPP(App):
    """Stacks TUI APP"""

    CSS = """
    #hello_message {
        color: green;
        border: solid yellow;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header()
        yield Input(placeholder="Enter your name", id="name_input")
        yield Button("Submit", id="submit_button")
        yield Static("Hello, World!", id="hello_message")

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == "submit_button":
            name = self.query_one("#name_input").value
            self.query_one("#hello_message").update(f"Hello {name}")

    def on_mount(self):
        self.title = "Stacks TUI"


def run():
    app = StacksAPP()
    app.run()


if __name__ == "__main__":
    run()
