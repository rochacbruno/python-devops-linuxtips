# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "requests",
# ]
# ///

import base64
import requests

# Basic Auth
credentials = base64.b64encode(b'user:pass').decode()
headers = {'Authorization': f'Basic {credentials}'}

response = requests.get(
    'https://httpbin.org/basic-auth/user/pass',
    headers=headers
)

print("Basic Auth Response:", response.json())

# Bearer Token (JWT)
token = "your_jwt_token_here"
headers = {'Authorization': f'Bearer {token}'}

response = requests.get(
    'https://api.example.com/protected',
    headers=headers
)

# API Key
response = requests.get('https://api.example.com/data?api_key=xyz')
response = requests.get('https://api.example.com/data', 
            headers={'X-API-Key': 'xyz'})