---
title: Sockets em Python
sub_title: A base da comunicação em rede
author: Bruno Rocha - LINUXtips
options:
  implicit_slide_ends: true
  end_slide_shorthand: true
  incremental_lists: true
---

Sockets
===

<!-- alignment: center -->

# 🔌 Sockets

A fundação de toda comunicação em rede

<!-- pause --> 

### Python para DevOps
#### Protocolos de Comunicação


O que são Sockets?
===

## 📡 Interface de Comunicação

- **Socket** = Ponto de conexão entre processos
- Interface entre aplicação e protocolo de rede
- Abstração do sistema operacional para I/O de rede

<!-- pause -->

### Analogia Simples

Imagine uma **tomada elétrica** (socket em inglês):
- Você **pluga** um aparelho para usar energia
- Em redes, você **conecta** processos para trocar dados


Qual Problema Resolvem?
===

## 🎯 Comunicação Entre Processos

### Problemas que sockets resolvem:

- Comunicação entre processos em **máquinas diferentes**
- Troca de dados via **rede local ou internet**
- Implementação de **protocolos** (HTTP, SSH, FTP...)
- Criação de **serviços** e **clientes** de rede

<!-- pause -->

> **Sem sockets**, não teríamos: APIs REST, SSH, bancos de dados remotos, microserviços...


Tipos de Sockets
===

<!-- column_layout: [1, 1] -->
<!-- column: 0 -->

## TCP (Stream)
**Confiável e ordenado**

```python
socket.SOCK_STREAM
```

- Garante entrega
- Mantém ordem
- Conexão persistente
- Ex: HTTP, SSH, FTP

<!-- column: 1 -->

## UDP (Datagram)
**Rápido e simples**

```python
socket.SOCK_DGRAM
```

- Sem garantias
- Mais rápido
- Sem conexão
- Ex: DNS, streaming


Exemplos do Mundo Real
===

## 🌍 Onde Usamos Sockets em DevOps?

- **Monitoramento**: Prometheus, Grafana, Datadog
- **Logs**: Fluentd, Logstash enviando para ElasticSearch
- **APIs**: Todo microserviço REST/gRPC
- **Bancos**: PostgreSQL, Redis, MongoDB
- **Mensageria**: RabbitMQ, Kafka, Redis Pub/Sub
- **Deploy**: Docker daemon, Kubernetes API
- **Automação**: Ansible, Terraform providers

<!-- pause -->

**Basicamente... TUDO que comunica via rede!**


Cliente TCP Simples
===

## 🔧 Conectando a um Servidor

```python +exec
import socket

# Criar socket TCP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectar ao servidor
sock.connect(('httpbin.org', 80))

# Enviar requisição HTTP simples
request = b"GET /ip HTTP/1.1\r\nHost: httpbin.org\r\n\r\n"
sock.send(request)

# Receber resposta
response = sock.recv(4096)
print(response.decode()[:200])  # Primeiros 200 chars

sock.close()
```


Servidor TCP Básico
===

<!-- column_layout: [1, 1] -->
<!-- column: 0 -->

## 🖥️ Criando um Servidor


```python
import socket
import threading

def handle_client(client_socket, address):
    print(f"📥 Conexão de {address}")
    
    # Receber dados
    data = client_socket.recv(1024)
    print(f"Recebido: {data.decode()}")
    
    # Enviar resposta
    response = f"Echo: {data.decode()}"
    client_socket.send(response.encode())
    
    client_socket.close()

# Criar servidor
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 9999))
server.listen(5)
print("🚀 Servidor rodando na porta 9999...")
```
### IMPORTANTE: Este servidor é TCP e BLOQUEANTE não aceita multiplas conexões e não implementa um protocolo de aplicação. 

<!-- column: 1 -->
## 🖳  Python como cliente

```python
>>> from socket import socket
>>> s=socket()
>>> s.connect(('localhost', 9999))
>>> s.send(b'Ola')
3
>>> s.recv(1024).decode()
'Echo: Ola'
```

<!-- pause --> 

Tente mandar um `s.send('Olá')`

<!-- pause --> 

```python
>>> s.send(b'Olá')
  File "<python-input-42>", line 1
    s.send(b'Olá')
           ^^^^^^
SyntaxError: bytes can only contain ASCII literal characters
```

<!-- pause --> 

Solução:

```python
>>> s.send('Olá'.encode('utf-8'))
3
>>> s.recv(1024).decode()
'Echo: Olá'
```
<!-- pause --> 

Cliente (Terminal)
```bash +exec
# Usando netcat
echo "Olá servidor!" | nc localhost 9999
# Ou telnet
telnet localhost 9999
```


Socket UDP Exemplo
===

## 📨 Comunicação Sem Conexão

