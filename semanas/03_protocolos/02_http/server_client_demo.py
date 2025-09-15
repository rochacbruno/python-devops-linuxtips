# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "requests",
# ]
# ///

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import threading
import time
import requests

class APIHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
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
time.sleep(2)
print()
# cliente
r = requests.get('http://localhost:8000/health')
print("Resposta:", r.json())