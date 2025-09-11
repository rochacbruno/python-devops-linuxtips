---
title: SSH em Python
sub_title: Automação e acesso remoto seguro
author: Bruno Rocha - LINUXtips
options:
  implicit_slide_ends: true
  end_slide_shorthand: true
  incremental_lists: true
---

SSH
===

<!-- alignment: center -->

# 🔐 SSH

Secure Shell Protocol

<!-- pause --> 

### Python para DevOps
#### Protocolos de Comunicação


O que é SSH?
===

## 🔒 Protocolo de Acesso Remoto Seguro

- **S**ecure **S**hell - Substituto seguro do Telnet
- Protocolo criptografado para acesso remoto
- Padrão de facto para administração Linux/Unix
- Porta padrão: **22**

<!-- pause -->

### Mais que um Terminal
- 🖥️ **Shell remoto** - Executar comandos
- 📁 **SFTP** - Transferência de arquivos
- 🔀 **Port forwarding** - Túneis seguros
- 🔑 **Autenticação** - Chaves públicas/privadas


Qual Problema Resolve?
===

## 🎯 Administração Remota Segura

### Problemas que SSH resolve:

- **Acesso remoto** criptografado a servidores
- **Automação** de tarefas em máquinas remotas
- **Transferência segura** de arquivos
- **Túneis seguros** para outros protocolos
- **Autenticação forte** sem senhas
- **Auditoria** e controle de acesso

<!-- pause -->

> Antes do SSH, usávamos Telnet e FTP.
> Tudo em texto puro na rede! 😱


Como SSH Funciona?
===

## 🔄 Handshake e Criptografia

```mermaid +render
sequenceDiagram
    participant Client
    participant Server
    
    Client->>Server: Connection Request (port 22)
    Server->>Client: Server Public Key
    Client->>Client: Verify Host Key
    Client->>Server: Encrypted Session Key
    Server->>Client: Authentication Challenge
    Client->>Server: Auth (Password/Key)
    Server->>Client: Access Granted
    Client<->Server: Encrypted Communication
```

### Camadas
1. **Transport** - Criptografia e integridade
2. **Authentication** - Validação do usuário
3. **Connection** - Canais multiplexados


Autenticação SSH
===

## 🔑 Métodos de Autenticação

<!-- column_layout: [1, 1] -->
<!-- column: 0 -->

### Password
```bash
ssh user@server
# Digite a senha
```
❌ Menos seguro
❌ Não automatizável
❌ Brute force

### Host-based
Confiança por hostname
❌ Raramente usado

<!-- column: 1 -->

### Public Key
```bash
ssh-keygen -t ed25519
ssh-copy-id user@server
ssh user@server  # Sem senha!
```
✅ Mais seguro
✅ Automatizável
✅ Sem senha na rede


Exemplos do Mundo Real
===

## 🌍 SSH em DevOps

- **Ansible**: Execução remota via SSH
- **GitHub/GitLab**: Git over SSH
- **CI/CD**: Deploy via SSH (Jenkins, GitLab CI)
- **Kubernetes**: kubectl exec usa SSH internamente
- **Bastion Hosts**: Jump servers para acesso
- **Backup**: rsync over SSH
- **Monitoring**: Coleta de métricas via SSH

<!-- pause -->

**Qualquer automação Linux passa por SSH!**


Cliente SSH com Paramiko
===

## 🐍 Biblioteca Python para SSH

```python +exec
# pip install paramiko
import paramiko
import io

# Simular conexão SSH
class MockSSHClient:
    def connect(self, hostname, username, password):
        print(f"🔗 Conectando a {username}@{hostname}")
    
    def exec_command(self, command):
        outputs = {
            'hostname': 'server01.example.com\n',
            'df -h': 'Filesystem      Size  Used Avail Use% Mounted on\n/dev/sda1        20G  5.5G   14G  30% /\n',
            'uptime': ' 10:42:31 up 45 days,  3:21,  2 users,  load average: 0.15, 0.12, 0.09\n'
        }
        stdin = io.StringIO()
        stdout = io.StringIO(outputs.get(command, f"Executado: {command}\n"))
        stderr = io.StringIO()
        return stdin, stdout, stderr
    
    def close(self):
        print("🔌 Conexão fechada")

# Usar cliente
ssh = MockSSHClient()
ssh.connect('192.168.1.100', username='admin', password='secret')

# Executar comandos
for cmd in ['hostname', 'df -h', 'uptime']:
    print(f"\n$ {cmd}")
    stdin, stdout, stderr = ssh.exec_command(cmd)
    print(stdout.read().strip())

ssh.close()
```


