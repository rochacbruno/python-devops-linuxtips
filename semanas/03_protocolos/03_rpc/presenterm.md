---
title: RPC e gRPC em Python
sub_title: Chamadas remotas de procedimento
author: Bruno Rocha - LINUXtips
options:
  implicit_slide_ends: true
  end_slide_shorthand: true
  incremental_lists: true
---

RPC e gRPC
===
<!-- font_size: 2 -->
<!-- alignment: center -->

# 🔄 RPC e gRPC

Remote Procedure Call & Google RPC




O que é RPC?
===

<!-- font_size: 2 -->
## 📡 Remote Procedure Call

- Chamar funções em **servidores remotos**
- Como se fossem **funções locais**
- Abstrai a complexidade de rede
- Cliente não precisa conhecer detalhes de rede

<!-- pause -->

### Conceito Simples
```python
# Local
result = calculate_tax(1000.00)

# Remoto (RPC)
result = remote_server.calculate_tax(1000.00)
#         ↑ Parece local, mas executa em outro servidor!
```


O que é gRPC?
===

<!-- font_size: 2 -->
## 🚀 Google RPC

- Framework RPC criado pelo Google
- Usa **Protocol Buffers** (protobuf)
- Suporta **múltiplas linguagens**
- Baseado em **HTTP/2**
- **Streaming** bidirecional

<!-- pause -->

### Características
- ⚡ **Alta performance** (binário, não JSON)
- 📝 **Fortemente tipado** (schema .proto)
- 🔄 **Streaming** nativo
- 🌐 **Poliglota** (Python, Go, Java, etc)


Qual Problema Resolvem?
===

<!-- font_size: 2 -->

### RPC/gRPC resolvem:

- **Microserviços** comunicando eficientemente
- **Latência** menor que REST/JSON
- **Tipagem forte** entre serviços
- **Streaming** de dados em tempo real
- **Versionamento** de APIs
- **Code generation** automático

<!-- pause -->

> REST é ótimo para APIs públicas.
> gRPC é perfeito para comunicação interna!


RPC vs REST
===

<!-- font_size: 2 -->
## 🆚 Comparação

<!-- column_layout: [1, 1] -->
<!-- column: 0 -->

### REST
```http
POST /api/users HTTP/1.1
Content-Type: application/json

{"name": "João", "age": 30}
```

- Orientado a **recursos**
- Verbos HTTP (GET, POST...)
- JSON/XML (texto)
- Stateless
- Cache friendly

<!-- column: 1 -->

### RPC/gRPC
```python
client.CreateUser(
    name="João", 
    age=30
)
```

- Orientado a **ações**
- Métodos/funções
- Binary (protobuf)
- Pode ter estado
- Mais eficiente


Protocol Buffers
===
<!-- alignment: center -->
<!-- font_size: 2 -->
## 📄 Linguagem de Definição

<!-- font_size: 1 -->
### Arquivo .proto
```protobuf
syntax = "proto3";

package users;

// Definir mensagens
message User {
    int32 id = 1;
    string name = 2;
    string email = 3;
    repeated string roles = 4;
}

message CreateUserRequest {
    string name = 1;
    string email = 2;
}

// Definir serviço
service UserService {
    rpc CreateUser(CreateUserRequest) returns (User);
    rpc GetUser(GetUserRequest) returns (User);
    rpc ListUsers(Empty) returns (stream User);
}
```

Exemplos do Mundo Real
===


<!-- font_size: 2 -->


<!-- alignment: center -->

## 🌍 gRPC em DevOps

- **Kubernetes**: Kubelet ↔ API Server
- **etcd**: Distributed key-value store
- **Envoy Proxy**: Service mesh communication
- **Prometheus**: Remote write/read
- **Docker**: Containerd API
- **Terraform**: Provider plugins
- **CNCF Projects**: Maioria usa gRPC

<!-- pause -->

**Google, Netflix, Square, Cisco, CoreOS...**
Todos usam gRPC em produção!


XML-RPC Simples
===

## 📜 RPC Clássico

