# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "requests",
#     "urllib3",
# ]
# ///

import time
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Configurar retry strategy
session = requests.Session()
retry = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[500, 502, 503, 504]
)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

# Rate limiting manual
class RateLimiter:
    def __init__(self, max_per_second=10):
        self.max_per_second = max_per_second
        self.min_interval = 1.0 / max_per_second
        self.last_request = 0
    
    def wait(self):
        elapsed = time.time() - self.last_request
        if elapsed < self.min_interval:
            time.sleep(self.min_interval - elapsed)
        self.last_request = time.time()

limiter = RateLimiter(max_per_second=5)
for i in range(10):
    limiter.wait()
    print(f"Request {i+1}")