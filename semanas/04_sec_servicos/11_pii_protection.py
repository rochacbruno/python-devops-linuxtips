import uuid
import json
from cryptography.fernet import Fernet

# Gerar chave de criptografia
key = Fernet.generate_key()
print(f"Chave de criptografia (guarde com segurança!): {key.decode()}")

cipher = Fernet(key)

# Usar UUIDs ao invés de IDs sequenciais
user_data = {
    'id': str(uuid.uuid4()),
    'email': 'user@example.com',
    'cpf': '123.456.789-00'
}

encrypted = cipher.encrypt(json.dumps(user_data).encode())
print(f"Dados criptografados: {encrypted[:100].decode('utf-8')}...")
print()
# Estes dados agora podem ser armazenados em arquivos ou
# bancos de dados com segurança.

# ----------------------------------------------

print("Descriptografando dados...")
decrypted = json.loads(cipher.decrypt(encrypted))
print(f"ID do usuário: {decrypted['id']}")
print(f"Email do usuário: {decrypted['email']}")
print(f"CPF do usuário: {decrypted['cpf']}")