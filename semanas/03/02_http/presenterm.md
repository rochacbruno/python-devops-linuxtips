---
title: HTTP em Python
sub_title: O protocolo da Web
author: Bruno Rocha - LINUXtips
options:
  implicit_slide_ends: true
  end_slide_shorthand: true
  incremental_lists: true
---

HTTP
===

<!-- alignment: center -->

<!-- font_size: 2 -->
# 🌐 HTTP

HyperText Transfer Protocol

<!-- pause --> 

O que é HTTP?
===

<!-- font_size: 2 -->
<!-- alignment: center -->

## 📡 Protocolo de Aplicação

- **H**yper**T**ext **T**ransfer **P**rotocol
- Protocolo cliente-servidor sobre TCP/IP
- Base de toda comunicação na Web
- Stateless - cada requisição é independente

<!-- pause -->

### Camadas
```
[Aplicação]  → HTTP/HTTPS
[Transporte] → TCP
[Rede]       → IP
[Física]     → Ethernet/WiFi
```


Qual Problema Resolve?
===

<!-- font_size: 2 -->
<!-- alignment: center -->

## 🎯 Comunicação Padronizada na Web

### Problemas que HTTP resolve:

- **Transferência** de recursos (HTML, JSON, imagens...)
- **Padronização** de comunicação cliente-servidor
- **Identificação** de recursos via URLs
- **Negociação** de conteúdo e formato
- **Autenticação** e autorização
- **Cache** e otimização

<!-- pause -->


<!-- font_size: 2 -->
> Sem HTTP, cada site precisaria de seu próprio protocolo!


Anatomia de uma Requisição
===

<!-- font_size: 2 -->
<!-- alignment: center -->

## 📋 Request HTTP

```yaml
GET /api/users/123 HTTP/1.1
Host: api.example.com
User-Agent: Python/3.11
Accept: application/json
Authorization: Bearer token123
```

### Componentes:
- **Método**: GET, POST, PUT, DELETE, PATCH...
- **Host**: api.example.com
- **Path**: /api/users/123
- **Versão**: HTTP/1.1, HTTP/2, HTTP/3
- **Headers**: Metadados da requisição
- **Body**: Dados (em POST, PUT, PATCH)


Anatomia de uma Resposta
===
<!-- font_size: 2 -->
<!-- alignment: center -->

## 📨 Response HTTP

```yaml
HTTP/1.1 200 OK
Content-Type: application/json
Content-Length: 58
Cache-Control: max-age=3600

{"id": 123, "name": "João", "role": "DevOps"}
```

### Componentes:
- **Versão**: HTTP/1.1, HTTP/2, HTTP/3
- **Status Code**: 200, 404, 500...
- **Status Text**: OK, Not Found, Internal Server Error
- **Headers**: Metadados da resposta
- **Body**: Conteúdo retornado


<!-- end_slide -->

<!-- jump_to_middle -->
<!-- font_size: 6 -->
<!-- alignment: center -->
# É apenas texto!


Métodos HTTP
===

<!-- font_size: 2 -->
<!-- alignment: center -->

## 🔧 Verbos e Seus Usos

| Método | Descrição | Uso Comum | Idempotente |
|--------|-----------|-----------|-------------|
| **GET** | Buscar dados | Listar, visualizar | ✅ |
| **POST** | Criar recurso | Criar novo registro | ❌ |
| **PUT** | Atualizar completo | Substituir recurso | ✅ |
| **PATCH** | Atualizar parcial | Modificar campos | ❌ |
| **DELETE*** | Remover | Deletar recurso | ✅ |
| **HEAD** | Só headers | Verificar existência | ✅ |
| **OPTIONS** | Métodos permitidos | CORS preflight | ✅ |

<!-- alignment: center -->

\* Idempotente: mesmo resultado se repetido várias vezes 
  
\* O método DELETE pode ser considerado idempotente,   
pois deletar um recurso inexistente não causa erro,   
mas retorna 204 No Content, porém nem sempre é implementado assim.


Status Codes
===

<!-- font_size: 2 -->
<!-- alignment: center -->

## 📊 Códigos de Resposta

