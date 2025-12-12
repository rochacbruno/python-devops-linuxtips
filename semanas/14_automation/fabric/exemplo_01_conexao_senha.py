from fabric import connection 

conn = connection.Connection(
    host="192.168.1.100",
    user="rochacbruno",
    connect_kwargs={"password": "123456"},
)

resultado = conn.run("sleep 10 & hostname", hide=True)
print(resultado.stdout.strip())

conn.close()
