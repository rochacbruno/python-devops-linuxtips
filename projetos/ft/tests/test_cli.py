from unittest.mock import patch
from ft.cli import main


def test_convert_command(capsys):
    test_args = ["ft", "convert", "--from", "file.json", "--to", "file.yaml"]

    with patch("sys.argv", test_args):
        main()
        captured = capsys.readouterr()

    assert "Converting from file.json to file.yaml" in captured.out


def test_detect_command(capsys):
    test_args = ["ft", "detect", "file.json"]

    with patch("sys.argv", test_args):
        main()
        captured = capsys.readouterr()

    assert "Detecting encoding of file.json" in captured.out