| Código | Status | Descrição | Uso Comum |
|--------|--------|-----------|----------|
| **1xx** | **Informacional** | | |
| 100 | Continue | Continuar requisição | Upload grande |
| 101 | Switching Protocols | Mudança de protocolo | WebSocket upgrade |
| **2xx** | **Sucesso** | | |
| 200 | OK | Requisição bem-sucedida | GET bem-sucedido |
| 201 | Created | Recurso criado | POST bem-sucedido |
| 204 | No Content | Sem conteúdo | DELETE bem-sucedido |
| **3xx** | **Redirecionamento** | | |
| 301 | Moved Permanently | Mudança permanente | URL antiga → nova |
| 302 | Found | Redirecionamento temporário | Login redirect |
| 304 | Not Modified | Usar cache | Cache válido |
| **4xx** | **Erro do Cliente** | | |
| 400 | Bad Request | Requisição inválida | Dados mal formatados |
| 401 | Unauthorized | Não autenticado | Token inválido |
| 403 | Forbidden | Sem permissão | Acesso negado |
| 404 | Not Found | Recurso não existe | URL incorreta |
| 429 | Too Many Requests | Rate limit | Limite excedido |
| **5xx** | **Erro do Servidor** | | |
| 500 | Internal Server Error | Erro genérico | Bug no servidor |
| 502 | Bad Gateway | Proxy error | Backend offline |
| 503 | Service Unavailable | Serviço indisponível | Manutenção |


Cliente HTTP com urllib
===

## 🐍 Biblioteca Padrão Python

<!-- column_layout: [1, 1] -->

<!-- column: 0 -->

```python
import urllib.request
import json

# GET simples
with urllib.request.urlopen('https://api.github.com/users/torvalds') as response:
    data = json.loads(response.read())
    print(f"Nome: {data['name']}")
    print(f"Empresa: {data['company']}")
    print(f"Repos públicos: {data['public_repos']}")
    print(f"Seguidores: {data['followers']}")

# POST com dados
import urllib.parse

data = urllib.parse.urlencode({'key': 'value'}).encode()
req = urllib.request.Request(
    'https://httpbin.org/post',
    data=data,
    method='POST'
)
print("\nPOST Response:")
with urllib.request.urlopen(req) as response:
     print(response.read())
```
<!-- column: 1 -->


```python +exec
/// import urllib.request
/// import json
/// 
/// # GET simples
/// with urllib.request.urlopen('https://api.github.com/users/torvalds') as response:
///     data = json.loads(response.read())
///     print(f"Nome: {data['name']}")
///     print(f"Empresa: {data['company']}")
///     print(f"Repos públicos: {data['public_repos']}")
///     print(f"Seguidores: {data['followers']}")
/// 
/// # POST com dados
/// import urllib.parse
/// 
/// data = urllib.parse.urlencode({'key': 'value'}).encode()
/// req = urllib.request.Request(
///     'https://httpbingo.org/post',
///     data=data,
///     method='POST'
/// )
/// print("\nPOST Response:")
/// with urllib.request.urlopen(req) as response:
///      print(response.read())
# uv run http_client.py
```



Cliente HTTP com requests
===

<!-- alignment: center -->

## 🚀 A Biblioteca Mais Popular

```python +exec
# pip install requests
import requests

# GET com parâmetros
response = requests.get(
    'https://api.github.com/search/repositories',
    params={'q': 'language:python stars:>10000', 'sort': 'stars'},
    headers={'Accept': 'application/vnd.github.v3+json'}
)

data = response.json()
print(f"Total de repositórios: {data['total_count']}\n")

# Top 3 repos Python
for repo in data['items'][:3]:
    print(f"⭐ {repo['stargazers_count']:,} - {repo['full_name']}")
    print(f"   {repo['description'][:60]}...")
```


Servidor HTTP Simples
===

## 🖥️ Servidor Básico

<!-- column_layout: [1, 1] -->

<!-- column: 0 -->

```python
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import threading
import time

class APIHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.send_header(
                'Content-Type', 'application/json'
            )
            self.end_headers()
            response = {
                'status': 'healthy',
                'timestamp': time.time(),
                'service': 'api-demo'
            }
            time.sleep(3)  # Simular latência
            self.wfile.write(json.dumps(response).encode())

# Rodar em thread para não bloquear
def run_server():
    server = HTTPServer(('localhost', 8000), APIHandler)
    print("Rodando em http://localhost:8000/health")
    server.timeout = 10  # Timeout para shutdown
    server.handle_request()

thread = threading.Thread(target=run_server, daemon=True)
thread.start()
```
<!-- column: 1 -->


