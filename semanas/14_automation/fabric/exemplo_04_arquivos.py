from fabric import Connection

conn = Connection(
    host="192.168.1.100", user="rochacbruno", connect_kwargs={"password": "123456"}
)

with open("config_teste.txt", "w") as f:
    f.write("DATABASE_URL=postgres://localhost/db\n")

resultado = conn.put("config_teste.txt", remote="/tmp/")
print(f"Upload: {resultado.local} -> {resultado.remote}")

conn.run("cat /tmp/config_teste.txt")

resultado = conn.get("/etc/hostname", local="./hostname_do_servidor.txt")
print(f"Download: {resultado.remote} -> {resultado.local}")

conn.close()
