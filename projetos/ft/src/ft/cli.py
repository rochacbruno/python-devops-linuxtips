"""This is CLI module for ft."""

import argparse


def main() -> None:
    """Main entry point for ft CLI

    Args:
      file: str

    Returns:
      None

    Raises:
      FileNotFoundError Raised when file is not readable
    """
    parser = argparse.ArgumentParser(
        description="File Tool: Canivete suiço para tratar arquivos.",
        epilog="""
Exemplos de uso:
  %(prog)s convert --from file.json --to file.yaml
  %(prog)s convert --from https://remote/file.json --to file.yaml
  %(prog)s convert --from file.yaml --to https://remote/post
  %(prog)s convert --from file.yaml --to json (sdout)
  echo STDIN | %(prog)s convert --from yaml --to json file.json
  %(prog)s detect mysterious_file.txt
        """.strip(),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--version", action="version", version="ft 0.1.0")

    subparsers = parser.add_subparsers(
        dest="command", help="Comandos disponíveis", metavar="COMMAND"
    )

    # convert command
    convert_parser = subparsers.add_parser(
        "convert",
        help=("Convert file formats \nsupport JSON YAML ..."),
        description="Convert file to target format",
    )
    convert_parser.add_argument(
        "--from", required=True, help="Source file or format", dest="from_"
    )
    convert_parser.add_argument("--to", required=True, help="Target file or format")

    # detect command
    detect_parser = subparsers.add_parser("detect", help="Detect file encoding")
    detect_parser.add_argument("file", help="File to detect encoding")

    args = parser.parse_args()
    match args.command:
        case "convert":
            print(f"Converting from {args.from_} to {args.to}")
            # TODO: Implement convert
        case "detect":
            print(f"Detecting encoding of {args.file}")
            # TODO: Implement detect
        case _:
            parser.print_help()
