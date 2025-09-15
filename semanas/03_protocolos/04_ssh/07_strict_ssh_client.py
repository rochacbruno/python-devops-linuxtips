# /// script
# dependencies = ["paramiko"] 
# ///
import paramiko
import os

class StrictSSHClient(paramiko.SSHClient):
    def __init__(self):
        super().__init__()
        # Carregar known_hosts
        self.load_system_host_keys()
        self.load_host_keys(os.path.expanduser('~/.ssh/known_hosts'))
        
        # Política estrita - rejeitar hosts desconhecidos
        self.set_missing_host_key_policy(paramiko.RejectPolicy())