Executando Comandos
===

## 📝 Comandos Remotos com Paramiko

```python
import paramiko

def execute_remote_command(host, username, command, key_file=None):
    """Executa comando em servidor remoto"""
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        if key_file:
            # Autenticação por chave
            key = paramiko.RSAKey.from_private_key_file(key_file)
            ssh.connect(host, username=username, pkey=key)
        else:
            # Autenticação por senha
            ssh.connect(host, username=username, password='senha')
        
        # Executar comando
        stdin, stdout, stderr = ssh.exec_command(command)
        
        # Retornar saída
        return {
            'stdout': stdout.read().decode(),
            'stderr': stderr.read().decode(),
            'exit_code': stdout.channel.recv_exit_status()
        }
    
    finally:
        ssh.close()

# Usar
result = execute_remote_command(
    'server.example.com',
    'admin',
    'docker ps --format "table {{.Names}}\t{{.Status}}"'
)
```


SFTP - Transferência de Arquivos
===

## 📁 Upload/Download Seguro

```python
import paramiko

def sftp_operations(host, username, password):
    """Operações SFTP"""
    
    # Criar cliente SSH
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, username=username, password=password)
    
    # Abrir sessão SFTP
    sftp = ssh.open_sftp()
    
    try:
        # Upload
        local_file = '/local/config.yaml'
        remote_file = '/remote/config.yaml'
        sftp.put(local_file, remote_file)
        print(f"📤 Upload: {local_file} → {remote_file}")
        
        # Download
        sftp.get('/remote/backup.tar.gz', '/local/backup.tar.gz')
        print(f"📥 Download: backup.tar.gz")
        
        # Listar diretório
        files = sftp.listdir('/remote/logs')
        print(f"📂 Arquivos em /remote/logs: {files}")
        
        # Criar diretório
        sftp.mkdir('/remote/new_dir')
        
        # Remover arquivo
        sftp.remove('/remote/old_file.txt')
        
    finally:
        sftp.close()
        ssh.close()
```


SSH com Chaves
===

## 🔑 Autenticação por Chave Pública

```python +exec
import os

# Gerar par de chaves (fazer uma vez)
print("🔑 Gerando par de chaves SSH...")
print("$ ssh-keygen -t ed25519 -C 'admin@example.com'")
print("Generating public/private ed25519 key pair.")
print("Your identification has been saved in ~/.ssh/id_ed25519")
print("Your public key has been saved in ~/.ssh/id_ed25519.pub")

# Simular uso com Paramiko
print("\n📝 Código Python para usar chave:")
print("""
import paramiko

# Carregar chave privada
private_key = paramiko.Ed25519Key.from_private_key_file(
    '/home/user/.ssh/id_ed25519'
)

# Conectar usando chave
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(
    hostname='server.example.com',
    username='admin',
    pkey=private_key  # Usar chave ao invés de senha
)

# Executar comando
stdin, stdout, stderr = ssh.exec_command('whoami')
print(stdout.read().decode())  # admin
""")
```


Port Forwarding (Túneis)
===

## 🔀 Túneis SSH

### Local Forward
```bash
# Acessar banco remoto via localhost
ssh -L 3307:database.internal:3306 user@jumphost

# Agora: mysql -h localhost -P 3307
```

### Remote Forward
```bash
# Expor serviço local para servidor remoto
ssh -R 8080:localhost:3000 user@server
```

### Dynamic (SOCKS Proxy)
```bash
# Proxy SOCKS5 via SSH
ssh -D 9090 user@server
# Configure browser: SOCKS5 localhost:9090
```

### Com Python
```python
import paramiko
import socket
import select

def create_tunnel(ssh_client, remote_host, remote_port, local_port):
    """Cria túnel SSH (port forwarding)"""
    transport = ssh_client.get_transport()
    
    local_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    local_socket.bind(('localhost', local_port))
    local_socket.listen(1)
    
    # Forward connections...
```


SSH Config File
===

## 📋 Configuração Avançada

### ~/.ssh/config
```bash
# Servidor de produção
Host prod
    HostName production.example.com
    User admin
    Port 22
    IdentityFile ~/.ssh/prod_key
    
# Bastion/Jump host
Host internal
    HostName 10.0.1.50
    User developer
    ProxyJump bastion
    
# Múltiplos servidores
Host web-*
    User www-data
    IdentityFile ~/.ssh/web_key
    StrictHostKeyChecking no
```

