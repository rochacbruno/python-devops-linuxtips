# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "requests",
# ]
# ///

import requests

# Usando proxy
proxies = {
    'http': 'http://proxy.company.com:8080',
    'https': 'https://proxy.company.com:8080'
}

response = requests.get(
    'https://api.example.com',
    proxies=proxies
)

# Túnel SSH (port forwarding)
# ssh -L 8080:remote-api.com:80 user@jumphost
# Depois use: http://localhost:8080