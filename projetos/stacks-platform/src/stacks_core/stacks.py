"""Definição dos stacks CDK-TF."""

import os

from cdktf import LocalBackend, TerraformOutput, TerraformStack
from cdktf_cdktf_provider_docker.container import Container, ContainerPorts
from cdktf_cdktf_provider_docker.image import Image
from cdktf_cdktf_provider_docker.provider import DockerProvider
from constructs import Construct

from .models import BaseParams, DockerParams


class BaseTerraformStack(TerraformStack):
    """Classe base para todos os stacks do Terraform."""

    provider_name: str = ""

    def __init__(
        self, scope: Construct, id: str, params: BaseParams, tfstate_path: str = None
    ):
        super().__init__(scope, id)
        self.params = params

        # Configurar backend local com caminho customizado
        if tfstate_path:
            LocalBackend(
                self, path=os.path.join(tfstate_path, "terraform.tfstate")
            )

        self.setup_provider()
        self.create_resources()

    def setup_provider(self):
        """Configura o provider (Docker, AWS, etc)."""
        raise NotImplementedError("Subclasses devem implementar setup_provider()")

    def create_resources(self):
        """Cria os recursos de infraestrutura."""
        raise NotImplementedError("Subclasses devem implementar create_resources()")


class WebAppDocker(BaseTerraformStack):
    """Stack para aplicação web com Docker."""

    provider_name = "docker"

    def __init__(
        self, scope: Construct, id: str, params: DockerParams, tfstate_path: str = None
    ):
        self.params: DockerParams = params
        super().__init__(scope, id, params, tfstate_path)

    def setup_provider(self):
        """Configura Docker provider."""
        DockerProvider(self, "docker")

    def create_resources(self):
        """Cria containers Docker."""
        # Imagem principal
        app_image = Image(
            self,
            f"{self.params.name}_image",
            name=self.params.base_image,
            keep_locally=True,
        )

        # Container principal
        app_container = Container(
            self,
            f"{self.params.name}_container",
            name=f"{self.params.name}-app",
            image=app_image.image_id,
            ports=[ContainerPorts(internal=80, external=port) for port in self.params.ports],
        )

        # Outputs do container principal
        TerraformOutput(
            self,
            "app_container_id",
            value=app_container.id,
            description="ID do container da aplicação",
        )

        TerraformOutput(
            self,
            "app_container_name",
            value=app_container.name,
            description="Nome do container da aplicação",
        )

        TerraformOutput(
            self,
            "app_ports",
            value=self.params.ports,
            description="Portas expostas pela aplicação",
        )

        # Database (opcional)
        if self.params.with_database and self.params.database:
            db_image = Image(
                self,
                f"{self.params.name}_db_image",
                name=self.params.database.image,
                keep_locally=True,
            )

            db_container = Container(
                self,
                f"{self.params.name}_db_container",
                name=f"{self.params.name}-db",
                image=db_image.image_id,
                ports=[
                    ContainerPorts(
                        internal=self.params.database.port,
                        external=self.params.database.port,
                    )
                ],
                env=[f"POSTGRES_PASSWORD={self.params.database.password}"],
            )

            # Outputs do database
            TerraformOutput(
                self,
                "db_container_id",
                value=db_container.id,
                description="ID do container do banco de dados",
            )

            TerraformOutput(
                self,
                "db_container_name",
                value=db_container.name,
                description="Nome do container do banco de dados",
            )

            TerraformOutput(
                self,
                "db_port",
                value=self.params.database.port,
                description="Porta do banco de dados",
            )
