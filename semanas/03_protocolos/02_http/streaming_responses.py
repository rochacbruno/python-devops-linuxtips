# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "requests",
# ]
# ///

import requests

# Download grande sem carregar tudo na memória
def download_file(url, filename):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        
        total_size = int(r.headers.get('content-length', 0))
        downloaded = 0
        
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
                downloaded += len(chunk)
                
                # Progress
                percent = (downloaded / total_size) * 100
                print(f'\rDownload: {percent:.1f}%', end='')

# Server-Sent Events (SSE)
response = requests.get('https://example.com/events', stream=True)
for line in response.iter_lines():
    if line:
        print(f"Event: {line.decode()}")