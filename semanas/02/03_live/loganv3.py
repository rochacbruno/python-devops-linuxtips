#!/usr/bin/env python3
# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "rich",
# ]
# ///
import re
import sys
from collections import Counter, defaultdict

from rich import box, print
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# Pattern para parsing de logs
LOG_PATTERN = re.compile(
    r"^(?P<ip>[\d.]+)\s+"
    r"(?P<identity>\S+)\s+"
    r"(?P<user>\S+)\s+"
    r"\[(?P<timestamp>[^\]]+)\]\s+"
    r'"(?P<method>\S+)\s+'
    r"(?P<path>\S+)\s+"
    r'(?P<protocol>[^"]+)"\s+'
    r"(?P<status>\d{3})\s+"
    r"(?P<size>\S+)"
)


def parse_line(line):
    if match := LOG_PATTERN.match(line):
        return match.groupdict()

    return None


def analyze_logs(file_handle, verbose=False):
    endpoint_counter = Counter()
    status_counter = Counter()
    error_endpoints = defaultdict(int)

    total_lines = 0
    valid_lines = 0

    for line_num, line in enumerate(file_handle, 1):
        total_lines = line_num

        if verbose and line_num % 100000 == 0:
            print(f"[cyan]Processadas {line_num:,} linhas...[/cyan]")

        if parsed := parse_line(line.strip()):
            valid_lines += 1
            endpoint = parsed["path"]
            status = int(parsed["status"])
            endpoint_counter[endpoint] += 1
            status_counter[status] += 1

            if status >= 400:
                error_endpoints[endpoint] += 1

    return {
        "total_lines": total_lines,
        "valid_lines": valid_lines,
        "endpoints": endpoint_counter,
        "status_codes": status_counter,
        "error_endpoints": dict(error_endpoints),
    }


def generate_report(stats):
    console = Console()
    console.print(
        Panel.fit(
            "[bold cyan]RELATÓRIO DE ANÁLISE DE LOGS - LOGAN[/bold cyan]",
            border_style="bright_blue",
        )
    )
    console.print()

    stats_table = Table(title="📊 ESTATÍSTICAS GERAIS", box=box.ROUNDED)
    stats_table.add_column("Métrica", style="cyan", no_wrap=True)
    stats_table.add_column("Valor", justify="right", style="green")
    stats_table.add_row("Total de linhas", f"{stats['total_lines']:,}")
    stats_table.add_row("Linhas válidas", f"{stats['valid_lines']:,}")
    invalid = stats["total_lines"] - stats["valid_lines"]

    if invalid > 0:
        stats_table.add_row("Linhas inválidas", f"[red]{invalid:,}[/red]")
    console.print(stats_table)
    console.print()

    endpoints_table = Table(
        title="🎯 TOP 10 ENDPOINTS MAIS ACESSADOS", box=box.ROUNDED
    )
    endpoints_table.add_column("#", style="dim", width=3)
    endpoints_table.add_column("Requisições", justify="right", style="yellow")
    endpoints_table.add_column("Endpoint", style="cyan")

    for idx, (endpoint, count) in enumerate(
        stats["endpoints"].most_common(10), 1
    ):
        endpoints_table.add_row(str(idx), f"{count:,}", endpoint)
    console.print(endpoints_table)
    console.print()

    if stats["error_endpoints"]:
        error_table = Table(
            title="❌ TOP 5 ENDPOINTS COM MAIS ERROS", box=box.ROUNDED
        )
        error_table.add_column("#", style="dim", width=3)
        error_table.add_column("Erros", justify="right", style="red")
        error_table.add_column("Endpoint", style="cyan")
        error_sorted = sorted(
            stats["error_endpoints"].items(), key=lambda x: x[1], reverse=True
        )[:5]

        for idx, (endpoint, count) in enumerate(error_sorted, 1):
            error_table.add_row(str(idx), f"{count:,}", endpoint)
        console.print(error_table)
        console.print()

    status_table = Table(
        title="📈 DISTRIBUIÇÃO DE STATUS HTTP", box=box.ROUNDED
    )
    status_table.add_column("Status", justify="center", style="cyan", width=8)
    status_table.add_column("Tipo", style="dim")
    status_table.add_column("Requisições", justify="right", style="yellow")
    status_table.add_column("Porcentagem", justify="right", style="green")
    status_table.add_column("Barra", style="blue")
    total_requests = sum(stats["status_codes"].values())
    max_count = (
        max(stats["status_codes"].values()) if stats["status_codes"] else 1
    )

    for status, count in sorted(stats["status_codes"].items()):
        percentage = (count / total_requests) * 100
        bar_length = int((count / max_count) * 20)
        bar = "█" * bar_length + "░" * (20 - bar_length)

        if 200 <= status < 300:
            status_type, status_style = "✅ OK", "[green]"
        elif 300 <= status < 400:
            status_type, status_style = "↪️ Redirect", "[yellow]"
        elif 400 <= status < 500:
            status_type, status_style = "⚠️ Client Error", "[orange1]"
        elif 500 <= status < 600:
            status_type, status_style = "❌ Server Error", "[red]"
        else:
            status_type, status_style = "❓ Unknown", "[dim]"
        status_table.add_row(
            f"{status_style}{status}[/]",
            status_type,
            f"{count:,}",
            f"{percentage:.1f}%",
            bar,
        )
    console.print(status_table)


if __name__ == "__main__":
    file = sys.argv[1] if len(sys.argv) > 1 else 0
    with open(file, buffering=1) as f:
        stats = analyze_logs(f, verbose=True)
        generate_report(stats)
