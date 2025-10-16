from click.testing import CliRunner
from ft.cli import main


def test_convert_command():
    runner = CliRunner()
    result = runner.invoke(main, ["convert", "--from", "file.json", "--to", "file.yaml"])

    assert result.exit_code == 0
    assert "Converting from file.json to file.yaml" in result.output


def test_detect_command():
    runner = CliRunner()
    result = runner.invoke(main, ["detect", "file.json"])

    assert result.exit_code == 0
    assert "Detecting encoding of file.json" in result.output
