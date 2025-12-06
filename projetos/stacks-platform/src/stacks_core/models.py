"""Modelos Pydantic para validação de parâmetros."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class BaseParams(BaseModel):
    """Parâmetros base para todos os stacks."""

    model_config = ConfigDict(extra="forbid")
    name: str = Field(..., description="Nome único do deployment")


class DatabaseConfig(BaseModel):
    """Configuração de banco de dados."""

    image: str = Field("postgres:16-alpine", description="Imagem Docker do banco")
    port: int = Field(5432, description="Porta do banco de dados")
    password: str = Field("changeme", description="Senha do banco")


class DockerParams(BaseParams):
    """Parâmetros para stack Docker."""

    base_image: str = Field("nginx:latest", description="Imagem Docker base")
    ports: list[int] = Field(default=[80], description="Portas a expor")
    with_database: bool = Field(False, description="Incluir container de banco")
    database: DatabaseConfig | None = Field(None, description="Config do banco")


class AWSParams(BaseParams):
    """Parâmetros para stack AWS."""

    region: str = Field("us-east-1", description="Região AWS")
    instance_type: str = Field("t2.micro", description="Tipo de instância EC2")
    ami_id: str = Field("ami-0c55b159cbfafe1f0", description="ID da AMI")
    use_localstack: bool = Field(True, description="Usar LocalStack (local)")


class DeployResult(BaseModel):
    """Resultado de um deploy."""

    status: Literal["success", "failed"]
    message: str
    stack_name: str
    resources: dict = Field(default_factory=dict)
    terraform_dir: str | None = None
