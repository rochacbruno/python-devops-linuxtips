# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "requests",
# ]
# ///

import requests

# Upload simples
with open('config.yaml', 'rb') as f:
    files = {'file': f}
    response = requests.post(
        'https://httpbin.org/post',
        files=files
    )

# Upload com metadata
files = {
    'file': ('config.yaml', open('config.yaml', 'rb'), 'text/yaml'),
    'field': (None, 'value')  # Campo adicional
}

data = {
    'description': 'Configuration file',
    'version': '1.0'
}

response = requests.post(
    'https://httpbin.org/post',
    files=files,
    data=data
)