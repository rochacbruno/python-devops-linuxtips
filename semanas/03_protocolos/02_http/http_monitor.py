# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "requests",
# ]
# ///

import requests
import time
from datetime import datetime

def health_check(services):
    """Monitora status de serviços HTTP"""
    results = []
    
    for name, url in services.items():
        try:
            start = time.time()
            response = requests.get(url, timeout=5)
            latency = (time.time() - start) * 1000
            
            results.append({
                'service': name,
                'status': response.status_code,
                'latency_ms': round(latency),
                'healthy': 200 <= response.status_code < 300
            })
        except Exception as e:
            results.append({
                'service': name,
                'status': 0,
                'error': str(e),
                'healthy': False
            })
    
    return results

# Monitorar serviços
services = {
    'GitHub': 'https://api.github.com',
    'Google': 'https://www.google.com',
    'HTTPBin': 'https://httpbin.org/status/200'
}

results = health_check(services)
for r in results:
    status = "✅" if r['healthy'] else "❌"
    print(f"{status} {r['service']:10} - {r.get('latency_ms', 'N/A'):4}ms")