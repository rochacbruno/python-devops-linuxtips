import subprocess
import sys
from pathlib import Path

import uvicorn
from fastapi import BackgroundTasks, Depends, FastAPI, Header, Request

from .utils import gate_by_github_ip

app = FastAPI()


@app.post("/", dependencies=[Depends(gate_by_github_ip)])
async def receive_payload(
    request: Request,
    background_tasks: BackgroundTasks,
    x_github_event: str = Header(...),
):
    match x_github_event:
        case "create":
            payload = await request.json()
            ref_type = payload.get("ref_type")

            if ref_type != "tag":
                return {
                    "message": f"Ref type {ref_type} received. No action taken."
                }
            ref = payload.get("ref")
            repository = payload.get("repository", {}).get("full_name")
            background_tasks.add_task(deploy, repository, ref)

            return {
                "message": f"Deployment on {repository} for tag {ref} started."
            }
        case "ping":
            return {"message": "pong"}
        case _:
            return {
                "message": f"Event {x_github_event} received. No action taken."
            }


def deploy(repository: str, ref: str) -> None:
    """
    Will look for a deployment script on ./deployment/{repository}/deploy.sh
    and execute it with the ref as argument.
    """

    if not repository or not ref:
        print("Repository or ref not provided. Aborting deployment.")

        return

    deployment_script_path = Path(f"deployment/{repository}/deploy.sh")

    if not deployment_script_path.exists():
        print(f"Deployment script not found for {repository}.")

        return

    try:
        subprocess.run(
            [str(deployment_script_path), ref],
            check=True,
        )
        print(f"Deployment script executed for {repository}.")
    except subprocess.CalledProcessError as e:
        print(f"Error executing deployment script for {repository}: {e}")


def main() -> None:
    """
    Main entry point for running the FastAPI application.

    when --uds is passed it takes the next argument as the socket path
    when --host and --port are passed it takes the next two arguments as
    host and port

    Example:
        gancho --host 127.0.0.1 --port 5000
        gancho --uds /path/to/socket

    when nothing is passed it defaults to 127.0.0.0 and port 5000
    """
    args = sys.argv[1:]

    if "--uds" in args:
        uds_index = args.index("--uds") + 1

        if uds_index < len(args):
            uds_path = args[uds_index]
            uvicorn.run(app, uds=uds_path, log_level="debug")
    elif "--host" in args and "--port" in args:
        host_index = args.index("--host") + 1
        port_index = args.index("--port") + 1

        if host_index < len(args) and port_index < len(args):
            host = args[host_index]
            port = int(args[port_index])
            uvicorn.run(app, host=host, port=port, log_level="debug")
    else:
        uvicorn.run(app, host="127.0.0.1", port=5000, log_level="debug")