### Usar com Paramiko
```python
import paramiko

# Carregar config
config = paramiko.SSHConfig()
with open(os.path.expanduser('~/.ssh/config')) as f:
    config.parse(f)

# Usar configuração
host_config = config.lookup('prod')
ssh.connect(
    hostname=host_config['hostname'],
    username=host_config['user'],
    key_filename=host_config['identityfile']
)
```


Parallel SSH
===

## ⚡ Execução em Múltiplos Servidores

```python +exec
# pip install parallel-ssh
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

def ssh_command(host, command):
    """Simula execução SSH"""
    time.sleep(0.1)  # Simular latência
    return f"{host}: {command} executado"

# Lista de servidores
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
```


Ansible-like com Python
===

## 🤖 Automação Estilo Ansible

```python
import paramiko
import yaml
from typing import List, Dict

class SimpleAutomation:
    def __init__(self, inventory_file):
        with open(inventory_file) as f:
            self.inventory = yaml.safe_load(f)
        self.results = []
    
    def run_task(self, host: str, task: Dict):
        """Executa uma task em um host"""
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        try:
            # Conectar
            ssh.connect(
                host, 
                username=self.inventory['vars']['ansible_user'],
                key_filename=self.inventory['vars']['ansible_ssh_key']
            )
            
            # Executar comando
            if task['module'] == 'shell':
                stdin, stdout, stderr = ssh.exec_command(task['args'])
                return stdout.read().decode()
            
            elif task['module'] == 'copy':
                sftp = ssh.open_sftp()
                sftp.put(task['src'], task['dest'])
                return f"Copied {task['src']} to {task['dest']}"
            
        finally:
            ssh.close()
    
    def run_playbook(self, playbook: List[Dict]):
        """Executa playbook em todos os hosts"""
        for task in playbook:
            print(f"\n📋 Task: {task['name']}")
            
            for host in self.inventory['hosts']:
                result = self.run_task(host, task)
                print(f"  ✅ {host}: {result[:50]}...")
```


SSH Jump Host (Bastion)
===

## 🏰 Acesso via Bastion

```python
import paramiko

def connect_via_jump_host(target_host, target_user, 
                          jump_host, jump_user, jump_key):
    """Conecta a servidor interno via jump host"""
    
    # 1. Conectar ao jump host
    jump_client = paramiko.SSHClient()
    jump_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    jump_client.connect(
        jump_host,
        username=jump_user,
        key_filename=jump_key
    )
    
    # 2. Criar canal para o servidor interno
    jump_transport = jump_client.get_transport()
    dest_addr = (target_host, 22)
    local_addr = ('127.0.0.1', 22)
    channel = jump_transport.open_channel(
        "direct-tcpip", dest_addr, local_addr
    )
    
    # 3. Conectar ao servidor interno através do canal
    target_client = paramiko.SSHClient()
    target_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    target_client.connect(
        target_host,
        username=target_user,
        sock=channel  # Usar canal do jump host
    )
    
    return target_client, jump_client

# Usar
target, jump = connect_via_jump_host(
    '10.0.1.50', 'admin',     # Servidor interno
    'bastion.example.com', 'user', '~/.ssh/bastion_key'
)

stdin, stdout, stderr = target.exec_command('hostname')
print(stdout.read().decode())
```


Monitoramento via SSH
===

## 📊 Coleta de Métricas

```python +exec
import json
from datetime import datetime

def collect_metrics(hosts):
    """Coleta métricas de múltiplos servidores"""
    
    metrics = {}
    
    for host in hosts:
        print(f"📊 Coletando métricas de {host}...")
        
        # Simular coleta
        metrics[host] = {
            'timestamp': datetime.now().isoformat(),
            'cpu': {
                'usage': 45.2,
                'load_avg': [0.5, 0.7, 0.8]
            },
            'memory': {
                'total_gb': 16,
                'used_gb': 8.5,
                'percent': 53.1
            },
            'disk': {
                '/': {'used_percent': 67},
                '/var': {'used_percent': 45}
            },
            'services': {
                'nginx': 'running',
                'postgresql': 'running',
                'redis': 'stopped'
            }
        }
    
    return metrics

# Coletar de múltiplos servidores
servers = ['web01', 'web02', 'db01']
metrics = collect_metrics(servers)

# Analisar
for host, data in metrics.items():
    print(f"\n🖥️ {host}:")
    print(f"  CPU: {data['cpu']['usage']}%")
    print(f"  Memory: {data['memory']['percent']}%")
    
    # Alertas
    if data['memory']['percent'] > 80:
        print(f"  ⚠️ ALERTA: Memória alta!")
    
    for service, status in data['services'].items():
        if status != 'running':
            print(f"  ❌ Serviço {service} está {status}")
```


