# /// script
# dependencies = ["paramiko"] 
# ///
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