```python +exec {1-2|7-20|22-26|28-34|1-34}
import xmlrpc.client
from xmlrpc.server import SimpleXMLRPCServer
import threading
import time

# Servidor
def start_server():
    server = SimpleXMLRPCServer(("localhost", 9000), logRequests=False)
    
    # Registrar funções
    server.register_function(lambda x, y: x + y, 'add')
    server.register_function(lambda x, y: x * y, 'multiply')
    server.register_function(lambda s: s.upper(), 'uppercase')
    
    # Timer para parar o servidor após 10 segundos
    timer = threading.Timer(10.0, server.shutdown)
    timer.start()
    
    # Rodar servidor até ser parado pelo timer
    server.serve_forever()

# Iniciar servidor em thread
thread = threading.Thread(target=start_server, daemon=True)
thread.start()

time.sleep(0.5)  # Aguardar servidor


# ------ Cliente:  Em outro computador ------
client = xmlrpc.client.ServerProxy("http://localhost:9000")

print(f"5 + 3 = {client.add(5, 3)}")
print(f"4 × 7 = {client.multiply(4, 7)}")
print(f"'hello' → '{client.uppercase('hello')}'")
```


JSON-RPC Moderno
===

## 🔧 RPC com JSON

<!-- column_layout: [1, 1] -->
<!-- column: 0 -->


```python +exec:uv +id:jj {4-5|7-20|23-28|31-50|1-52}
/// # /// script
/// # dependencies = [
/// #     "jsonrpclib-pelix",
/// # ]
/// # ///
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

/// if __name__ == "__main__":
///     # Iniciar servidor em thread separada
///     server_thread = threading.Thread(target=start_server, daemon=True)
///     server_thread.start()
///     # Aguardar servidor inicializar
///     time.sleep(1)
///     # Executar cliente
///     run_client()
///     print("\n✅ Exemplo JSON-RPC concluído!")
```

<!-- column: 1 -->

<!-- snippet_output: jj -->



gRPC: Instalação
===

<!-- alignment: center -->

## 📦 Setup do Ambiente

```bash
# Instalar gRPC e ferramentas
pip install grpcio grpcio-tools

# Estrutura do projeto
project/
├── protos/
│   └── service.proto    # Definições
├── generated/
│   ├── service_pb2.py   # Messages
│   └── service_pb2_grpc.py  # Services
├── server.py
└── client.py
```

### Compilar .proto
```bash
python -m grpc_tools.protoc \
    -I./protos \
    --python_out=./generated \
    --grpc_python_out=./generated \
    ./protos/service.proto
```


gRPC: Definindo Serviço
===

<!-- alignment: center -->
## 📝 metrics.proto

```protobuf {1-3|5-26|28-34|1-34}
syntax = "proto3";

package monitoring;

// Mensagens
message MetricRequest {
    string hostname = 1;
    string metric_type = 2;  // cpu, memory, disk
}

message MetricResponse {
    string hostname = 1;
    string metric_type = 2;
    double value = 3;
    int64 timestamp = 4;
    string unit = 5;
}

message HealthRequest {
    string service = 1;
}

message HealthResponse {
    bool healthy = 1;
    string message = 2;
}

// Serviço
service MonitoringService {
    rpc GetMetric(MetricRequest) returns (MetricResponse);
    rpc StreamMetrics(MetricRequest) returns (stream MetricResponse);
    rpc CheckHealth(HealthRequest) returns (HealthResponse);
}
```


gRPC: Servidor Python
===

<!-- alignment: center -->
## 🖥️ Implementando Servidor

```python {7-8|10|12-35|1-36}
import grpc
from concurrent import futures
import time
import random

# Import dos arquivos gerados
import metrics_pb2
import metrics_pb2_grpc

class MonitoringService(metrics_pb2_grpc.MonitoringServiceServicer):
    
    def GetMetric(self, request, context):
        """Retorna uma métrica"""
        value = random.uniform(0, 100)
        
        return metrics_pb2.MetricResponse(
            hostname=request.hostname,
            metric_type=request.metric_type,
            value=value,
            timestamp=int(time.time()),
            unit="percent" if request.metric_type == "cpu" else "GB"
        )
    
    def StreamMetrics(self, request, context):
        """Stream de métricas"""
        for i in range(10):
            yield self.GetMetric(request, context)
            time.sleep(1)
    
    def CheckHealth(self, request, context):
        """Health check"""
        return metrics_pb2.HealthResponse(
            healthy=True,
            message=f"Service {request.service} is running"
        )
```


gRPC: Cliente Python
===

<!-- alignment: center -->
## 💻 Consumindo Serviço

