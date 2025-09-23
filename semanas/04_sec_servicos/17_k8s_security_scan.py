#!/usr/bin/env python3
# /// script
# dependencies = ["kubernetes"]
# ///
import subprocess
import smtplib
from email.mime.text import MIMEText

def send_alert(subject: str, body: str, to_email: str):
    """Envia alerta por email"""
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = "sysadmin"
    msg['To'] = to_email
    with smtplib.SMTP('smtp.example.com') as server:
        server.login('user', 'password')
        server.send_message(msg)

def scan_image(image: str) -> str:
    """Escaneia imagem Docker usando Trivy"""
    try:
        result = subprocess.run(
            ['trivy', 'image', '--severity', 'CRITICAL', image],
            capture_output=True, text=True, check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Erro ao escanear {image}:\n{e.stderr}"

# Exemplo de uso
from kubernetes import client, config
config.load_kube_config()
v1 = client.CoreV1Api()
pods = v1.list_pod_for_all_namespaces(watch=False)
for pod in pods.items:
    for container in pod.spec.containers:
        image = container.image
        scan_result = scan_image(image)
        if "CRITICAL" in scan_result:
            send_alert(
                subject=f"Alerta de Vulnerabilidade Crítica na imagem {image}",
                body=scan_result,
                to_email="support"
            )