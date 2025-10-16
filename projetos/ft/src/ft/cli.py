"""This is CLI module for ft."""

import click


@click.group(
    help="File Tool: Canivete suiço para tratar arquivos.",
    epilog="""
Exemplos de uso:\n
  ft convert --from file.json --to file.yaml\n
  ft convert --from https://remote/file.json --to file.yaml\n
  ft convert --from file.yaml --to https://remote/post\n
  ft convert --from file.yaml --to json (sdout)\n
  echo STDIN | ft convert --from yaml --to json file.json\n
  ft detect mysterious_file.txt
    """,
)
@click.version_option(version="0.1.0", prog_name="ft")
def main() -> None:
    """Main entry point for ft CLI

    Raises:
      FileNotFoundError: Raised when file is not readable
    """
    pass


@main.command(help="Convert file formats\nsupport JSON YAML ...")
@click.option(
    "--from",
    "from_",
    required=True,
    help="Source file or format",
)
@click.option(
    "--to",
    required=True,
    help="Target file or format",
)
def convert(from_: str, to: str) -> None:
    """Convert file to target format

    Args:
        from_: Source file or format
        to: Target file or format
    """
    click.echo(f"Converting from {from_} to {to}")
    # TODO: Implement convert


@main.command(help="Detect file encoding")
@click.argument("file")
def detect(file: str) -> None:
    """Detect file encoding

    Args:
        file: File to detect encoding
    """
    click.echo(f"Detecting encoding of {file}")
    # TODO: Implement detect