```python +exec
/// from http.server import HTTPServer, BaseHTTPRequestHandler
/// import json
/// import threading
/// import time
/// import requests
/// 
/// class APIHandler(BaseHTTPRequestHandler):
///     def do_GET(self):
///         if self.path == '/health':
///             self.send_response(200)
///             self.send_header('Content-Type', 'application/json')
///             self.end_headers()
///             response = {
///                 'status': 'healthy',
///                 'timestamp': time.time(),
///                 'service': 'api-demo'
///             }
///             time.sleep(3)  # Simular latência
///             self.wfile.write(json.dumps(response).encode())
/// 
/// # Rodar em thread para não bloquear
/// def run_server():
///     server = HTTPServer(('localhost', 8000), APIHandler)
///     print("Rodando em http://localhost:8000/health")
///     server.timeout = 10  # Timeout para shutdown
///     server.handle_request()
/// 
/// thread = threading.Thread(target=run_server, daemon=True)
/// thread.start()
/// time.sleep(2)
/// print()
# cliente
r = requests.get('http://localhost:8000/health')
print("Resposta:", r.json())
```

REST API Exemplo
===
<!-- alignment: center -->
## 🔄 CRUD Completo

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List

app = FastAPI()

class User(BaseModel):
    name: str
    email: str
    role: str = "user"

class UserResponse(User):
    id: int

users: Dict[int, UserResponse] = {}  # DATABASE SIMULADA

@app.get("/users", response_model=List[UserResponse])
async def get_users():
    return list(users.values())

@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    return users[user_id]

@app.post("/users", response_model=UserResponse, status_code=201)
async def create_user(user: User):
    user_response = UserResponse(id=next_id, **user.dict())
    users[next_id] = user_response
    next_id += 1
    return user_response

@app.delete("/users/{user_id}", status_code=204)
async def delete_user(user_id: int):
    users.pop(user_id, None)
    return None
```


Autenticação HTTP
===

<!-- alignment: center -->
<!-- pause --> 
### Basic Auth
```python
import base64

# Cliente
credentials = base64.b64encode(b'user:pass').decode()
headers = {'Authorization': f'Basic {credentials}'}

response = requests.get(
    'https://httpbin.org/basic-auth/user/pass',
    headers=headers
)
```

<!-- pause --> 

### Bearer Token (JWT)
```python
# Cliente
headers = {'Authorization': f'Bearer {token}'}

response = requests.get(
    'https://api.example.com/protected',
    headers=headers
)
```

<!-- pause --> 

### API Key
```python
# Query param ou Header
requests.get('https://api.example.com/data?api_key=xyz')
requests.get('https://api.example.com/data', 
            headers={'X-API-Key': 'xyz'})
```


Sessões e Cookies
===

## 🍪 Mantendo Estado

```python +exec
import requests

# Criar sessão para manter cookies
session = requests.Session()

# Setar cookies via GET (httpbin permite isso)
session.get('https://httpbingo.org/cookies/set?sessionid=abc123&user=admin')

# Requisições subsequentes enviam cookie automaticamente
response = session.get('https://httpbingo.org/cookies')
print("Cookies na sessão:", response.json())

# Adicionar cookie manualmente
session.cookies.set('custom_cookie', 'my_value')

# Verificar todos os cookies
print("\nCookies armazenados:")
for cookie in session.cookies:
    print(f"  {cookie.name} = {cookie.value}")

# Fechar sessão
session.close()
```


Upload de Arquivos
===

## 📤 Multipart Form Data

```python
import requests

# Upload simples
with open('config.yaml', 'rb') as f:
    files = {'file': f}
    response = requests.post(
        'https://httpbin.org/post',
        files=files
    )

# Upload com metadata
files = {
    'file': ('config.yaml', open('config.yaml', 'rb'), 'text/yaml'),
    'field': (None, 'value')  # Campo adicional
}

data = {
    'description': 'Configuration file',
    'version': '1.0'
}

