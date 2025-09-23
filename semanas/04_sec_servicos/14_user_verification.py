import time
import hashlib

def verify_user(email: str, password: str) -> bool:
    """Verifica sem expor se usuário existe"""
    # Sempre fazer hash mesmo se usuário não existir
    hashed = hashlib.sha256(password.encode()).hexdigest()

    # Simular delay consistente
    time.sleep(0.1)
    user = db_get_user_by_email(email)  # Função fictícia
    if user and user['password_hash'] == hashed:
        return True  # "Login bem-sucedido"

    # Mensagem genérica
    return False  # "Credenciais inválidas"