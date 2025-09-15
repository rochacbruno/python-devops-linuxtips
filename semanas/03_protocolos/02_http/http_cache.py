# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "requests-cache",
# ]
# ///

import requests_cache  # pip install requests-cache

# Criar sessão com cache
session = requests_cache.CachedSession(
    'cache_demo',
    expire_after=300,  # 5 minutos
    allowable_codes=[200, 301],
    allowable_methods=['GET', 'POST']
)

# Primeira requisição - vai para o servidor
response = session.get('https://api.github.com/users/torvalds')
print(f"From cache: {response.from_cache}")  # False

# Segunda requisição - vem do cache
response = session.get('https://api.github.com/users/torvalds')
print(f"From cache: {response.from_cache}")  # True

# Headers de cache
cache_headers = {
    'Cache-Control': 'max-age=3600',
    'ETag': '"123456"',
    'Last-Modified': 'Wed, 21 Oct 2023 07:28:00 GMT'
}