response = requests.post(
    'https://httpbin.org/post',
    files=files,
    data=data
)
```


Streaming Responses
===

## 📺 Download Eficiente

```python
import requests

# Download grande sem carregar tudo na memória
def download_file(url, filename):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        
        total_size = int(r.headers.get('content-length', 0))
        downloaded = 0
        
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
                downloaded += len(chunk)
                
                # Progress
                percent = (downloaded / total_size) * 100
                print(f'\rDownload: {percent:.1f}%', end='')

# Server-Sent Events (SSE)
response = requests.get('https://example.com/events', stream=True)
for line in response.iter_lines():
    if line:
        print(f"Event: {line.decode()}")
```


Async HTTP com aiohttp
===

## ⚡ Requisições Assíncronas

<!-- column_layout: [1, 1] -->
<!-- column: 0 -->

```python +exec:uv +id:async_http
# /// script
# dependencies = ["aiohttp"]
# ///
import asyncio
import aiohttp 

async def fetch_user(session, user_id):
    url = (
            'https://jsonplaceholder.typicode.com/users/'
            f'{user_id}'
    )
    async with session.get(url) as response:
        await asyncio.sleep(1)  # Simular latência
        print(f"Fetched user {user_id}")
        return await response.json()

async def fetch_all_users():
    async with aiohttp.ClientSession() as session:
        # Buscar 10 usuários em paralelo
        tasks = [
            fetch_user(session, i) 
            for i in range(1, 11)
        ]
        users = await asyncio.gather(*tasks) 
        print("\nUsuários:")
        for user in users:
            print(f"- {user['name']} ({user['email']})")

asyncio.run(fetch_all_users())
```
<!-- column: 1 -->

<!-- snippet_output: async_http -->

<!-- pause --> 

### Vantagem
✅ 10 requisições paralelas vs sequenciais
⚡ 10x mais rápido para I/O intensivo


HTTP/2 e HTTP/3
===

## 🚀 Evolução do Protocolo

<!-- font_size: 2 -->

<!-- column_layout: [1, 1, 1] -->
<!-- column: 0 -->

### HTTP/1.1
**Protocolo original (1997)**

- ✅ Simples e confiável
- ❌ Uma requisição por vez
- ❌ Múltiplas conexões TCP
- ❌ Headers em texto
- ❌ Head-of-line blocking

**Uso:** ~30% da web

<!-- column: 1 -->

### HTTP/2
**Multiplexação (2015)**

- ✅ Múltiplas req/conexão
- ✅ Server push
- ✅ Headers comprimidos (HPACK)
- ✅ Protocolo binário
- ❌ Ainda usa TCP

**Uso:** ~65% da web

<!-- column: 2 -->

### HTTP/3
**QUIC Protocol (2022)**

- ✅ Sobre UDP (não TCP!)
- ✅ 0-RTT connection
- ✅ Menor latência
- ✅ Melhor em redes instáveis
- ✅ Criptografia obrigatória

**Uso:** ~25% e crescendo

---

### Exemplo Prático

```python +exec:uv 
# /// script
# dependencies = ["httpx[http2]"]
# ///
# httpx suporta HTTP/2 e HTTP/3
import httpx
import asyncio

# HTTP/2
async def main():
    async with httpx.AsyncClient(http2=True) as client:
        response = await client.get('https://http2.pro/api/v1')
        print(f"Versão: {response.http_version}")
    
asyncio.run(main())

# Comparação de performance
# HTTP/1.1: 100 requests = ~10s
# HTTP/2:   100 requests = ~3s  
# HTTP/3:   100 requests = ~2s
```


Proxy e Túnel
===

## 🔀 Roteamento de Requisições

```python
import requests

# Usando proxy
proxies = {
    'http': 'http://proxy.company.com:8080',
    'https': 'https://proxy.company.com:8080'
}

response = requests.get(
    'https://api.example.com',
    proxies=proxies
)

# Túnel SSH (port forwarding)
# ssh -L 8080:remote-api.com:80 user@jumphost
# Depois use: http://localhost:8080
```


Rate Limiting e Retry
===

## 🔄 Resiliência

```python
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Configurar retry strategy
session = requests.Session()
retry = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[500, 502, 503, 504]
)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