Deploy Automatizado
===

## 🚀 Deploy via SSH

```python
import paramiko
from datetime import datetime

class Deployer:
    def __init__(self, host, user, key_file):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(host, username=user, key_filename=key_file)
    
    def deploy(self, app_name, version):
        """Deploy de aplicação"""
        
        steps = [
            # 1. Backup atual
            f"cp -r /apps/{app_name} /backups/{app_name}_{datetime.now():%Y%m%d}",
            
            # 2. Pull nova versão
            f"cd /apps/{app_name} && git fetch && git checkout {version}",
            
            # 3. Instalar dependências
            f"cd /apps/{app_name} && pip install -r requirements.txt",
            
            # 4. Migrar banco
            f"cd /apps/{app_name} && python manage.py migrate",
            
            # 5. Restart serviço
            f"systemctl restart {app_name}",
            
            # 6. Health check
            f"curl -f http://localhost:8000/health || exit 1"
        ]
        
        for i, cmd in enumerate(steps, 1):
            print(f"Step {i}/{len(steps)}: {cmd[:50]}...")
            
            stdin, stdout, stderr = self.ssh.exec_command(cmd)
            exit_code = stdout.channel.recv_exit_status()
            
            if exit_code != 0:
                print(f"❌ Falha no step {i}")
                print(stderr.read().decode())
                
                # Rollback
                self.rollback(app_name)
                return False
        
        print("✅ Deploy concluído com sucesso!")
        return True
```


SSH Agent Forwarding
===

## 🔐 Encaminhamento de Chaves

```python
import paramiko
import os

def connect_with_agent_forwarding(hostname, username):
    """Conecta com agent forwarding habilitado"""
    
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    # Usar SSH agent local
    agent = paramiko.Agent()
    agent_keys = agent.get_keys()
    
    if not agent_keys:
        raise Exception("Nenhuma chave no SSH agent")
    
    # Conectar usando chave do agent
    ssh.connect(
        hostname,
        username=username,
        pkey=agent_keys[0],
        allow_agent=True,  # Permitir agent
        look_for_keys=False
    )
    
    # Agora pode fazer SSH para outros servers
    # sem copiar a chave privada
    stdin, stdout, stderr = ssh.exec_command(
        'ssh git@github.com "git clone repo.git"'
    )
    
    return ssh

# Configurar agent localmente
# ssh-add ~/.ssh/id_rsa
# ssh -A user@server  # -A habilita forwarding
```


Segurança SSH
===

## 🔒 Boas Práticas

### Configuração Segura (/etc/ssh/sshd_config)
```bash
# Desabilitar root login
PermitRootLogin no

# Apenas autenticação por chave
PasswordAuthentication no
PubkeyAuthentication yes

# Limitar usuários
AllowUsers admin developer

# Timeout de inatividade
ClientAliveInterval 300
ClientAliveCountMax 2

# Versão do protocolo
Protocol 2

# Fail2ban para proteção contra brute force
```

### Python - Validação de Host Key
```python
import paramiko

class StrictSSHClient(paramiko.SSHClient):
    def __init__(self):
        super().__init__()
        # Carregar known_hosts
        self.load_system_host_keys()
        self.load_host_keys(os.path.expanduser('~/.ssh/known_hosts'))
        
        # Política estrita - rejeitar hosts desconhecidos
        self.set_missing_host_key_policy(paramiko.RejectPolicy())
```


Logs e Auditoria
===

## 📝 Monitoramento de Acesso

```python +exec
import json
from datetime import datetime

class SSHAuditor:
    def __init__(self):
        self.log_file = '/var/log/ssh_audit.json'
        self.sessions = []
    
    def log_session(self, user, host, command, result):
        """Registra atividade SSH"""
        
        session = {
            'timestamp': datetime.now().isoformat(),
            'user': user,
            'host': host,
            'command': command,
            'exit_code': result.get('exit_code', 0),
            'duration_ms': result.get('duration', 0)
        }
        
        self.sessions.append(session)
        
        # Salvar em arquivo
        # with open(self.log_file, 'a') as f:
        #     f.write(json.dumps(session) + '\n')
        
        # Alertas
        if 'rm -rf' in command:
            print(f"⚠️ ALERTA: Comando perigoso detectado!")
        
        if result.get('exit_code') != 0:
            print(f"❌ Comando falhou: {command}")
    
    def generate_report(self):
        """Gera relatório de atividades"""
        print("\n📊 Relatório de Auditoria SSH")
        print("-" * 40)
        
        for s in self.sessions[-5:]:
            print(f"{s['timestamp'][:19]} | {s['user']}@{s['host']}")
            print(f"  Comando: {s['command'][:50]}")
            print(f"  Status: {'✅' if s['exit_code'] == 0 else '❌'}")

# Exemplo de uso
auditor = SSHAuditor()
auditor.log_session('admin', 'web01', 'systemctl restart nginx', {'exit_code': 0, 'duration': 1250})
auditor.log_session('dev', 'db01', 'rm -rf /tmp/*', {'exit_code': 0, 'duration': 500})
auditor.generate_report()
```


