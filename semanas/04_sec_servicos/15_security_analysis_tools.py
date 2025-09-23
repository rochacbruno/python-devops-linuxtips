# Comandos úteis para segurança
commands = [
    "pip-audit",          # Verifica CVEs em dependências Python
    "safety check",       # Análise de vulnerabilidades
    "bandit -r .",        # Análise de código Python
    "trivy image app:latest",  # Scan de container
    "grype .",            # Vulnerabilidades em dependências
]

print("Ferramentas de análise de segurança:")
for cmd in commands:
    tool = cmd.split()[0]
    print(f"  - {tool}: {cmd}")

# Verificar se ferramentas estão instaladas
import shutil
for tool in ['pip-audit', 'safety', 'bandit']:
    installed = shutil.which(tool) is not None
    status = "✓" if installed else "✗"
    print(f"  {status} {tool}")