```python +exec
import socket
import json

# Cliente UDP - Consulta DNS
def dns_query(hostname):
    # Criar socket UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Usar getaddrinfo para resolver
    try:
        result = socket.getaddrinfo(hostname, None)
        ips = [r[4][0] for r in result]
        return list(set(ips))  # IPs únicos
    except:
        return []

# Testar
sites = ['google.com', 'github.com', 'aws.amazon.com']
for site in sites:
    ips = dns_query(site)
    print(f"{site:20} → {', '.join(ips)}")
```


Bibliotecas de Alto Nível
===

## 🚀 Abstrações Pythônicas

### Não reinvente a roda!

<!-- column_layout: [1, 1] -->
<!-- column: 0 -->

**Para HTTP:**
```python
import requests

# Muito mais simples!
r = requests.get('https://api.github.com')
print(r.json())
```

**Para WebSockets:**
```python
import websocket

ws = websocket.WebSocket()
ws.connect("ws://echo.websocket.org")
ws.send("Hello!")
```

<!-- column: 1 -->

**Para Async:**
```python
import asyncio

async def tcp_client():
    reader, writer = await asyncio.open_connection(
        'example.com', 80
    )
    writer.write(b'GET / HTTP/1.0\r\n\r\n')
    data = await reader.read(100)
    writer.close()
```


Exemplo DevOps: Health Check
===

<!-- column_layout: [2, 1] -->
<!-- column: 0 -->


## 🏥 Monitorando Serviços

```python
import socket
import time

def check_service(host, port, timeout=2):
    """Verifica se serviço está respondendo"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    
    try:
        start = time.time()
        result = sock.connect_ex((host, port))
        latency = (time.time() - start) * 1000
        
        if result == 0:
            return True, f"{latency:.0f}ms"
        return False, "Connection refused"
    except socket.timeout:
        return False, "Timeout"
    finally:
        sock.close()

# Monitorar serviços
services = [
    ('google.com', 443, 'HTTPS'),
    ('8.8.8.8', 53, 'DNS'),
    ('github.com', 22, 'SSH')
]

for host, port, name in services:
    ok, msg = check_service(host, port)
    status = "✅" if ok else "❌"
    print(f"{status} {name:8} {host:15}:{port:5} → {msg}")
```

<!-- column: 1 -->

```python +exec
/// import socket
/// import time
/// 
/// def check_service(host, port, timeout=2):
///     """Verifica se serviço está respondendo"""
///     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
///     sock.settimeout(timeout)
/// 
///     try:
///         start = time.time()
///         result = sock.connect_ex((host, port))
///         latency = (time.time() - start) * 1000
/// 
///         if result == 0:
///             return True, f"{latency:.0f}ms"
///         return False, "Connection refused"
///     except socket.timeout:
///         return False, "Timeout"
///     finally:
///         sock.close()
/// 
/// # Monitorar serviços
/// services = [
///     ('google.com', 443, 'HTTPS'),
///     ('8.8.8.8', 53, 'DNS'),
///     ('github.com', 22, 'SSH')
/// ]
/// 
/// for host, port, name in services:
///     ok, msg = check_service(host, port)
///     status = "✅" if ok else "❌"
///     print(f"{status} {name:8} {host:15}:{port:5} → {msg}")
```





Port Scanner Básico
===

## 🔍 Descobrindo Serviços

```python +exec
import socket
from concurrent.futures import ThreadPoolExecutor

def scan_port(host, port):
    """Tenta conectar em uma porta"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)
    result = sock.connect_ex((host, port))
    sock.close()
    return port if result == 0 else None

def scan_host(host, ports):
    """Scan paralelo de portas"""
    open_ports = []
    
    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = [executor.submit(scan_port, host, p) for p in ports]
        for future in futures:
            if port := future.result():
                open_ports.append(port)
    
    return sorted(open_ports)

# Portas comuns em DevOps
common_ports = [22, 80, 443, 3306, 5432, 6379, 8080, 9090]

host = 'scanme.nmap.org'
open_ports = scan_host(host, common_ports)
print(f"Portas abertas em {host}: {open_ports}")
```


Socket Options
===

## ⚙️ Configurações Avançadas

```python
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Reusar endereço (evita "Address already in use")
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Keep-alive para detectar conexões mortas
sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)

# Buffer sizes
sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 8192)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 8192)

# Timeout
sock.settimeout(30.0)

# Non-blocking mode
sock.setblocking(False)
```


Unix Domain Sockets
===

## 🐧 Comunicação Local Eficiente

```python
import socket
import os

# Servidor Unix Socket
server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

# Remove socket antigo se existir
sock_path = '/tmp/my_app.sock'
if os.path.exists(sock_path):
    os.remove(sock_path)

server.bind(sock_path)
server.listen(1)

# Cliente se conecta assim:
client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
client.connect('/tmp/my_app.sock')
```

