"""CLI usando Cyclopts."""

import json
import sys

import httpx
from cyclopts import App
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax
from rich.table import Table

console = Console()


cli = App(
    name="stacks",
    help="Deploy and manage stacks on the **Stacks Platform**.",
    help_format="markdown",
)

API_BASE = "http://localhost:8000/api/v1"


@cli.command()
def list():
    """Lista stacks disponíveis."""
    try:
        response = httpx.get(f"{API_BASE}/stacks", timeout=10.0)
        response.raise_for_status()

        stacks = response.json()

        table = Table(title="Stacks Disponíveis", show_header=True, header_style="bold magenta")
        table.add_column("Nome", style="cyan", width=20)
        table.add_column("Parâmetros Requeridos", style="green")

        for name, info in stacks.items():
            props = info["params_schema"]["properties"]
            required = info["params_schema"].get("required", [])
            params_list = [
                f"{k} ({v.get('type', 'any')})" for k, v in props.items() if k in required
            ]
            table.add_row(name, "\n".join(params_list))

        console.print(table)

    except httpx.ConnectError:
        console.print("[red]✗ Erro: Não foi possível conectar à API.[/red]")
        console.print("[yellow]Certifique-se de que a API está rodando: uv run stacks-api[/yellow]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]✗ Erro: {e}[/red]")
        sys.exit(1)


@cli.command()
def deploy(
    stack: str,
    name: str,
    base_image: str = "nginx:latest",
    ports: str = "80",
    with_database: bool = False,
):
    """Faz deploy de um stack.

    Args:
        stack: Nome do stack (ex: web-app-docker)
        name: Nome único para este deployment
        base_image: Imagem Docker base (padrão: nginx:latest)
        ports: Portas a expor, separadas por vírgula (padrão: 80)
        with_database: Incluir container de banco de dados
    """
    try:
        ports_list = [int(p.strip()) for p in ports.split(",")]

        params = {
            "name": name,
            "base_image": base_image,
            "ports": ports_list,
            "with_database": with_database,
        }

        if with_database:
            params["database"] = {
                "image": "postgres:16-alpine",
                "port": 5432,
                "password": "changeme",
            }

        console.print(
            Panel(
                f"[yellow]Stack:[/yellow] {stack}\n"
                f"[yellow]Nome:[/yellow] {name}\n"
                f"[yellow]Imagem:[/yellow] {base_image}\n"
                f"[yellow]Portas:[/yellow] {ports_list}\n"
                f"[yellow]Com DB:[/yellow] {with_database}",
                title="Iniciando Deploy",
                border_style="blue",
            )
        )

        response = httpx.post(f"{API_BASE}/deploy/{stack}", json=params, timeout=300.0)
        response.raise_for_status()

        result = response.json()

        if result["status"] == "success":
            console.print(
                Panel(
                    f"[green]✓ {result['message']}[/green]",
                    title="Deploy Concluído",
                    border_style="green",
                )
            )

            if result.get("resources"):
                console.print("\n[cyan]Recursos criados:[/cyan]")
                syntax = Syntax(json.dumps(result["resources"], indent=2), "json", theme="monokai")
                console.print(syntax)

        else:
            console.print(f"[red]✗ {result['message']}[/red]")
            sys.exit(1)

    except httpx.ConnectError:
        console.print("[red]✗ Erro: Não foi possível conectar à API.[/red]")
        sys.exit(1)
    except httpx.HTTPStatusError as e:
        console.print(f"[red]✗ Erro HTTP {e.response.status_code}: {e.response.text}[/red]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]✗ Erro: {e}[/red]")
        sys.exit(1)


@cli.command()
def health():
    """Verifica saúde da API."""
    try:
        response = httpx.get(f"{API_BASE}/health", timeout=5.0)
        response.raise_for_status()

        data = response.json()
        console.print(f"[green]✓ API está {data['status']}[/green]")

    except httpx.ConnectError:
        console.print("[red]✗ API não está acessível[/red]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]✗ Erro: {e}[/red]")
        sys.exit(1)


def main():
    """Entry point do CLI."""
    cli()


if __name__ == "__main__":
    main()
