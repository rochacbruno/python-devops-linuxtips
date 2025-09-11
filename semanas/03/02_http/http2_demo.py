# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "httpx[http2]",
# ]
# ///

# httpx suporta HTTP/2 e HTTP/3
import httpx
import asyncio

# HTTP/2
async def main():
    async with httpx.AsyncClient(http2=True) as client:
        response = await client.get('https://http2.pro/api/v1')
        print(f"Versão: {response.http_version}")
    
asyncio.run(main())

# Comparação de performance
# HTTP/1.1: 100 requests = ~10s
# HTTP/2:   100 requests = ~3s  
# HTTP/3:   100 requests = ~2s