### Onde são usados?
- Docker daemon: `/var/run/docker.sock`
- PostgreSQL: `/var/run/postgresql/.s.PGSQL.5432`
- SystemD: `/run/systemd/private`


Async Sockets com asyncio
===

## ⚡ Programação Assíncrona

```python
import asyncio

async def handle_client(reader, writer):
    """Handler assíncrono para clientes"""
    addr = writer.get_extra_info('peername')
    print(f"Cliente conectado: {addr}")
    
    while True:
        data = await reader.read(1024)
        if not data:
            break
            
        message = data.decode()
        print(f"Recebido: {message}")
        
        # Echo back
        writer.write(data)
        await writer.drain()
    
    writer.close()
    await writer.wait_closed()

async def main():
    server = await asyncio.start_server(
        handle_client, 'localhost', 8888
    )
    
    async with server:
        await server.serve_forever()

# asyncio.run(main())
```


Exemplo Real: Proxy TCP
===

## 🔄 Redirecionador de Tráfego

```python
import socket
import threading

def proxy_handler(client_sock, remote_host, remote_port):
    """Encaminha dados entre cliente e servidor remoto"""
    # Conectar ao servidor real
    remote_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_sock.connect((remote_host, remote_port))
    
    def forward(source, destination):
        while True:
            data = source.recv(4096)
            if not data:
                break
            destination.send(data)
    
    # Threads para forward bidirecional
    t1 = threading.Thread(target=forward, args=(client_sock, remote_sock))
    t2 = threading.Thread(target=forward, args=(remote_sock, client_sock))
    
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    
    client_sock.close()
    remote_sock.close()

# Uso: proxy local:8080 → google.com:80
```


Debugging Sockets
===

## 🐛 Ferramentas de Diagnóstico

### Comandos Linux Úteis

```bash
# Ver sockets abertos
netstat -tuln
ss -tuln

# Ver processo usando porta
lsof -i :8080
fuser 8080/tcp

# Capturar tráfego
tcpdump -i any port 8080
wireshark

# Testar conectividade
nc -zv host.com 80
telnet host.com 80
```

### Python Debug
```python
import socket
import sys

# Habilitar debug
socket.setdefaulttimeout(5)

# Logger para debug
import logging
logging.basicConfig(level=logging.DEBUG)
```


Segurança em Sockets
===

## 🔐 Boas Práticas

### ⚠️ Cuidados Importantes

- **Sempre** valide dados recebidos
- **Nunca** confie no cliente
- Use **TLS/SSL** para dados sensíveis
- Implemente **rate limiting**
- Configure **timeouts** apropriados
- Limite **tamanho de buffers**

### Exemplo com SSL
```python
import ssl

# Wrap socket com SSL
context = ssl.create_default_context()
secure_sock = context.wrap_socket(
    sock, 
    server_hostname='example.com'
)
```


Performance e Escalabilidade
===

## 📊 Otimizações

<!-- column_layout: [1, 1] -->
<!-- column: 0 -->

### Single Thread
❌ **Bloqueante**
```python
while True:
    client, _ = server.accept()
    handle(client)  # Bloqueia
```

### Multi Thread
✅ **Concorrente**
```python
while True:
    client, _ = server.accept()
    thread = Thread(target=handle, 
                   args=(client,))
    thread.start()
```

<!-- column: 1 -->

### Async I/O
✅ **Eficiente**
```python
async def handle(reader, writer):
    # Non-blocking
    data = await reader.read()
```

### Event Loop
🚀 **Máxima Performance**
```python
# select, epoll, kqueue
import selectors
sel = selectors.DefaultSelector()
```

Recursos e Próximos Passos
===

## 📚 Continue Aprendendo!

### Documentação
- [Python Socket Programming](https://docs.python.org/3/library/socket.html)
- [Real Python - Sockets](https://realpython.com/python-sockets/)

### Bibliotecas Avançadas
- **asyncio**: Programação assíncrona
- **trio**: Async alternativo
- **socketio**: WebSockets + fallbacks
- **ZeroMQ**: Mensageria avançada

### Próxima Aula
**HTTP** - O protocolo da Web
- Como funciona por baixo dos panos
- Construindo clientes e servidores HTTP
- REST APIs com Python


Conclusão
===

## 🎯 O que Aprendemos

<!-- font_size: 1 -->

✅ Sockets são a **base** de toda comunicação em rede

✅ Python torna sockets **acessíveis** e **práticos**

✅ De health checks a proxies - sockets estão **em todo lugar**

✅ Abstrações existem, mas entender sockets é **fundamental**

<!-- pause -->

> "Tudo em DevOps depende de comunicação em rede.
> Sockets são o alicerce dessa comunicação."
> 
> -- Todo SRE experiente
