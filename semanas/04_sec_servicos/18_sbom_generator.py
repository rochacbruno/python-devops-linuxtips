import subprocess
import json
from pathlib import Path

def generate_sbom():
    """Gera SBOM básico do projeto"""
    sbom = {
        "bomFormat": "CycloneDX",
        "specVersion": "1.4",
        "components": []
    }

    # Coletar dependências
    if Path('requirements.txt').exists():
        with open('requirements.txt') as f:
            for line in f:
                if line.strip() and not line.strip().startswith('#') and '--hash=' not in line:
                    parts = line.replace("\\","").strip().split('==')
                    component = {
                        "type": "library",
                        "name": parts[0],
                        "version": parts[1] if len(parts) > 1 else "latest"
                    }
                    sbom["components"].append(component)

    return sbom

# Exemplo de SBOM
sbom_example = generate_sbom()
print(f"SBOM gerado com {len(sbom_example['components'])} componentes")
print(json.dumps(sbom_example, indent=2) + "...")