import subprocess

def scan_image(image: str):
    """Escaneia imagem Docker usando Trivy"""
    try:
        result = subprocess.run(
            ['trivy', 'image', image],
            capture_output=True, text=True, check=True
        )
        print(f"Scan completo para {image}:\n{result.stdout[:500]}...")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao escanear {image}:\n{e.stderr}")

# Exemplo de uso
scan_image('python:3.11-slim')