import socket


def handle_client(client_socket, address):
    print(f"📥 Conexão de {address}")

    try:
        while True:
            # Receber dados
            data = client_socket.recv(1024)

            if not data:  # Cliente desconectou
                break

            print(f"Recebido: {data.decode()}")

            # Enviar resposta
            response = f"Echo: {data.decode()}"
            client_socket.send(response.encode())
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        print(f"📤 Desconexão de {address}")
        client_socket.close()


# Criar servidor
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("0.0.0.0", 9999))
server.listen(5)
print("🚀 Servidor rodando na porta 9999...")

# Loop principal do servidor
try:
    while True:
        client_socket, address = server.accept()
        handle_client(client_socket, address)
except KeyboardInterrupt:
    print("\n⛔ Servidor encerrado")
finally:
    server.close()
