"""Cliente Python para API do Jenkins usando python-jenkins library."""

import os
import time

import jenkins

TOKEN = os.getenv("JENKINS_TOKEN", "")


class JenkinsClient:
    """Cliente para interagir com Jenkins API usando python-jenkins."""

    def __init__(self, url: str, username: str, token: str):
        """Inicializa o cliente Jenkins.

        Args:
            url: URL do servidor Jenkins
            username: Nome de usuário
            token: Token de autenticação
        """
        self.server = jenkins.Jenkins(url, username=username, password=token)
        self._username = username
        self._token = token

    def get_job_info(self, job_name: str) -> dict:
        """Obtém informações de um job.

        Args:
            job_name: Nome do job

        Returns:
            Dicionário com informações do job
        """
        return self.server.get_job_info(job_name)

    def trigger_build(self, job_name: str, parameters: dict | None = None) -> int:
        """Dispara build de um job e retorna o número do build.

        Args:
            job_name: Nome do job
            parameters: Parâmetros do build (opcional)

        Returns:
            Número do build disparado
        """
        # Pega o número do último build antes de disparar
        job_info = self.server.get_job_info(job_name)
        last_build_number = job_info.get("lastBuild", {}).get("number", 0) or 0

        # Dispara o build
        queue_number = self.server.build_job(job_name, parameters=parameters)

        # Aguarda o build ser criado
        while True:
            try:
                job_info = self.server.get_job_info(job_name)
                current_build_number = (
                    job_info.get("lastBuild", {}).get("number", 0) or 0
                )

                if current_build_number > last_build_number:
                    return current_build_number

                # Verifica se o item na fila foi cancelado
                queue_item = self.server.get_queue_item(queue_number)
                if queue_item.get("cancelled"):
                    raise RuntimeError(
                        f"Build foi cancelado na fila (queue ID: {queue_number})"
                    )
            except jenkins.NotFoundException:
                # Item já saiu da fila, continua esperando o build aparecer
                pass

            time.sleep(1)

    def get_build_status(self, job_name: str, build_number: int) -> str:
        """Obtém status de um build.

        Args:
            job_name: Nome do job
            build_number: Número do build

        Returns:
            Status do build (SUCCESS, FAILURE, RUNNING, etc)
        """
        build_info = self.server.get_build_info(job_name, build_number)
        return build_info["result"] or "RUNNING"

    def list_jobs(self) -> list[str]:
        """Lista todos os jobs.

        Returns:
            Lista com nomes dos jobs
        """
        jobs = self.server.get_jobs()
        return [job["name"] for job in jobs]

    def get_build_console_output(self, job_name: str, build_number: int) -> str:
        """Obtém o console output de um build.

        Args:
            job_name: Nome do job
            build_number: Número do build

        Returns:
            Console output do build
        """
        return self.server.get_build_console_output(job_name, build_number)

    def stop_build(self, job_name: str, build_number: int) -> None:
        """Para um build em execução.

        Args:
            job_name: Nome do job
            build_number: Número do build
        """
        self.server.stop_build(job_name, build_number)

    def delete_job(self, job_name: str) -> None:
        """Deleta um job.

        Args:
            job_name: Nome do job
        """
        self.server.delete_job(job_name)

    def create_job(self, job_name: str, config_xml: str) -> None:
        """Cria um novo job.

        Args:
            job_name: Nome do job
            config_xml: Configuração XML do job
        """
        self.server.create_job(job_name, config_xml)

    def get_version(self) -> str:
        """Obtém a versão do Jenkins.

        Returns:
            Versão do Jenkins
        """
        # Workaround: get_version() in python-jenkins 1.8.3 doesn't send auth
        # Use authenticated request to get version from headers instead
        import requests

        response = requests.get(
            f"{self.server.server}api/json", auth=(self._username, self._token)
        )
        response.raise_for_status()
        return response.headers.get("X-Jenkins", "Unknown")


# Exemplo de uso
if __name__ == "__main__":
    client = JenkinsClient(
        url="http://localhost:8080",
        username="admin",
        token=TOKEN,
    )

    # Obtém versão do Jenkins
    version = client.get_version()
    print(f"Jenkins version: {version}")

    # Lista jobs
    jobs = client.list_jobs()
    print(f"Jobs: {jobs}")

    # Dispara build
    build_id = client.trigger_build("hello")
    print(f"Build disparado: {build_id}")

    # Verifica status
    while True:
        status = client.get_build_status("hello", build_id)
        print(f"Status: {status}")
        if status in ["SUCCESS", "FAILURE", "ABORTED"]:
            break
        time.sleep(5)

    # Exibe console output
    console = client.get_build_console_output("hello", build_id)
    print(f"\nConsole Output:\n{console}")
