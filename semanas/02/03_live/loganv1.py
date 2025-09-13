import sys


def analyze_logs(file_handle):
    line_count = 0

    for line in file_handle:
        line_count += 1

    print(f"Total de linhas: {line_count}")


# Simular execução
# from io import StringIO
# fake_log = StringIO("linha1\nlinha2\nlinha3\n")
# analyze_logs(fake_log)

if __name__ == "__main__":
    file = sys.argv[1] if len(sys.argv) > 1 else 0
    with open(file) as f:
        # with open(file, buffering=1) as f:
        analyze_logs(f)

    # Outra forma de evitar buffering é usar stdin diretamente
    # analyze_logs(sys.stdin)
