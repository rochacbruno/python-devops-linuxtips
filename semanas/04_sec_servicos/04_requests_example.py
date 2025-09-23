import requests

# requests usa verificação de certificados por padrão
response = requests.get('https://httpbin.org/get')
print(f"Status: {response.status_code}")
print("Headers:")
for k, v in response.headers.items():
    print(f"  {k}: {v}")
print("\nBody:")
print(response.text[:200] + "...")