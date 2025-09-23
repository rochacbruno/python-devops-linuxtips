import ssl
from http.server import HTTPServer, SimpleHTTPRequestHandler

server = HTTPServer(('localhost', 4443), SimpleHTTPRequestHandler)
server.socket = ssl.wrap_socket(
    server.socket,
    certfile='./cert.pem',
    keyfile='./key.pem',
    server_side=True
)
server.serve_forever()