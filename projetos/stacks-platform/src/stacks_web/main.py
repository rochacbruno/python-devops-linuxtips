"""Aplicação Web/Mobile com Flet."""

import flet as ft
import httpx

API_BASE = "http://localhost:8000/api/v1"


def main(page: ft.Page):
    """Aplicação principal."""
    page.title = "Stacks Platform"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 30
    page.window.width = 600
    page.window.height = 800

    # State
    stacks_data = {}

    # Widgets
    title = ft.Text(
        "🚀 Stacks Platform",
        size=36,
        weight=ft.FontWeight.BOLD,
        text_align=ft.TextAlign.CENTER,
    )

    subtitle = ft.Text(
        "Multi-interface Infrastructure as Code",
        size=14,
        color=ft.Colors.GREY_500,
        text_align=ft.TextAlign.CENTER,
    )

    stack_dropdown = ft.Dropdown(
        label="Stack",
        hint_text="Selecione um stack",
        width=500,
        options=[],
    )

    name_input = ft.TextField(
        label="Nome do deployment",
        hint_text="meu-projeto",
        width=500,
        prefix_icon=ft.Icons.LABEL,
    )

    image_input = ft.TextField(
        label="Imagem base",
        value="nginx:latest",
        width=500,
        prefix_icon=ft.Icons.IMAGE,
    )

    ports_input = ft.TextField(
        label="Portas (separadas por vírgula)",
        value="80",
        width=500,
        prefix_icon=ft.Icons.SETTINGS_ETHERNET,
    )

    db_checkbox = ft.Checkbox(
        label="Incluir banco de dados PostgreSQL",
        value=False,
    )

    status_text = ft.Text("", size=14, text_align=ft.TextAlign.CENTER)
    progress_bar = ft.ProgressBar(visible=False, width=500)

    async def load_stacks(e=None):
        """Carrega stacks disponíveis."""
        status_text.value = "⏳ Carregando stacks..."
        status_text.color = ft.Colors.YELLOW
        page.update()

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{API_BASE}/stacks", timeout=10.0)
                response.raise_for_status()
                stacks_data.update(response.json())

                stack_dropdown.options = [ft.dropdown.Option(name) for name in stacks_data.keys()]

                status_text.value = f"✅ {len(stacks_data)} stack(s) disponível(is)"
                status_text.color = ft.Colors.GREEN

        except httpx.ConnectError:
            status_text.value = "❌ Erro: API não está acessível"
            status_text.color = ft.Colors.RED
        except Exception as ex:
            status_text.value = f"❌ Erro: {ex}"
            status_text.color = ft.Colors.RED

        page.update()

    async def deploy_stack(e):
        """Executa deploy."""
        # Validações
        if not stack_dropdown.value:
            status_text.value = "❌ Selecione um stack"
            status_text.color = ft.Colors.RED
            page.update()
            return

        if not name_input.value or not name_input.value.strip():
            status_text.value = "❌ Nome do deployment é obrigatório"
            status_text.color = ft.Colors.RED
            page.update()
            return

        progress_bar.visible = True
        status_text.value = "⏳ Deploying..."
        status_text.color = ft.Colors.YELLOW
        page.update()

        try:
            # Parse portas
            try:
                ports = [int(p.strip()) for p in ports_input.value.split(",") if p.strip()]
            except ValueError:
                status_text.value = "❌ Portas inválidas. Use números separados por vírgula."
                status_text.color = ft.Colors.RED
                progress_bar.visible = False
                page.update()
                return

            # Preparar params
            params = {
                "name": name_input.value.strip(),
                "base_image": image_input.value or "nginx:latest",
                "ports": ports,
                "with_database": db_checkbox.value,
            }

            if db_checkbox.value:
                params["database"] = {
                    "image": "postgres:16-alpine",
                    "port": 5432,
                    "password": "changeme",
                }

            async with httpx.AsyncClient(timeout=300.0) as client:
                response = await client.post(
                    f"{API_BASE}/deploy/{stack_dropdown.value}", json=params
                )
                response.raise_for_status()
                result = response.json()

                if result["status"] == "success":
                    status_text.value = f"✅ {result['message']}"
                    status_text.color = ft.Colors.GREEN

                    # Mostrar dialog de sucesso
                    page.open(
                        ft.AlertDialog(
                            title=ft.Text("Deploy Concluído!"),
                            content=ft.Text(result["message"]),
                            actions=[
                                ft.TextButton("OK", on_click=lambda e: page.close(page.overlay[0]))
                            ],
                        )
                    )
                else:
                    status_text.value = f"❌ {result['message']}"
                    status_text.color = ft.Colors.RED

        except httpx.ConnectError:
            status_text.value = "❌ Erro: API não está acessível"
            status_text.color = ft.Colors.RED
        except httpx.HTTPStatusError as ex:
            status_text.value = f"❌ Erro HTTP {ex.response.status_code}"
            status_text.color = ft.Colors.RED
        except Exception as ex:
            status_text.value = f"❌ Erro: {str(ex)[:100]}"
            status_text.color = ft.Colors.RED

        finally:
            progress_bar.visible = False
            page.update()

    deploy_button = ft.ElevatedButton(
        "🚀 Deploy",
        on_click=deploy_stack,
        width=240,
        height=50,
        style=ft.ButtonStyle(
            color=ft.Colors.WHITE,
            bgcolor=ft.Colors.BLUE,
        ),
    )

    reload_button = ft.OutlinedButton(
        "🔄 Recarregar Stacks",
        on_click=load_stacks,
        width=240,
        height=50,
    )

    # Layout
    page.add(
        ft.Column(
            [
                title,
                subtitle,
                ft.Divider(height=30),
                stack_dropdown,
                name_input,
                image_input,
                ports_input,
                db_checkbox,
                ft.Container(height=10),
                ft.Row(
                    [deploy_button, reload_button],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20,
                ),
                progress_bar,
                ft.Container(height=10),
                status_text,
            ],
            spacing=15,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

    # Carregar stacks ao iniciar
    page.run_task(load_stacks)


def web():
    """Entry point para executar a aplicação."""
    ft.app(target=main, port=8550, view=ft.AppView.WEB_BROWSER)


if __name__ == "__main__":
    ft.app(target=main)
