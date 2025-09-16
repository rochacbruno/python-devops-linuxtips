import getpass
import hashlib
import secrets

# Ocultar entrada de senha
# password = getpass.getpass("Digite a senha: ")
password = "senha123"  # Para demonstração

# Hash seguro com salt
salt = secrets.token_bytes(32)
hashed = hashlib.pbkdf2_hmac(
    'sha256',
    password.encode('utf-8'),
    salt,
    100000 # 100k iterações
)
print(f"Hash: {hashed.hex()}")