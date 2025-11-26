# Terraform com Python

## 1. O que é Terraform?

Terraform é uma ferramenta de **Infrastructure as Code (IaC)** que permite:
- Descrever infraestrutura como código
- Provisionar recursos de forma declarativa
- Gerenciar múltiplos providers (AWS, Azure, Docker, etc)

### Conceito: Declarativo vs Imperativo

```
Imperativo (script):           Declarativo (Terraform):
1. Criar VM                    resource "vm" {
2. Configurar rede               name = "web-server"
3. Instalar software             size = "small"
4. Iniciar serviço             }
                               ↓
                               Terraform faz tudo
```

### Fluxo de trabalho

```
┌──────────┐      ┌──────────┐      ┌──────────┐
│  Write   │ ───> │   Plan   │ ───> │  Apply   │
│   .tf    │      │(preview) │      │(execute) │
└──────────┘      └──────────┘      └──────────┘
                                          │
                                          ▼
                                    ┌──────────┐
                                    │ Resources│
                                    │ Created  │
                                    └──────────┘
```

---

## 2. Instalação

### Linux/macOS

```bash
# Baixar Terraform
wget https://releases.hashicorp.com/terraform/1.14.0/terraform_1.14.0_linux_amd64.zip
unzip terraform_1.14.0_linux_amd64.zip
sudo mv terraform /usr/local/bin/

# Verificar instalação
terraform version
```

### Via Package Manager

```bash
# Ubuntu/Debian
sudo apt-get update && sudo apt-get install -y terraform

# macOS
brew install terraform

# Verificar
terraform --version
```

---

## 3. Providers - Conceito

Providers são plugins que permitem Terraform interagir com diferentes plataformas.

```
┌──────────────┐
│  Terraform   │
└──────┬───────┘
       │
   ┌───┴────┬────────┬────────┐
   │        │        │        │
┌──▼──┐  ┌──▼──┐  ┌──▼──┐  ┌──▼───┐
│ AWS │  │Azure│  │ GCP │  │Docker│
└─────┘  └─────┘  └─────┘  └──────┘
```

### Exemplo: Docker Provider

```bash
# Instalar Docker
sudo apt-get install docker.io
sudo systemctl start docker
```

**Arquivo: docker/main.tf**

```hcl
terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
}

provider "docker" {
  host = "unix:///var/run/docker.sock"
}

# Baixar imagem nginx
resource "docker_image" "nginx" {
  name = "nginx:latest"
}

# Criar container
resource "docker_container" "web" {
  name  = "meu-nginx"
  image = docker_image.nginx.image_id

  ports {
    internal = 80
    external = 8080
  }
}
```

**Executar:**

```bash
cd docker/
../terraform init      # Baixa providers
../terraform plan      # Preview das mudanças
../terraform apply     # Aplica mudanças (digite 'yes')

# Verificar
curl http://localhost:8080

# Destruir
../terraform destroy
```

---

## 4. HCL (HashiCorp Configuration Language)

### Estrutura Básica

```hcl
# Bloco de recurso
resource "tipo" "nome" {
  argumento = "valor"

  bloco_aninhado {
    chave = "valor"
  }
}

# Variáveis
variable "nome" {
  type    = string
  default = "valor"
}

# Outputs
output "resultado" {
  value = resource.tipo.nome.atributo
}
```

### Exemplo Completo: Infraestrutura Multi-Container

**Arquivo: multi/main.tf**

```hcl
terraform {
  required_providers {
    docker = {
      source = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
}

provider "docker" {}

# Network
resource "docker_network" "app_network" {
  name = "app-network"
}

# Redis
resource "docker_image" "redis" {
  name = "redis:alpine"
}

resource "docker_container" "redis" {
  name  = "redis"
  image = docker_image.redis.image_id

  networks_advanced {
    name = docker_network.app_network.name
  }
}

# Web App
resource "docker_image" "webapp" {
  name = "nginx:alpine"
}

resource "docker_container" "webapp" {
  name  = "webapp"
  image = docker_image.webapp.image_id

  ports {
    internal = 80
    external = 8081
  }

  networks_advanced {
    name = docker_network.app_network.name
  }
}

# Output
output "webapp_url" {
  value = "http://localhost:8080"
}
```

**Executar:**

```bash
cd multi/
../terraform init
../terraform apply -auto-approve
../terraform output webapp_url
```

---

## 5. CDKTF - Terraform com Python

CDKTF permite escrever Terraform usando linguagens de programação (Python, TypeScript, etc).

```
Python Code ──> CDKTF ──> Terraform JSON ──> Resources
```

### Instalação

```bash
uv pip install cdktf cdktf-cdktf-provider-docker
```

### Exemplo: Docker com CDKTF

**Arquivo: docker_stack.py**

```python
#!/usr/bin/env python
from constructs import Construct
from cdktf import App, TerraformStack
from cdktf_cdktf_provider_docker.provider import DockerProvider
from cdktf_cdktf_provider_docker.image import Image
from cdktf_cdktf_provider_docker.container import Container, ContainerPorts


class DockerStack(TerraformStack):
    def __init__(self, scope: Construct, name: str):
        super().__init__(scope, name)

        # Provider
        DockerProvider(self, "docker")

        # Imagem Nginx
        nginx_image = Image(self, "nginx-image",
            name="nginx:latest",
            keep_locally=False
        )

        # Container
        Container(self, "nginx-container",
            name="my-nginx",
            image=nginx_image.image_id,
            ports=[ContainerPorts(
                internal=80,
                external=8082
            )]
        )


app = App()
DockerStack(app, "cdktf-docker")
app.synth()
```

