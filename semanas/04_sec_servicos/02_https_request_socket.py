import ssl
import socket
import pprint

context = ssl.create_default_context()
context.check_hostname = True
context.verify_mode = ssl.CERT_REQUIRED

# Conectar com HTTPS
sock = socket.create_connection(('httpbin.org', 443))
ssock = context.wrap_socket(sock, server_hostname='httpbin.org')

# Fazer requisição HTTPS
request = (
  "GET /get HTTP/1.1\r\nHost: httpbin.org\r\nConnection: close\r\n\r\n"
)
ssock.sendall(request.encode())
response = b""
while True:
    data = ssock.recv(4096)
    if not data:
        break
    response += data
headers, body = response.split(b"\r\n\r\n", 1)
print("Headers:")
pprint.pprint(headers.decode().split("\r\n"))
print("\nBody:")
pprint.pprint(body.decode()[:200] + "...")