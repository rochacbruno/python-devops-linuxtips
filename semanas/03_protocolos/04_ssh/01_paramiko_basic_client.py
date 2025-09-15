# /// script
# dependencies = ["paramiko"] 
# ///
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

# Para usar com cliente real, remover esta linha:
paramiko.SSHClient = MockSSHClient

# Usar cliente
ssh = paramiko.SSHClient()
ssh.connect('192.168.1.100', username='admin', password='secret')

# Executar comandos
for cmd in ['hostname', 'df -h', 'uptime']:
    print(f"\n$ {cmd}")
    stdin, stdout, stderr = ssh.exec_command(cmd)
    print(stdout.read().decode().strip())

ssh.close()