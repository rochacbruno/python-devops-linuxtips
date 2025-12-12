from fabric import ThreadingGroup

hosts = [
    "rochacbruno@192.168.1.100",
    "rochacbruno@192.168.1.101",
]

# Criar grupo (execução paralela)
group = ThreadingGroup(*hosts, connect_kwargs={"password": "123456"})

print("=== Executando em paralelo ===\n")

# Comando executado ao mesmo tempo em todos
resultados = group.run("hostname && uptime && date -Ins", hide=True)

for conn, resultado in resultados.items():
    print(f"[{conn.host}]")
    print(resultado.stdout)
