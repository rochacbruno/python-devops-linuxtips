#!/usr/bin/env python3
"""
Script de monitoramento de containers Docker.
Verifica se o container 'my_api' está rodando e saudável.
Usa a biblioteca sched para agendamento de tarefas.
"""

import os
import sched
import time
import subprocess
from datetime import datetime
from typing import Optional
import urllib.request
import urllib.error
import json


def envia_alerta(mensagem: str) -> None:
    """Envia alerta escrevendo em arquivo."""
    with open("/tmp/alertas", "a") as alertas:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        alertas.write(f"[{timestamp}] {mensagem}\n")
    print(f"🚨 ALERTA: {mensagem}")


def container_esta_rodando(container_name: str) -> bool:
    """Verifica se um container está rodando."""
    try:
        result = subprocess.run(
            ["docker", "ps", "--filter", f"name={container_name}", "--format", "{{.Names}}"],
            capture_output=True,
            text=True,
            check=True
        )
        containers = result.stdout.strip().split('\n')
        return container_name in containers
    except subprocess.CalledProcessError as e:
        print(f"Erro ao verificar container: {e}")
        return False


def verificar_health_endpoint(url: str = "http://localhost:8000/health", timeout: int = 5) -> Optional[dict]:
    """Faz requisição HTTP para o endpoint de health check."""
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=timeout) as response:
            data = json.loads(response.read().decode())
            return {"status_code": response.status, "data": data}
    except urllib.error.HTTPError as e:
        # Captura erros HTTP (como 503)
        try:
            data = json.loads(e.read().decode())
            return {"status_code": e.code, "data": data}
        except:
            return {"status_code": e.code, "data": None}
    except Exception as e:
        print(f"Erro ao fazer requisição: {e}")
        return None


def parar_container(container_name: str) -> bool:
    """Para um container."""
    try:
        subprocess.run(["docker", "stop", container_name], check=True, capture_output=True)
        print(f"Container {container_name} parado com sucesso")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Erro ao parar container: {e}")
        return False


def iniciar_container(container_name: str, image: str = "my_api", port: str = "8000:8000") -> bool:
    """Inicia um container."""
    try:
        # Remove container antigo se existir
        subprocess.run(
            ["docker", "rm", "-f", container_name],
            capture_output=True,
        )

        # Inicia novo container
        subprocess.run(
            ["docker", "run", "-d", "--name", container_name, "-p", port, image],
            check=True,
            capture_output=True
        )
        print(f"Container {container_name} iniciado com sucesso")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Erro ao iniciar container: {e}")
        return False


def resetar_container(container_name: str) -> None:
    """Para e reinicia o container."""
    print(f"Resetando container {container_name}...")
    parar_container(container_name)
    time.sleep(2)  # Aguarda um pouco antes de reiniciar
    iniciar_container(container_name)
    time.sleep(3)  # Aguarda o container inicializar


def scan() -> None:
    """Verifica se o container está rodando e saudável."""
    container_name = "my_api"
    print(f"\n{'='*60}")
    print(f"Scanning container: {container_name}")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}")

    # Verifica se o container está rodando
    if not container_esta_rodando(container_name):
        mensagem = f"Container {container_name} não está rodando!"
        envia_alerta(mensagem)
        print(f"⚠️  {mensagem}")
        print("Tentando iniciar o container...")
        iniciar_container(container_name)
        return

    print(f"✓ Container {container_name} está rodando")

    # Verifica o health check
    print("Verificando endpoint /health...")
    health_response = verificar_health_endpoint()

    if health_response is None:
        mensagem = f"Não foi possível conectar ao endpoint /health do container {container_name}"
        envia_alerta(mensagem)
        print(f"⚠️  {mensagem}")
        print("Container pode estar iniciando ou com problemas. Resetando...")
        resetar_container(container_name)
        envia_alerta(f"Container {container_name} foi resetado devido a falha de conexão")
        return

    status_code = health_response["status_code"]
    data = health_response["data"]

    if status_code == 200:
        print(f"✓ Container está saudável!")
        if data:
            print(f"  Status: {data.get('status', 'N/A')}")
            print(f"  Mensagem: {data.get('message', 'N/A')}")
            print(f"  Request count: {data.get('request_count', 'N/A')}")
    else:
        mensagem = f"Container {container_name} não está saudável! Status code: {status_code}"
        if data:
            mensagem += f" - {data.get('message', '')}"
        envia_alerta(mensagem)
        print(f"⚠️  {mensagem}")
        print("Resetando container...")
        resetar_container(container_name)
        envia_alerta(f"Container {container_name} foi resetado devido a status não saudável")


def agendar_scan(scheduler: sched.scheduler, interval: int) -> None:
    """Agenda a próxima execução do scan."""
    scan()
    # Agenda a próxima execução
    scheduler.enter(interval, 1, agendar_scan, (scheduler, interval))


def main() -> None:
    """Função principal que configura e executa o agendamento."""
    # Lê configurações de variáveis de ambiente
    interval = int(os.getenv("SCAN_INTERVAL", "30"))  # Padrão: 30 segundos

    print(f"Iniciando daemon de monitoramento de containers")
    print(f"Intervalo de verificação: {interval} segundos")
    print(f"Pressione CTRL+C para parar\n")

    # Cria o scheduler
    scheduler = sched.scheduler(time.time, time.sleep)

    # Agenda a primeira execução
    scheduler.enter(0, 1, agendar_scan, (scheduler, interval))

    try:
        # Executa o scheduler (loop infinito)
        scheduler.run()
    except KeyboardInterrupt:
        print("\n\nDaemon interrompido pelo usuário")
        print("Encerrando...")


if __name__ == "__main__":
    main()
