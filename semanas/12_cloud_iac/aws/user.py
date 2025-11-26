import boto3

# Conectar ao IAM
iam = boto3.client(
    "iam",
    #region_name="us-east-1",
    #aws_access_key_id="test",
    #aws_secret_access_key="test",
    # endpoint_url="http://localhost:4566",
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