# Rate limiting manual
class RateLimiter:
    def __init__(self, max_per_second=10):
        self.max_per_second = max_per_second
        self.min_interval = 1.0 / max_per_second
        self.last_request = 0
    
    def wait(self):
        elapsed = time.time() - self.last_request
        if elapsed < self.min_interval:
            time.sleep(self.min_interval - elapsed)
        self.last_request = time.time()

limiter = RateLimiter(max_per_second=5)
for i in range(10):
    limiter.wait()
    print(f"Request {i+1}")
```


Cache HTTP
===

## 💾 Otimização com Cache

```python
import requests_cache  # pip install requests-cache

# Criar sessão com cache
session = requests_cache.CachedSession(
    'cache_demo',
    expire_after=300,  # 5 minutos
    allowable_codes=[200, 301],
    allowable_methods=['GET', 'POST']
)

# Primeira requisição - vai para o servidor
response = session.get('https://api.github.com/users/torvalds')
print(f"From cache: {response.from_cache}")  # False

# Segunda requisição - vem do cache
response = session.get('https://api.github.com/users/torvalds')
print(f"From cache: {response.from_cache}")  # True

# Headers de cache
cache_headers = {
    'Cache-Control': 'max-age=3600',
    'ETag': '"123456"',
    'Last-Modified': 'Wed, 21 Oct 2023 07:28:00 GMT'
}
```

Monitoramento HTTP
===

## 📈 Health Checks e Métricas

<!-- column_layout: [1, 1] -->

<!-- column: 0 -->

```python +exec +id:http_monitor
import requests
import time
from datetime import datetime

def health_check(services):
    """Monitora status de serviços HTTP"""
    results = []
    
    for name, url in services.items():
        try:
            start = time.time()
            response = requests.get(url, timeout=5)
            latency = (time.time() - start) * 1000
            
            results.append({
                'service': name,
                'status': response.status_code,
                'latency_ms': round(latency),
                'healthy': 200 <= response.status_code < 300
            })
        except Exception as e:
            results.append({
                'service': name,
                'status': 0,
                'error': str(e),
                'healthy': False
            })
    
    return results

# Monitorar serviços
services = {
    'GitHub': 'https://api.github.com',
    'Google': 'https://www.google.com',
    'HTTPBin': 'https://httpbin.org/status/200'
}

results = health_check(services)
for r in results:
    status = "✅" if r['healthy'] else "❌"
    print(f"{status} {r['service']:10} - {r.get('latency_ms', 'N/A'):4}ms")
```

<!-- column: 1 -->
<!-- snippet_output: http_monitor -->

Ferramentas CLI
===

## 🛠️ Debug e Teste

### curl - Swiss Army Knife
```bash
# GET com headers
curl -H "Accept: application/json" https://api.github.com

# POST com dados
curl -X POST -d '{"name":"test"}' -H "Content-Type: application/json" \
     https://httpbin.org/post

# Download com progresso
curl -L -O --progress-bar https://example.com/file.zip
```

### httpie - Human Friendly
```bash
# GET simples
http https://api.github.com/users/torvalds

# POST com JSON
http POST httpbin.org/post name=test type=demo

# Custom headers
http GET httpbin.org/headers Authorization:"Bearer token"
```


Recursos e Próximos Passos
===

<!-- font_size: 2 -->
## 📚 Continue Aprendendo!

### Documentação
- [MDN Web Docs - HTTP](https://developer.mozilla.org/pt-BR/docs/Web/HTTP)
- [Requests Documentation](https://requests.readthedocs.io/)
- [HTTPX - HTTP/2 Client](https://www.python-httpx.org/)

### Frameworks Web
- **FastAPI**: APIs modernas e rápidas
- **Flask**: Simplicidade e flexibilidade
- **Django REST**: Full-featured
- **aiohttp**: Async server/client

### Próxima Aula
**RPC e gRPC** - Chamadas de Procedimento Remoto
- Alternativas ao REST
- Protocol Buffers
- Streaming bidirecional


Conclusão
===
<!-- font_size: 3 -->

## 🎯 O que Aprendemos


✅ HTTP é o **protocolo universal** da web

✅ Python tem **excelentes bibliotecas** para HTTP

✅ De APIs REST a webhooks - HTTP está **onipresente**

✅ Entender HTTP é **essencial** para DevOps moderno

