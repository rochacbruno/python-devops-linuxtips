# AWS com Python

## Requisitos

- Rodar localmente stack AWS (LocalStack) OU
- Ter uma conta AWS para experimentos

---

## 1. Setup LocalStack (Opcional)

Para testar localmente sem custos:


```bash
# Iniciar LocalStack
docker run --name aws -d -p 4566:4566 localstack/localstack

export AWS_ACCESS_KEY_ID=test
export AWS_SECRET_ACCESS_KEY=test
export AWS_DEFAULT_REGION=us-east-1
export AWS_ENDPOINT_URL=http://localhost:4566
```

Verificar se o localstask está executando.

```bash
curl http://localhost:4566/_localstack/health
```

Criar ambiente Python/

```bash
# crie venv
uv venv .venv

# instale as libs
uv pip install boto3 awscli awscli-local localstack

# Testar conexão (com aws instalado localmente)
uv run awslocal s3 ls

# Teste a config
➜ uv run aws configure list                              
      Name                    Value             Type    Location
      ----                    -----             ----    --------
   profile                <not set>             None    None
access_key     ****************test              env    
secret_key     ****************test              env    
    region                us-east-1              env    AWS_DEFAULT_REGION
```


---

## 2. AWS Overview - Arquitetura Básica

```
┌─────────────────────────────────────────────────┐
│                  AWS Cloud                      │
│                                                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │   IAM    │  │   VPC    │  │   EC2    │       │
│  │(Identity)│  │(Network) │  │(Compute) │       │
│  └──────────┘  └──────────┘  └──────────┘       │
│                                                 │
│  ┌──────────┐                                   │
│  │    S3    │                                   │
│  │(Storage) │                                   │
│  └──────────┘                                   │
└─────────────────────────────────────────────────┘
```

---

## 3. Gestão de Identidades (IAM)

### Conceito
IAM controla **quem** pode acessar **o quê** na AWS.

```
User ──> Groups ──> Policies (permissões)
                         │
                         └──> Resources (EC2, S3, etc)
```

### Exemplo Prático: Criar usuário e obter chaves

```python
import boto3

# Conectar ao IAM
iam = boto3.client(
    "iam",
    #region_name="us-east-1",
    #aws_access_key_id="test",
    #aws_secret_access_key="test",
    endpoint_url="http://localhost:4566",
)

# Criar usuário
user = iam.create_user(UserName='demo-user')
print(f"Usuário criado: {user['User']['UserName']}")

# Criar chave de acesso
keys = iam.create_access_key(UserName='demo-user')
print(f"Access Key: {keys['AccessKey']['AccessKeyId']}")
print(f"Secret Key: {keys['AccessKey']['SecretAccessKey']}")

# Listar usuários
users = iam.list_users()
for user in users['Users']:
    print(f"- {user['UserName']}")
```

Verifique no terminal.

```console
➜ uv run awslocal iam list-users

{
    "Users": [
        {
            "Path": "/",
            "UserName": "demo-user",
            "UserId": "8o1gx0muuv6hzkqjx2nu",
            "Arn": "arn:aws:iam::000000000000:user/demo-user",
            "CreateDate": "2025-11-25T19:01:21.075263Z"
        }
    ]
}
```

---

## 4. Network (VPC & Security Groups)

### Conceito
VPC = Rede virtual isolada na AWS

```
┌─────────────────────────────────┐
│           VPC (10.0.0.0/16)     │
│                                 │
│  ┌─────────────────────┐        │
│  │ Subnet (10.0.1.0/24)│        │
│  │                     │        │
│  │  ┌────────────┐     │        │
│  │  │ EC2        │     │        │
│  │  │ Instance   │     │        │
│  │  └────────────┘     │        │
│  │         │           │        │
│  └─────────┼───────────┘        │
│            │                    │
│     ┌──────▼───────┐            │
│     │Security Group│            │
│     │ Port: 22,80  │            │
│     └──────────────┘            │
└─────────────────────────────────┘
```

### Exemplo Prático: Criar Security Group

```python
import boto3

ec2 = boto3.client('ec2')

# Criar Security Group
sg = ec2.create_security_group(
    GroupName='web-server-sg',
    Description='Permite HTTP e SSH'
)
sg_id = sg['GroupId']

# Adicionar regras
ec2.authorize_security_group_ingress(
    GroupId=sg_id,
    IpPermissions=[
        {
            'IpProtocol': 'tcp',
            'FromPort': 22,
            'ToPort': 22,
            'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
        },
        {
            'IpProtocol': 'tcp',
            'FromPort': 80,
            'ToPort': 80,
            'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
        }
    ]
)

print(f"Security Group criado: {sg_id}")
```

---

## 5. EC2 (Compute)

### Conceito
EC2 = Máquinas virtuais na nuvem

```
Lifecycle:
Launch ──> Running ──> Stop ──> Terminate
             │           │
             └──► Restart◄┘
```

### Exemplo Prático: Gerenciar instâncias

```python
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
```

```bash
uv run awslocal ec2 describe-instances --region us-east-1 2>&1
```

---

## 6. S3 (Storage)

### Conceito
S3 = Object storage (armazena arquivos como objetos)

```
┌──────────────┐
│   Bucket     │ (container global)
│              │
│  ┌────────┐  │
│  │file.txt│  │ (objeto)
│  └────────┘  │
│              │
│  ┌────────┐  │
│  │img.png │  │
│  └────────┘  │
└──────────────┘
```

### Exemplo Prático: Gerenciar buckets e arquivos

```bash
echo "Batata123" > local_file.txt
```

agora mandamos esse arquivo para o s3.

```python
import boto3

s3 = boto3.client('s3')

# Criar bucket
bucket_name = 'meu-bucket-demo-123'
s3.create_bucket(Bucket=bucket_name)
print(f"Bucket criado: {bucket_name}")

# Upload de arquivo
s3.upload_file(
    Filename='local_file.txt',
    Bucket=bucket_name,
    Key='remote_file.txt'
)
print("Arquivo enviado")

# Listar objetos
response = s3.list_objects_v2(Bucket=bucket_name)
for obj in response.get('Contents', []):
    print(f"- {obj['Key']} ({obj['Size']} bytes)")

# Download de arquivo
s3.download_file(
    Bucket=bucket_name,
    Key='remote_file.txt',
    Filename='downloaded_file.txt'
)
print("Arquivo baixado")

# Deletar objeto
# s3.delete_object(Bucket=bucket_name, Key='remote_file.txt')

# Deletar bucket
# s3.delete_bucket(Bucket=bucket_name)
```

```bash
uv run awslocal s3 ls
```


---

## 7. Resumo - Fluxo Completo

```
1. IAM      → Criar usuário e permissões
              ↓
2. VPC/SG   → Configurar rede e firewall
              ↓
3. EC2      → Provisionar servidor
              ↓
4. S3       → Armazenar arquivos/backups
```
