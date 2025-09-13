import re
import sys
from collections import Counter, defaultdict

LOG_PATTERN = re.compile(
    r"(?P<ip>\S+) \S+ \S+ \[(?P<datetime>[^\]]+)\] "
    r'"(?P<method>\S+) (?P<path>\S+) (?P<protocol>\S+)" '
    r"(?P<status>\d+) (?P<size>\S+)"
)


def parse_line(line):
    if match := LOG_PATTERN.match(line):
        return match.groupdict()

    return None


def analyze_logs(file_handle, verbose=False):
    # Contadores eficientes
    endpoint_counter = Counter()
    status_counter = Counter()
    error_endpoints = defaultdict(int)
    total_lines = 0
    valid_lines = 0

    for line_num, line in enumerate(file_handle, 1):
        total_lines = line_num
        # Feedback para arquivos grandes

        if verbose and line_num % 1000 == 0:
            print(f"Processadas {line_num:,} linhas...", file=sys.stderr)

        parsed = parse_line(line.strip())

        if parsed:
            valid_lines += 1
            # Coleta estatísticas
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
    """Gera o Relatório Visual"""
    report = []

    report.append("=" * 50)
    report.append("RELATÓRIO DE ANÁLISE DE LOGS - LOGAN")
    report.append("=" * 50)
    report.append("")

    # ESTATÍSTICAS GERAIS
    report.append("📊 ESTATÍSTICAS GERAIS:")
    report.append(f"   Total de linhas: {stats['total_lines']:,}")
    report.append(f"   Linhas válidas: {stats['valid_lines']:,}")
    report.append("")

    # TOP 10 ENDPOINTS MAIS ACESSADOS
    report.append("🎯 TOP 10 ENDPOINTS MAIS ACESSADOS:")

    for endpoint, count in stats["endpoints"].most_common(10):
        report.append(f"   {count:,} - {endpoint}")
    report.append("")

    # TOP 5 ENDPOINTS COM MAIS ERROS

    if stats["error_endpoints"]:
        report.append("❌ TOP 5 ENDPOINTS COM MAIS ERROS:")
        error_sorted = sorted(
            stats["error_endpoints"].items(), key=lambda x: x[1], reverse=True
        )[:5]

        for endpoint, count in error_sorted:
            report.append(f"    {count:,} - {endpoint}")
        report.append("")

    # DISTRIBUIÇÃO DE STATUS HTTP
    report.append("📈 DISTRIBUIÇÃO DE STATUS HTTP:")
    total_requests = sum(stats["status_codes"].values())

    for status, count in sorted(stats["status_codes"].items()):
        percentage = (count / total_requests) * 100
        report.append(f"   {status}: {count:,} ({percentage:.1f}%)")

    return "\n".join(report)


if __name__ == "__main__":
    file = sys.argv[1] if len(sys.argv) > 1 else 0
    with open(file, buffering=1) as f:
        stats = analyze_logs(f, verbose=True)
        print(generate_report(stats))