SSH Multiplexing
===

## 🔀 Reutilização de Conexões

### Configuração (~/.ssh/config)
```bash
Host *
    ControlMaster auto
    ControlPath ~/.ssh/sockets/%r@%h-%p
    ControlPersist 600
```

### Com Paramiko
```python
import paramiko
import threading

class SSHConnectionPool:
    """Pool de conexões SSH reutilizáveis"""
    
    def __init__(self, max_connections=10):
        self.pool = {}
        self.lock = threading.Lock()
        self.max_connections = max_connections
    
    def get_connection(self, host, username, **kwargs):
        """Pega ou cria conexão"""
        
        key = f"{username}@{host}"
        
        with self.lock:
            if key in self.pool:
                # Reutilizar conexão existente
                return self.pool[key]
            
            # Criar nova conexão
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(host, username=username, **kwargs)
            
            self.pool[key] = ssh
            return ssh
    
    def close_all(self):
        """Fecha todas as conexões"""
        for ssh in self.pool.values():
            ssh.close()
        self.pool.clear()
```


Exercício Prático
===

## 💪 Mãos à Obra!

### Desafio: Sistema de Backup Distribuído

Crie um sistema que:
1. Conecte a múltiplos servidores via SSH
2. Execute backup de diretórios específicos
3. Transfira backups via SFTP
4. Gere relatório de status
5. Envie notificação em caso de falha

### Requisitos:
- Parallelização de operações
- Retry em caso de falha
- Compressão antes da transferência
- Rotação de backups antigos

<!-- pause -->

```python
class BackupManager:
    def backup_server(self, server):
        # 1. SSH para criar tar.gz
        # 2. SFTP para download
        # 3. Verificar integridade
        # 4. Limpar remoto
        pass
```


Fabric - Automação Simplificada
===

## 🧵 Framework de Deploy

```python
# pip install fabric
from fabric import Connection, task

@task
def deploy(c):
    """Deploy da aplicação"""
    
    # Conectar
    with Connection('user@server.com') as conn:
        # Git pull
        with conn.cd('/app'):
            conn.run('git pull origin main')
            
        # Instalar deps
        conn.run('pip install -r requirements.txt')
        
        # Restart
        conn.sudo('systemctl restart myapp')
        
        # Verificar
        result = conn.run('curl -s localhost:8000/health')
        if 'ok' in result.stdout:
            print("✅ Deploy successful!")

# Executar: fab deploy
```

### Múltiplos Servidores
```python
from fabric import Group

servers = Group('web1', 'web2', 'web3')
results = servers.run('uptime')

for conn, result in results.items():
    print(f"{conn.host}: {result.stdout}")
```


Recursos e Próximos Passos
===

## 📚 Continue Aprendendo!

### Documentação
- [Paramiko Documentation](https://www.paramiko.org/)
- [OpenSSH Manual](https://www.openssh.com/manual.html)
- [Fabric Documentation](https://www.fabfile.org/)

### Ferramentas Relacionadas
- **Ansible**: Automação declarativa
- **Salt**: Execução remota em massa
- **Puppet/Chef**: Configuration management
- **Teleport**: SSH moderno com auditoria

### Próxima Aula
**MCP** - Model Context Protocol
- Protocolo moderno para LLMs
- Integração com ferramentas
- Automação inteligente


Conclusão
===

## 🎯 O que Aprendemos

<!-- font_size: 1 -->

✅ SSH é **fundamental** para administração Linux

✅ Python + Paramiko = **automação poderosa**

✅ Segurança via **chaves públicas** é essencial

✅ SSH vai além do terminal: **túneis, SFTP, forwarding**

<!-- pause -->

> "SSH é a porta de entrada para o mundo DevOps.
> Domine SSH e você dominará a automação de infraestrutura."
> 
> -- Todo SRE experiente