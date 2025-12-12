from fabric import Config, SerialGroup

config = Config(overrides={"sudo": {"password": "123456"}})

hosts = [
    "rochacbruno@192.168.1.100",  # db
    "rochacbruno@192.168.1.101",  # app
]

group = SerialGroup(*hosts, connect_kwargs={"password": "123456"})

print("=== Verificando hosts ===\n")

resultados = group.run("hostname && uptime && date -Ins", hide=True)

for conn, resultado in resultados.items():
    print(f"Host: {conn.host}")
    print(f"  {resultado.stdout.strip()}")
    print()
