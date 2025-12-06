import flet as ft


def main(page: ft.Page):
    page.title = "Stacks Web"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    page.window.width = 800
    page.window.height = 600

    title = ft.Text("🚀 Stacks Web", size=36, weight=ft.FontWeight.BOLD)
    name_input = ft.TextField(label="name", hint_text="Enter your name")

    async def set_name(e):
        hello_message.value = f"Hello, {name_input.value}"
        page.update()

    submit_button = ft.ElevatedButton("Submit", on_click=set_name)
    hello_message = ft.Text("Hello, World")

    page.add(title, name_input, submit_button, hello_message)


def web():
    ft.app(target=main, port=8550, view=ft.AppView.WEB_BROWSER)


if __name__ == "__main__":
    ft.app(target=main)
