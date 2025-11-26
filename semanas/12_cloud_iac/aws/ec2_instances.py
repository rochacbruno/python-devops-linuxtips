import boto3

ec2 = boto3.resource('ec2')

# Criar instância
instances = ec2.create_instances(
    ImageId='ami-0c55b159cbfafe1f0',  # Amazon Linux 2
    MinCount=1,
    MaxCount=1,
    InstanceType='t2.micro',
    KeyName='my-key-pair'
)

instance = instances[0]
print(f"Instância criada: {instance.id}")

# Esperar ficar disponível
instance.wait_until_running()
instance.reload()
print(f"IP Público: {instance.public_ip_address}")

# Listar instâncias
for inst in ec2.instances.all():
    print(f"{inst.id} - {inst.state['Name']}")

# Parar instância
# instance.stop()
# print("Instância parada")

# Terminar instância
# instance.terminate()
