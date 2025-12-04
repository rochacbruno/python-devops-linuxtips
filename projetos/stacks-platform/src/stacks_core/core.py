"""Core deployment manager."""

import json
import logging
import os
import subprocess
import tempfile
from typing import Type

from cdktf import App

from .models import BaseParams, DeployResult
from .stacks import BaseTerraformStack

logger = logging.getLogger(__name__)


class DeployError(Exception):
    """Erro durante o deploy."""

    pass


class DeployManager:
    """Gerencia o ciclo de vida dos deploys."""

    def __init__(
        self, terraform_binary: str = "terraform", tfstate_dir: str = "tfstates"
    ):
        self.terraform_binary = terraform_binary
        self.tfstate_dir = os.path.abspath(tfstate_dir)
        # Criar diretório de estados se não existir
        os.makedirs(self.tfstate_dir, exist_ok=True)

    def deploy(
        self,
        stack_name: str,
        stack_class: Type[BaseTerraformStack],
        params: BaseParams,
    ) -> DeployResult:
        """Executa deploy de um stack."""
        logger.info(f"Iniciando deploy: {stack_name}")

        try:
            # Criar diretório persistente para este deploy específico
            deploy_name = params.name
            deploy_dir = os.path.join(self.tfstate_dir, stack_name, deploy_name)
            os.makedirs(deploy_dir, exist_ok=True)

            # Synthesize CDK-TF
            tf_dir = self._synthesize(deploy_dir, stack_name, stack_class, params)

            # Terraform init
            self._run_terraform("init", tf_dir)

            # Terraform apply
            self._run_terraform("apply", tf_dir, auto_approve=True)

            # Extrair outputs do Terraform
            resources = self._get_terraform_outputs(tf_dir)

            logger.info(f"Deploy concluído: {stack_name}")

            return DeployResult(
                status="success",
                message=f"Deploy de {stack_name} realizado com sucesso",
                stack_name=stack_name,
                resources=resources,
                terraform_dir=tf_dir,
            )

        except Exception as e:
            logger.error(f"Erro no deploy: {e}")
            return DeployResult(status="failed", message=str(e), stack_name=stack_name)

    def _synthesize(
        self,
        outdir: str,
        stack_name: str,
        stack_class: Type[BaseTerraformStack],
        params: BaseParams,
    ) -> str:
        """Gera código Terraform usando CDK-TF."""
        app = App(outdir=outdir)
        deploy_name = params.name
        stack_id = f"{stack_name}_{deploy_name}_stack"
        terraform_dir = os.path.join(outdir, "stacks", stack_id)

        # Passar o caminho onde o tfstate deve ser salvo
        stack_class(app, stack_id, params, tfstate_path=terraform_dir)
        app.synth()

        if not os.path.exists(terraform_dir):
            raise DeployError(f"Synth falhou: {terraform_dir} não existe")

        logger.debug(f"Terraform config gerado em: {terraform_dir}")
        return terraform_dir

    def _run_terraform(self, command: str, cwd: str, auto_approve: bool = False):
        """Executa comando terraform."""
        cmd = [self.terraform_binary, command]

        if auto_approve and command == "apply":
            cmd.append("-auto-approve")

        logger.debug(f"Executando: {' '.join(cmd)} em {cwd}")

        result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)

        if result.returncode != 0:
            raise DeployError(f"Terraform {command} falhou:\n{result.stderr}")

        return result.stdout

    def _get_terraform_outputs(self, cwd: str) -> dict:
        """Extrai outputs do Terraform após apply."""
        try:
            cmd = [self.terraform_binary, "output", "-json"]
            logger.debug(f"Extraindo outputs: {' '.join(cmd)} em {cwd}")

            result = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)

            if result.returncode != 0:
                logger.warning(f"Não foi possível extrair outputs: {result.stderr}")
                return {}

            outputs_raw = json.loads(result.stdout)

            # Terraform output -json retorna um dict onde cada chave tem {value, type, sensitive}
            # Extrair apenas os valores
            resources = {key: data["value"] for key, data in outputs_raw.items()}

            logger.debug(f"Outputs extraídos: {resources}")
            return resources

        except Exception as e:
            logger.warning(f"Erro ao extrair outputs do Terraform: {e}")
            return {}
