from ft.cli import main


def test_no_args(capsys):
    main()
    captured = capsys.readouterr()
    assert "Hello from ft" in captured.out
