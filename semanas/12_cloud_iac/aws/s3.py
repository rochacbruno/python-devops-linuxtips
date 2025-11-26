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
