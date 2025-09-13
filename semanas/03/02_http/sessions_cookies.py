# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "requests",
# ]
# ///

import requests

# Criar sessão para manter cookies
session = requests.Session()

# Setar cookies via GET (httpbin permite isso)
session.get('https://httpbingo.org/cookies/set?sessionid=abc123&user=admin')

# Requisições subsequentes enviam cookie automaticamente
response = session.get('https://httpbingo.org/cookies')
print("Cookies na sessão:", response.json())

# Adicionar cookie manualmente
session.cookies.set('custom_cookie', 'my_value')

# Verificar todos os cookies
print("\nCookies armazenados:")
for cookie in session.cookies:
    print(f"  {cookie.name} = {cookie.value}")

# Fechar sessão
session.close()