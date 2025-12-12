
from fabric import Config, Connection


config = Config(overrides={"sudo": {"password": "123456"}})


conn = Connection(
    host="192.168.1.100",
    user="rochacbruno",  # usuário não-root
    config=config,
    connect_kwargs={"password": "123456"},
)

resultado = conn.run("whoami", hide=True)
print(f"Usuário atual: {resultado.stdout.strip()}")

resultado = conn.sudo("whoami", hide=True)
print(f"Com sudo: {resultado.stdout.strip()}")

conn.close()
