import socket


# Cliente UDP - Consulta DNS
def dns_query(hostname):
    # Usar getaddrinfo para resolver
    try:
        result = socket.getaddrinfo(hostname, None)
        ips = [r[4][0] for r in result]
        return list(set(ips))  # IPs únicos
    except socket.gaierror:
        return []


# Testar
sites = ["google.com", "github.com", "aws.amazon.com"]

for site in sites:
    ips = dns_query(site)
    print(f"{site:20} → {', '.join(map(str, ips)) if ips else 'No IPs'}")
