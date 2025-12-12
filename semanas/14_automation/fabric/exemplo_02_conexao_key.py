
from fabric import connection

conn = connection.Connection(
    host="192.168.1.100",
    user="rochacbruno",
    connect_kwargs={"key_filename": "exemple_key"},
)

resultado = conn.run("hostname", hide=True)
print(resultado.stdout.strip())

conn.close()
