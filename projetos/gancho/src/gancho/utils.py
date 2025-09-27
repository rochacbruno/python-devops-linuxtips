import ipaddress
import os

from fastapi import HTTPException, Request, status
from httpx import AsyncClient

GITHUB_IPS_ONLY = os.getenv("GITHUB_IPS_ONLY", "false").lower() in ["true", "1"]


async def gate_by_github_ip(request: Request):
    # Allow GitHub IPs only

    if GITHUB_IPS_ONLY:
        try:
            src_ip = ipaddress.ip_address(request.client.host)
        except ValueError:
            raise HTTPException(
                status.HTTP_400_BAD_REQUEST, "Could not hook sender ip address"
            )
        async with AsyncClient() as client:
            allowlist = await client.get("https://api.github.com/meta")

        for valid_ip in allowlist.json()["hooks"]:
            if src_ip in ipaddress.ip_network(valid_ip):
                return
        else:
            raise HTTPException(
                status.HTTP_403_FORBIDDEN, "Not a GitHub hooks ip address"
            )
