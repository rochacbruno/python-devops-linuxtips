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