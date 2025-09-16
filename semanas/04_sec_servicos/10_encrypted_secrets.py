import os
import logging
from cryptography.fernet import Fernet, InvalidToken

logging.basicConfig(level=logging.INFO)

class Secret(str):
    def __init__(self, value: str):
        self._value = value
    @property
    def safe(self):
        return  f"{self._value[:3]}****"
    def __repr__(self):
        return f"<Secret {self.safe}>"
    def decode(self) -> str:
        return self._value

def load_secret(secret_file: str, secret_key: str) -> Secret:
    """Lê e descriptografa o conteúdo do arquivo de segredo"""
    try:
        with open(secret_file, 'rb') as f:
            encrypted_data = f.read()
        fernet = Fernet(secret_key)
        decrypted_data = fernet.decrypt(encrypted_data)
        return Secret(decrypted_data.decode('utf-8'))
    except FileNotFoundError:
        logging.error(f"Arquivo de segredo não encontrado: {secret_file}")
        raise
    except InvalidToken:
        logging.error("Chave de segredo inválida ou dados corrompidos")
        raise
    except Exception as e:
        logging.error(f"Erro ao carregar segredo: {e}")
        raise

# Exemplo de uso
# Key must be 32 url-safe base64-encoded bytes
os.environ['SECRET_KEY'] = Fernet.generate_key().decode()
secret_key = os.getenv('SECRET_KEY')

# Simular criação do arquivo de segredo
with open('/tmp/db_password', 'wb') as f:
    fernet = Fernet(secret_key)
    encrypted = fernet.encrypt(b'supersecretpassword')
    f.write(encrypted)

# Carregar segredo
secret_file = '/tmp/db_password'  # Ajuste conforme necessário
if not secret_key:
    raise Exception("Variável de ambiente SECRET_KEY não definida")
try:
    db_password = load_secret(secret_file, secret_key)
    logging.info("Senha do banco carregada com sucesso")
    # Use db_password com segurança
    print(f"DB PASSWORD: {db_password.safe}")
except Exception:
    logging.error("Falha ao carregar a senha do banco")