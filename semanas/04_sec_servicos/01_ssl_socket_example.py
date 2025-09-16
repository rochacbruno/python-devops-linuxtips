import ssl
import socket

# Criar contexto SSL seguro
context = ssl.create_default_context()
context.check_hostname = True
context.verify_mode = ssl.CERT_REQUIRED  # OPTIONS: ssl.CERT_NONE, ssl.CERT_OPTIONAL

# Conectar com HTTPS
with socket.create_connection(('httpbin.org', 443)) as sock:
    with context.wrap_socket(sock, server_hostname='httpbin.org') as ssock:
        print(f"Cifra: {ssock.cipher()}")
        print(f"Versão SSL: {ssock.version()}")