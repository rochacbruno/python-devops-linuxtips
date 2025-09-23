import ssl
import certifi
import urllib.request
import pprint

# Usar certificados confiáveis
context = ssl.create_default_context(cafile=certifi.where())

# Fazer requisição HTTPS
with urllib.request.urlopen('https://httpbin.org/get', context=context) as response:
    print(f"Status: {response.status}")
    print("Headers:")
    pprint.pprint(response.getheaders())
    print("\nBody:")
    pprint.pprint(response.read().decode()[:200] + "...")