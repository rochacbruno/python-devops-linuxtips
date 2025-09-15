import socket

# Criar socket TCP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectar ao servidor
sock.connect(("httpbingo.org", 80))

# Enviar requisição HTTP simples
request = b"GET /ip HTTP/1.1\r\nHost: httpbin.org\r\n\r\n"
sock.send(request)

# Receber resposta
response = sock.recv(4096)
print(response.decode()[:200])  # Primeiros 200 chars

sock.close()
