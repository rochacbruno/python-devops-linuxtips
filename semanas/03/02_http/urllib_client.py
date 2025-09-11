import urllib.request
import json

# GET simples
with urllib.request.urlopen('https://api.github.com/users/torvalds') as response:
    data = json.loads(response.read())
    print(f"Nome: {data['name']}")
    print(f"Empresa: {data['company']}")
    print(f"Repos públicos: {data['public_repos']}")
    print(f"Seguidores: {data['followers']}")

# POST com dados
import urllib.parse

data = urllib.parse.urlencode({'key': 'value'}).encode()
req = urllib.request.Request(
    'https://httpbin.org/post',
    data=data,
    method='POST'
)
print("\nPOST Response:")
with urllib.request.urlopen(req) as response:
     print(response.read())