"""TUI usando Textual."""

import httpx
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Button, Checkbox, Footer, Header, Input, Select, Static

API_BASE = "http://localhost:8000/api/v1"


class StacksApp(App):
    """Aplicação TUI para Stacks Platform."""

    CSS = """
    Screen {
        background: $surface;
    }

    #main-container {
        width: 100%;
        height: 100%;
        padding: 1;
        align: center middle;
    }

    #form-container {
        width: 80;
        height: auto;
        border: solid $primary;
        padding: 2;
        background: $panel;
    }

    #title {
        text-align: center;
        text-style: bold;
        color: $accent;
        margin-bottom: 1;
    }

    Input {
        margin: 1 0;
    }

    Select {
        margin: 1 0;
    }

    Checkbox {
        margin: 1 0;
    }

    #button-container {
        height: auto;
        align: center middle;
        margin-top: 1;
    }

    Button {
        margin: 0 1;
    }

    #status {
        margin-top: 1;
        padding: 1;
        text-align: center;
        height: auto;
        border: solid $secondary;
    }
    """

    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("ctrl+r", "reload", "Reload Stacks"),
        Binding("ctrl+d", "deploy", "Deploy"),
    ]

    def compose(self) -> ComposeResult:
        """Composição da interface."""
        yield Header()

        with Container(id="main-container"):
            with Vertical(id="form-container"):
                yield Static("🚀 Stacks Platform", id="title")

                yield Select(
                    options=[("Carregando...", "loading")],
                    prompt="Selecione um stack",
                    id="stack_select",
                )

                yield Input(placeholder="Nome do deployment *", id="name_input")

                yield Input(
                    placeholder="Imagem base (padrão: nginx:latest)",
                    id="image_input",
                )

                yield Input(
                    placeholder="Portas (separadas por vírgula, padrão: 80)",
                    id="ports_input",
                )

                yield Checkbox("Incluir banco de dados PostgreSQL", id="db_checkbox")

                with Horizontal(id="button-container"):
                    yield Button("Deploy", id="deploy_btn", variant="primary")
                    yield Button("Recarregar Stacks", id="reload_btn", variant="default")

                yield Static("Pronto para deploy", id="status")

        yield Footer()

    async def on_mount(self) -> None:
        """Ao montar, carregar stacks."""
        await self.load_stacks()

    async def load_stacks(self) -> None:
        """Lista stacks disponíveis."""
        status = self.query_one("#status", Static)
        status.update("⏳ Carregando stacks...")

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{API_BASE}/stacks", timeout=10.0)
                response.raise_for_status()
                stacks = response.json()

                select = self.query_one("#stack_select", Select)
                select.set_options([(name, name) for name in stacks.keys()])

                status.update(f"✅ {len(stacks)} stack(s) disponível(is)")

        except httpx.ConnectError:
            status.update("❌ Erro: API não está acessível")
        except Exception as e:
            status.update(f"❌ Erro: {e}")

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handler para botões."""
        if event.button.id == "deploy_btn":
            await self.do_deploy()
        elif event.button.id == "reload_btn":
            await self.load_stacks()

    async def action_reload(self) -> None:
        """Action para recarregar stacks."""
        await self.load_stacks()

    async def action_deploy(self) -> None:
        """Action para deploy."""
        await self.do_deploy()

    async def do_deploy(self) -> None:
        """Executa deploy."""
        status = self.query_one("#status", Static)

        try:
            # Coletar inputs
            stack_name = self.query_one("#stack_select", Select).value
            name = self.query_one("#name_input", Input).value.strip()
            image = self.query_one("#image_input", Input).value.strip() or "nginx:latest"
            ports_str = self.query_one("#ports_input", Input).value.strip() or "80"
            with_db = self.query_one("#db_checkbox", Checkbox).value

            # Validações
            if not stack_name or stack_name == "loading":
                status.update("❌ Selecione um stack válido")
                return

            if not name:
                status.update("❌ Nome do deployment é obrigatório")
                return

            # Parse portas
            try:
                ports = [int(p.strip()) for p in ports_str.split(",") if p.strip()]
            except ValueError:
                status.update("❌ Portas inválidas. Use números separados por vírgula.")
                return

            # Preparar params
            params = {
                "name": name,
                "base_image": image,
                "ports": ports,
                "with_database": with_db,
            }

            if with_db:
                params["database"] = {
                    "image": "postgres:16-alpine",
                    "port": 5432,
                    "password": "changeme",
                }

            status.update(f"⏳ Deploying {stack_name}...")

            async with httpx.AsyncClient(timeout=300.0) as client:
                response = await client.post(f"{API_BASE}/deploy/{stack_name}", json=params)
                response.raise_for_status()
                result = response.json()

                if result["status"] == "success":
                    status.update(f"✅ {result['message']}")
                else:
                    status.update(f"❌ {result['message']}")

        except httpx.ConnectError:
            status.update("❌ Erro: API não está acessível")
        except httpx.HTTPStatusError as e:
            error_detail = e.response.text
            status.update(f"❌ Erro HTTP {e.response.status_code} {error_detail}")
        except Exception as e:
            status.update(f"❌ Erro: {str(e)[:100]}")


def run():
    """Executa a TUI."""
    app = StacksApp()
    app.run()


if __name__ == "__main__":
    run()
