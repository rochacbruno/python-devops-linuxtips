# /// script
# dependencies = [] 
# ///
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

def ssh_command(host, command):
    """Simula execução SSH"""
    time.sleep(0.1)  # Simular latência
    # aqui usaria Paramiko para conectar e executar
    return f"{host}: {command} executado"

servers = [
    'web01.example.com',
    'web02.example.com',
    'db01.example.com',
    'cache01.example.com'
]

command = 'systemctl status nginx'
print(f"🚀 Executando '{command}' em {len(servers)} servidores...\n")

# Execução paralela
with ThreadPoolExecutor(max_workers=10) as executor:
    futures = {
        executor.submit(ssh_command, host, command): host 
        for host in servers
    }
    
    for future in as_completed(futures):
        host = futures[future]
        try:
            result = future.result()
            print(f"✅ {result}")
        except Exception as e:
            print(f"❌ {host}: {e}")