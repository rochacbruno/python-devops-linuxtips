import subprocess

class Secret(str):
    def __init__(self, value: str):
        self._value = value

    @property
    def safe(self):
        return  f"{self._value[:2]}****"

    def __repr__(self):
        return f"<Secret {self.safe}>"

    def decode(self) -> str:
        return self._value


def get_1password_secret(item: str, field: str) -> Secret:
    """Recupera segredo do 1Password CLI"""
    result = subprocess.run(
        ['op', 'read', f'item/{item}/field/{field}'],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        raise Exception("Erro ao recuperar segredo")
    return Secret(result.stdout.strip())

# Exemplo de uso
db_password = get_1password_secret('MyDatabase', 'password')
print(db_password)  # Faz decode do valor real
print(f"Senha do DB: {db_password.safe}")  # Não expõe valor real
# exemplo de uso em repr
print(f"Objeto secreto: {db_password!r}")