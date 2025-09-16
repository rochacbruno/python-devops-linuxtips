# HashiCorp Vault
import hvac
import os
import boto3
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

# HashiCorp Vault
client = hvac.Client(url='http://localhost:8200')
client.token = os.environ['VAULT_TOKEN']
secret = client.secrets.kv.v2.read_secret_version(path='myapp/config')

# AWS Secrets Manager
client = boto3.client('secretsmanager')
response = client.get_secret_value(SecretId='prod/myapp/db')

# Azure Key Vault
vault_url = "https://myvault.vault.azure.net/"
client = SecretClient(vault_url=vault_url, credential=DefaultAzureCredential())
secret = client.get_secret("mySecret")