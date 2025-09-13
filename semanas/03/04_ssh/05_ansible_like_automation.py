# /// script
# dependencies = ["paramiko", "pyyaml"] 
# ///
import paramiko
import yaml
from typing import List, Dict

class SimpleAutomation:
    def __init__(self, inventory_file):
        with open(inventory_file) as f:
            self.inventory = yaml.safe_load(f) # hosts: ...
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

# Exemplo de uso
if __name__ == "__main__":
    # automation = SimpleAutomation('inventory.yaml')
    # playbook = yaml.safe_load(open('playbook.yaml'))
    # automation.run_playbook(playbook)
    print("Exemplo: automation = SimpleAutomation('inventory.yaml')")
    print("Exemplo: playbook = yaml.safe_load(open('playbook.yaml'))")
    print("Exemplo: automation.run_playbook(playbook)")