**Executar:**


```bash
uv run docker_stack.py
```

Isso vai gerar `cdktf.out/stacks/cdktf-docker`

```
cd cdktf.out/stacks/cdktf-docker
../../../terraform init
../../../terraform plan
../../../terraform apply

# Testar
curl http://localhost:8082

# Destruir
../../../terraform destroy
```

---

## 6. Exemplo Avançado: Python + CDKTF + AWS

**Arquivo: aws_stack.py**

```python
from constructs import Construct
from cdktf import App, TerraformStack, TerraformOutput
from cdktf_cdktf_provider_aws.provider import AwsProvider, AwsProviderEndpoints
from cdktf_cdktf_provider_aws.instance import Instance
from cdktf_cdktf_provider_aws.s3_bucket import S3Bucket


class AwsInfraStack(TerraformStack):
    def __init__(self, scope: Construct, name: str):
        super().__init__(scope, name)

        # Provider AWS
        AwsProvider(
            self,
            "aws",
            region="us-east-1",
            endpoints=[
                AwsProviderEndpoints(
                    ec2="http://localhost:4566",
                    iam="http://localhost:4566",
                    sts="http://localhost:4566",
                    s3="http://s3.localhost.localstack.cloud:4566",
                ),
            ],
            access_key="test",
            secret_key="test",
            skip_credentials_validation=True,
            skip_metadata_api_check="true",
            skip_requesting_account_id=True,
            s3_use_path_style=True,  # Critical for LocalStack S3
        )
        # Bucket S3
        bucket = S3Bucket(
            self,
            "my-bucket",
            bucket="my-cdktf-bucket-demo-123",
            tags={"Environment": "Dev"},
            timeouts={"create": "1m", "update": "1m", "delete": "1m"},
        )

        # EC2 Instance
        instance = Instance(
            self,
            "web-server",
            ami="ami-ff0fea8310f3",
            instance_type="m5.large",  # Use non-burstable instance (no credit_specification)
            tags={"Name": "WebServer"},
            # Add timeouts to prevent hanging
            timeouts={"create": "2m", "update": "2m", "delete": "2m"},
        )

        # Outputs
        TerraformOutput(self, "bucket_name", value=bucket.bucket)
        TerraformOutput(self, "instance_ip", value=instance.public_ip)


app = App()
AwsInfraStack(app, "aws-infra")
app.synth()
```

**Executar:**

```bash
uv run aws_stack.py
```

Isto gera o arquivo `cdktf.out/stacks/aws-infra`

```bash
cd cdktf.out/stacks.aws-infra
../../../terraform init
../../../terraform plan
../../../terraform apply
```

```bash
uv run awslocal ec2 describe-instances --region us-east-1 2>&1
uv run awslocal s3 ls
```

---

## 7. Usando Python para Gerenciar Terraform

### Executar Terraform via Python

```python
import subprocess
import json


def terraform_init():
    """Inicializa Terraform"""
    subprocess.run(["terraform", "init"], check=True)


def terraform_plan():
    """Mostra preview das mudanças"""
    result = subprocess.run(
        ["terraform", "plan", "-json"],
        capture_output=True,
        text=True
    )
    return result.stdout


def terraform_apply():
    """Aplica mudanças"""
    subprocess.run(
        ["terraform", "apply", "-auto-approve"],
        check=True
    )


def terraform_output():
    """Obtém outputs"""
    result = subprocess.run(
        ["terraform", "output", "-json"],
        capture_output=True,
        text=True
    )
    return json.loads(result.stdout)


def terraform_destroy():
    """Destrói recursos"""
    subprocess.run(
        ["terraform", "destroy", "-auto-approve"],
        check=True
    )


# Uso
if __name__ == "__main__":
    print("Inicializando...")
    terraform_init()

    print("Aplicando infraestrutura...")
    terraform_apply()

    print("Outputs:")
    outputs = terraform_output()
    for key, value in outputs.items():
        print(f"  {key}: {value['value']}")
```
---

## 9. Resumo - Fluxo Completo

```
┌─────────────────────────────────────────┐
│         Abordagem 1: HCL Puro           │
├─────────────────────────────────────────┤
│ 1. Escrever .tf                         │
│ 2. terraform init/plan/apply            │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│       Abordagem 2: Python + CDKTF       │
├─────────────────────────────────────────┤
│ 1. Escrever Python                      │
│ 2. cdktf synth (gera .tf)               │
│ 3. cdktf deploy                         │
└─────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  Abordagem 3: Python controla Terraform │
├─────────────────────────────────────────┤
│ 1. Escrever .tf                         │
│ 2. subprocess.run(["terraform", ...])   │
│ 3. Automatizar com Python               │
└─────────────────────────────────────────┘
```

---

## Links Úteis

- Terraform Docs: https://developer.hashicorp.com/terraform
- CDKTF: https://developer.hashicorp.com/terraform/cdktf
- Providers Registry: https://registry.terraform.io/
