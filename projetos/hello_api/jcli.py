"""Cliente Python para API do Jenkins."""

import os

import requests

TOKEN = os.getenv("JENKINS_TOKEN", "")


class JenkinsClient:
    """Cliente para interagir com Jenkins API."""

    def __init__(self, url: str, username: str, token: str):
        self.url = url.rstrip("/")
        self.auth = (username, token)

    def get_job_info(self, job_name: str) -> dict:
        """Obtém informações de um job."""
        response = requests.get(f"{self.url}/job/{job_name}/api/json", auth=self.auth)
        response.raise_for_status()
        return response.json()

    def trigger_build(self, job_name: str, parameters: dict | None = None) -> int:
        """Dispara build de um job e retorna o número do build."""
        url = f"{self.url}/job/{job_name}/build"

        if parameters:
            url = f"{self.url}/job/{job_name}/buildWithParameters"

        response = requests.post(url, auth=self.auth, data=parameters)
        response.raise_for_status()

        # Obtém o ID da fila
        queue_url = response.headers["Location"]
        queue_id = int(queue_url.split("/")[-2])

        # Aguarda o item da fila se tornar um build
        import time

        while True:
            queue_response = requests.get(f"{queue_url}api/json", auth=self.auth)
            queue_response.raise_for_status()
            queue_data = queue_response.json()

            # Verifica se o build foi criado
            if "executable" in queue_data and queue_data["executable"]:
                return queue_data["executable"]["number"]

            # Se foi cancelado
            if queue_data.get("cancelled"):
                raise RuntimeError(
                    f"Build foi cancelado na fila (queue ID: {queue_id})"
                )

            time.sleep(1)

    def get_build_status(self, job_name: str, build_number: int) -> str:
        """Obtém status de um build."""
        response = requests.get(
            f"{self.url}/job/{job_name}/{build_number}/api/json", auth=self.auth
        )
        response.raise_for_status()
        data = response.json()
        return data["result"] or "RUNNING"

    def list_jobs(self) -> list[str]:
        """Lista todos os jobs."""
        response = requests.get(f"{self.url}/api/json", auth=self.auth)
        response.raise_for_status()
        data = response.json()
        return [job["name"] for job in data["jobs"]]


# Exemplo de uso
if __name__ == "__main__":
    client = JenkinsClient(
        url="http://localhost:8080",
        username="admin",
        token=TOKEN,
    )

    # Lista jobs
    jobs = client.list_jobs()
    print(f"Jobs: {jobs}")

    # Dispara build
    build_id = client.trigger_build("hello")
    print(f"Build disparado: {build_id}")

    # Verifica status
    import time

    while True:
        status = client.get_build_status("hello", build_id)
        print(f"Status: {status}")
        if status in ["SUCCESS", "FAILURE", "ABORTED"]:
            break
        time.sleep(5)
