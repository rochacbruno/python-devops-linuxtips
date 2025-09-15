# /// script
# dependencies = [
#     "jsonrpclib-pelix",
# ]
# ///
import json
import threading
import time
from jsonrpclib import Server
from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer

class MetricsServer:
    def calculate_metrics(self, cpu_usage, memory_usage):
        """Calcular métricas de sistema"""
        return {
            "avg_cpu": sum(cpu_usage) / len(cpu_usage),
            "max_cpu": max(cpu_usage),
            "avg_memory": sum(memory_usage) / len(memory_usage),
            "alert": max(cpu_usage) > 80
        }
    
    def get_system_info(self):
        """Retornar informações do sistema"""
        return {
            "server": "MetricsServer", "version": "1.0", "status": "running"
        }

def start_server():
    """Iniciar o servidor JSON-RPC"""
    server = SimpleJSONRPCServer(('localhost', 8001))
    server.register_instance(MetricsServer())
    print("Servidor JSON-RPC iniciado em http://localhost:8001")
    server.serve_forever()

# ---- Cliente: Em outro computador ----
def run_client():
    """Executar cliente JSON-RPC"""
    client = Server('http://localhost:8001')
    # Dados de exemplo
    cpu_data = [45, 67, 89, 34, 56]
    memory_data = [2.1, 2.3, 2.5, 2.2, 2.4]
    print("🔗 Conectando ao servidor JSON-RPC...")
    # Chamar método remoto
    result = client.calculate_metrics(cpu_data, memory_data)
    print("\n📊 Métricas calculadas:")
    print(json.dumps(result, indent=2))
    # Chamar outro método
    info = client.get_system_info()
    print("\n📋 Informações do servidor:")
    print(json.dumps(info, indent=2))

if __name__ == "__main__":
    # Iniciar servidor em thread separada
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    # Aguardar servidor inicializar
    time.sleep(1)
    # Executar cliente
    run_client()
    print("\n✅ Exemplo JSON-RPC concluído!")