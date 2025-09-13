# /// script
# dependencies = [] 
# ///
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
if __name__ == "__main__":
    auditor = SSHAuditor()
    auditor.log_session('admin', 'web01', 'systemctl restart nginx', {'exit_code': 0, 'duration': 1250})
    auditor.log_session('dev', 'db01', 'rm -rf /tmp/*', {'exit_code': 0, 'duration': 500})
    auditor.generate_report()