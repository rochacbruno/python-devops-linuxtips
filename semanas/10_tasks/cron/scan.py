#!/usr/bin/env python3
"""
Script de monitoramento de espaço em disco.
Verifica se o sistema tem pelo menos 30% de espaço livre.
Caso contrário, envia um alerta.
"""

import time
import shutil
from datetime import datetime


def envia_alerta(mensagem):
    """Envia alerta escrevendo em arquivo."""
    with open("/tmp/alertas.log", "a") as alertas:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        alertas.write(f"[{timestamp}] {mensagem}\n")


def scan():
    """Verifica o espaço em disco e envia alerta se necessário."""
    print("Scanning disk space...")

    # Obtém informações de espaço em disco do diretório raiz
    disk_usage = shutil.disk_usage("/")

    # Calcula a porcentagem de espaço livre
    total = disk_usage.total
    used = disk_usage.used
    free = disk_usage.free
    percent_free = (free / total) * 100

    print(f"Total: {total / (1024**3):.2f} GB")
    print(f"Usado: {used / (1024**3):.2f} GB")
    print(f"Livre: {free / (1024**3):.2f} GB")
    print(f"Porcentagem livre: {percent_free:.2f}%")

    # Verifica se há menos de 30% de espaço livre
    if percent_free < 70:
        mensagem = (
            f"ALERTA: Espaço em disco baixo! "
            f"Apenas {percent_free:.2f}% de espaço livre. "
            f"({free / (1024**3):.2f} GB disponíveis)"
        )
        envia_alerta(mensagem)
        print(f"⚠️  {mensagem}")
    else:
        print(f"✓ Espaço em disco OK ({percent_free:.2f}% livre)")


if __name__ == "__main__":
    scan()