```python +line_numbers {2-3|7-8|10-18|20-29|30-34|1-34}
import grpc
import metrics_pb2
import metrics_pb2_grpc

def run_client():
    # Conectar ao servidor
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = metrics_pb2_grpc.MonitoringServiceStub(channel)
        
        # 1. Chamada simples
        print("📊 Métrica única:")
        response = stub.GetMetric(
            metrics_pb2.MetricRequest(
                hostname="server01",
                metric_type="cpu"
            )
        )
        print(f"  CPU: {response.value:.1f}%")
        
        # 2. Stream de métricas
        print("\n📈 Stream de métricas:")
        request = metrics_pb2.MetricRequest(
            hostname="server01",
            metric_type="memory"
        )
        
        for metric in stub.StreamMetrics(request):
            print(f"  Memory: {metric.value:.2f} GB")
        
        # 3. Health check
        health = stub.CheckHealth(
            metrics_pb2.HealthRequest(service="api")
        )
        print(f"\n❤️ Health: {health.message}")
```
Tipos de RPC em gRPC
===

<!-- alignment: center -->
## 🔄 4 Tipos de Comunicação

### 1️⃣ Unary (Request-Response)
```python
def GetUser(request) -> response:
    return user
```

### 2️⃣ Server Streaming
```python
def ListUsers(request) -> stream response:
    for user in users:
        yield user
```

### 3️⃣ Client Streaming
```python
def UploadFile(stream request) -> response:
    for chunk in request:
        process(chunk)
    return result
```

### 4️⃣ Bidirectional Streaming
```python
def Chat(stream request) -> stream response:
    for message in request:
        yield process(message)
```

Load Balancing
===

<!-- alignment: center -->
## ⚖️ Distribuição de Carga

```python
import grpc
import random

class LoadBalancedChannel:
    def __init__(self, addresses):
        self.channels = [
            grpc.insecure_channel(addr) 
            for addr in addresses
        ]
    
    def get_stub(self):
        # Round-robin ou random
        channel = random.choice(self.channels)
        return metrics_pb2_grpc.MonitoringServiceStub(channel)

# Usar com múltiplos servidores
lb = LoadBalancedChannel([
    'server1:50051',
    'server2:50051',
    'server3:50051'
])

stub = lb.get_stub()
response = stub.GetMetric(request)
```

### Alternativas
- **Envoy Proxy**: Load balancer L7
- **Kubernetes Service**: DNS round-robin
- **Consul/Etcd**: Service discovery


Testando gRPC
===

<!-- alignment: center -->
### Testar com grpcurl
```bash
# Listar serviços
grpcurl -plaintext localhost:50051 list

# Descrever serviço
grpcurl -plaintext localhost:50051 describe monitoring.MonitoringService

# Chamar método
grpcurl -plaintext -d '{"hostname":"server01"}' \
    localhost:50051 monitoring.MonitoringService/GetMetric
```

Debugging gRPC
===

<!-- alignment: center -->

### grpcui - Interface Web
```bash
# Instalar
go install github.com/fullstorydev/grpcui/cmd/grpcui@latest

# Rodar UI
grpcui -plaintext localhost:50051
```

### Wireshark
- Decode as HTTP2
- Filter: `http2.header.path contains "grpc"`

### Métricas
```python
# Prometheus metrics
from prometheus_client import Counter, Histogram

grpc_requests = Counter('grpc_requests_total', 'Total gRPC requests')
grpc_duration = Histogram('grpc_request_duration_seconds', 'gRPC request duration')
```

Recursos e Próximos Passos
===

<!-- alignment: center -->
## 📚 Continue Aprendendo!

### Documentação
- [gRPC.io](https://grpc.io/)
- [Protocol Buffers](https://protobuf.dev/)
- [gRPC Python](https://grpc.io/docs/languages/python/)

### Ferramentas
- **BloomRPC**: GUI para testar gRPC
- **grpcurl**: CLI para gRPC
- **ghz**: Load testing para gRPC
- **Buf**: Linting e breaking changes

### Próxima Aula
**SSH** - Secure Shell Protocol
- Automação remota
- Transferência segura
- Túneis e port forwarding


Conclusão
===

## 🎯 O que Aprendemos

<!-- font_size: 1 -->

✅ RPC abstrai **chamadas remotas** como locais

✅ gRPC traz **performance** e **tipo seguro**

✅ Protocol Buffers são **eficientes** e **versionáveis**

✅ Streaming **bidirecional** nativo

<!-- pause -->

> "gRPC é a escolha natural para comunicação 
> entre microserviços em ambientes de alta performance."
> 
> -- Engenheiros do Google, Netflix, e Uber
