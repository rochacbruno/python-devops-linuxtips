import sys
import uuid
import traceback

def safe_error_handler(exc_type, exc_value, exc_traceback):
    """Handler que não expõe informações sensíveis"""
    if exc_type == KeyboardInterrupt:
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    # Log completo para desenvolvimento
    with open('errors.log', 'a') as f:
        traceback.print_exception(exc_type, exc_value, exc_traceback, file=f)

    # Mensagem genérica para usuário
    print("Ocorreu um erro. Por favor, contate o suporte.")
    print(f"ID do erro: {uuid.uuid4()}")

# Configurar handler customizado
sys.excepthook = safe_error_handler

# Teste
password = "senha123"
raise ValueError(f"Senha inválida: {password}")