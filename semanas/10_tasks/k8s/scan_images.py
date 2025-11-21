# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "kubernetes",
# ]
# ///

#!/usr/bin/env python3
"""
Script de monitoramento de imagens Docker no Kubernetes.
Verifica se há pods usando imagens com tag 'latest'.
Envia alerta caso encontre.
"""

import smtplib
from email.mime.text import MIMEText
import json
import urllib.request
import os
import sys
from datetime import datetime
from typing import List

try:
    from kubernetes import client, config
    from kubernetes.client.rest import ApiException
except ImportError:
    print("Erro: Biblioteca 'kubernetes' não instalada")
    print("Instale com: pip install kubernetes")
    sys.exit(1)

SMTP_SERVER = "mailhog.default.svc.cluster.local"
SMTP_PORT = 1025


def enviar_email(mensagem):
    msg = MIMEText(mensagem)
    msg["Subject"] = "Alerta: Imagens com tag latest"
    msg["From"] = "admin@system.com"
    msg["To"] = "support@system.com"

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
        # smtp.starttls()
        # smtp.login(SMTP_USER, SMTP_PASS)
        smtp.send_message(msg)


def enviar_slack(mensagem, webhook_url):
    payload = {"text": mensagem}
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        webhook_url, data=data, headers={"Content-Type": "application/json"}
    )
    urllib.request.urlopen(req)


def envia_alerta(mensagem: str, arquivo: str = "/tmp/alertas") -> None:
    """Envia alerta escrevendo em arquivo."""
    try:
        # with open(arquivo, "a") as alertas:
        #     timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        #     alertas.write(f"[{timestamp}] {mensagem}\n")
        # print(f"🚨 ALERTA gravado: {mensagem}")
        # enviar_slack(mensagem=mensagem, webhook_url=os.getenv("SLACK_WEBHOOK_URL"))
        enviar_email(mensagem=mensagem)
    except Exception as e:
        print(f"Erro ao gravar alerta: {e}")


def inicializar_kubernetes() -> client.CoreV1Api:
    """
    Inicializa o cliente do Kubernetes.
    Tenta carregar config do cluster primeiro (quando rodando em pod),
    senão carrega do kubeconfig local.
    """
    try:
        # Tenta carregar configuração in-cluster (quando rodando em pod)
        config.load_incluster_config()
        print("✓ Configuração in-cluster carregada")
    except config.ConfigException:
        try:
            # Se falhar, tenta carregar do kubeconfig local
            config.load_kube_config()
            print("✓ Configuração local (kubeconfig) carregada")
        except Exception as e:
            print(f"Erro ao carregar configuração do Kubernetes: {e}")
            sys.exit(1)

    return client.CoreV1Api()


def obter_pods(v1: client.CoreV1Api, namespace: str = "default") -> List[client.V1Pod]:
    """
    Obtém lista de pods em um namespace.

    Args:
        v1: Cliente da API Core V1
        namespace: Namespace a ser consultado

    Returns:
        Lista de pods
    """
    try:
        pods = v1.list_namespaced_pod(namespace=namespace)
        return pods.items
    except ApiException as e:
        print(f"Erro ao listar pods: {e}")
        return []


def verificar_imagem_latest(imagem: str) -> bool:
    """
    Verifica se uma imagem usa tag 'latest' ou não especifica tag.

    Args:
        imagem: Nome da imagem (ex: 'nginx:latest' ou 'nginx')

    Returns:
        True se usa 'latest' ou não tem tag
    """
    # Imagens sem tag explícita usam 'latest' por padrão
    if ":" not in imagem:
        return True

    # Verifica se tag é 'latest'
    _, tag = imagem.rsplit(":", 1)
    return tag.lower() == "latest"


def scan(namespace: str = "default") -> None:
    """
    Executa o scan de imagens nos pods do cluster.

    Args:
        namespace: Namespace a ser escaneado
    """
    print(f"\n{'=' * 70}")
    print("Kubernetes Image Scanner")
    print(f"Namespace: {namespace}")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'=' * 70}\n")

    # Inicializa cliente Kubernetes
    v1 = inicializar_kubernetes()

    # Obtém pods
    print(f"Obtendo pods do namespace '{namespace}'...")
    pods = obter_pods(v1, namespace)

    if not pods:
        print(f"Nenhum pod encontrado no namespace '{namespace}'")
        return

    print(f"✓ Encontrados {len(pods)} pod(s)\n")

    # Verificar imagens
    pods_com_latest = []
    total_containers = 0

    for pod in pods:
        pod_name = pod.metadata.name
        pod_status = pod.status.phase

        # Verificar containers
        if pod.spec.containers:
            for container in pod.spec.containers:
                total_containers += 1
                container_name = container.name
                image = container.image

                print(f"Pod: {pod_name}")
                print(f"  Container: {container_name}")
                print(f"  Imagem: {image}")
                print(f"  Status: {pod_status}")

                if verificar_imagem_latest(image):
                    print("  ⚠️  ALERTA: Usando tag 'latest'!")
                    pods_com_latest.append(
                        {
                            "pod": pod_name,
                            "container": container_name,
                            "image": image,
                            "status": pod_status,
                        }
                    )
                else:
                    print("  ✓ OK: Imagem pinada")

                print()

        # Verificar init containers (se houver)
        if pod.spec.init_containers:
            for container in pod.spec.init_containers:
                total_containers += 1
                container_name = container.name
                image = container.image

                print(f"Pod: {pod_name}")
                print(f"  Init Container: {container_name}")
                print(f"  Imagem: {image}")

                if verificar_imagem_latest(image):
                    print("  ⚠️  ALERTA: Usando tag 'latest'!")
                    pods_com_latest.append(
                        {
                            "pod": pod_name,
                            "container": f"{container_name} (init)",
                            "image": image,
                            "status": pod_status,
                        }
                    )
                else:
                    print("  ✓ OK: Imagem pinada")

                print()

    # Resumo
    print(f"{'=' * 70}")
    print("RESUMO:")
    print(f"  Total de pods: {len(pods)}")
    print(f"  Total de containers: {total_containers}")
    print(f"  Containers com 'latest': {len(pods_com_latest)}")
    print(f"{'=' * 70}\n")

    # Enviar alertas se houver problemas
    if pods_com_latest:
        mensagem = (
            f"ALERTA: Encontrados {len(pods_com_latest)} container(s) "
            f"usando tag 'latest' no namespace '{namespace}'"
        )
        envia_alerta(mensagem)
        print(f"⚠️  {mensagem}\n")

        # Detalhar cada container com problema
        print("Detalhes dos containers com tag 'latest':")
        for item in pods_com_latest:
            detalhe = (
                f"  - Pod: {item['pod']}, "
                f"Container: {item['container']}, "
                f"Imagem: {item['image']}, "
                f"Status: {item['status']}"
            )
            print(detalhe)
            envia_alerta(detalhe)

        print()
    else:
        print("✓ Nenhum container usando tag 'latest' encontrado!")


def main():
    """Função principal."""
    # Lê namespace das variáveis de ambiente ou usa 'default'
    namespace = os.getenv("SCAN_NAMESPACE", "default")

    print("Iniciando Kubernetes Image Scanner...")
    print(f"Namespace configurado: {namespace}\n")

    try:
        scan(namespace)
    except Exception as e:
        print(f"Erro durante o scan: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)

    print("\nScan concluído!")


if __name__ == "__main__":
    main()
