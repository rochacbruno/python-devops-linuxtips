# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "psutil",
#     "xdg-base-dirs",
#     "pygithub",
#     "cryptography",
#     "hvac",
# ]
# ///
"""
Depdends on a running vault:

$ {podman or docker} run --rm -d --cap-add=IPC_LOCK \
  -e 'VAULT_DEV_ROOT_TOKEN_ID=root' \
  -p 8200:8200 \
  --name vault \
  docker.io/hashicorp/vaul

"""
import os
import json
from sys import set_coroutine_origin_tracking_depth
from typing import Any
import psutil
import tomllib
from pathlib import Path
from xdg_base_dirs import xdg_config_home
from collections import ChainMap
from argparse import ArgumentParser, Namespace
from github import Github, Auth
import getpass
from cryptography.fernet import Fernet
import hvac

ConfigDict = dict[str, Any]
ConfigChain = ChainMap[str, Any]


def check_cpu_usage():
    return psutil.cpu_percent(interval=1)


def check_memory_usage():
    return psutil.virtual_memory().percent


def check_disk_usage():
    return psutil.disk_usage("/").percent


def check_ci_status(repo_name: str, config: ConfigChain) -> str:
    g = Github(auth=Auth.Token(config["github_token"]))
    repo = g.get_repo(repo_name)
    runs = repo.get_workflow_runs()
    latest = runs[0]
    if latest.status == "completed":
        return latest.conclusion
    return latest.status


def build_text(config: ConfigChain) -> str:
    components = {
        "CPU": {"icon": "", "data": f"{check_cpu_usage()}%"},
        "MEM": {"icon": "", "data": f"{check_memory_usage()}%"},
        "DISC": {"icon": "", "data": f"{check_disk_usage()}%"},
    }
    if repo := config.get("github_repo"):
        components["GHA"] = {
            "icon": "",
            "data": check_ci_status(repo_name=repo, config=config),
        }
    if "GHA" in config["enabled_components"] and not config.get("github_repo"):
        print(f"GHA requires --github-repo and --github-token")
        exit(1)

    parts = []

    for title in config["enabled_components"]:
        component = components[title]
        icon = component.get("icon", "")
        data = component["data"]
        parts.append(f"{icon} {title}: {data}")

    return "\n".join(parts)


def load_config_from_file(filename: str) -> ConfigDict:
    config_base = Path(xdg_config_home()) / "dash"
    config_base.mkdir(parents=True, exist_ok=True)
    config_filename = config_base / filename
    try:
        with open(config_filename, "rb") as f:
            config = tomllib.load(f)
            return {k.lower(): v for k, v in config.items()}
    except FileNotFoundError:
        return {}


def parse_value(k: str, value: Any):
    if k == "enabled_components":
        return value.split(",")
    return value


def format_key(key: str, prefix: str = ""):
    return key.removeprefix(prefix).lower()


def load_env_config(prefix: str) -> ConfigDict:
    prefix = f"{prefix}_"
    config = {
        format_key(k, prefix): parse_value(format_key(k), v)
        for k, v in os.environ.items()
        if k.startswith(prefix)
    }
    return config


def parse_cli_config(cli_config: ConfigDict) -> ConfigDict:
    return {k: v for k, v in cli_config.items() if v is not None}


def load_config(cli_config: ConfigDict) -> ConfigChain:
    default_config = {"enabled_components": ["CPU", "MEM", "DISC"]}
    file_config = load_config_from_file("config.toml")
    # secrets_config = load_config_from_file(".secrets.toml")
    secrets_config = load_secrets()
    env_config = load_env_config("DASH")
    cli_config = parse_cli_config(cli_config)
    return ChainMap(
        cli_config,
        env_config,
        secrets_config,
        file_config,
        default_config,
    )


def build_cli() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument(
        "--enabled-components",
        "-c",
        dest="enabled_components",
        # action="append"
        # nargs="*"
        type=lambda v: v.split(","),
    )
    parser.add_argument("--auth", action="store_true", required=False, default=False)
    args = parser.parse_args()
    return args


def create_vault_client():
    client = hvac.Client("http://127.0.0.1:8200", token=os.environ["VAULT_TOKEN"])
    assert client.is_authenticated()
    return client


def handle_auth():
    # Client vault
    client = create_vault_client()
    # prompt user
    github_token = getpass.getpass("Github Token: ")
    # save to vault
    client.secrets.kv.v2.create_or_update_secret(
        path="dash", secret={"github_token": github_token}
    )
    print("auth credentials saved")


def load_secrets() -> ConfigDict:
    secrets = {}
    # client
    client = create_vault_client()
    # ler o secret
    secret = client.secrets.kv.v2.read_secret_version(
        path="dash", raise_on_deleted_version=True
    )
    secrets["github_token"] = secret["data"]["data"]["github_token"]
    return secrets


if __name__ == "__main__":
    cli = build_cli()
    if cli.auth:
        handle_auth()
        exit(0)
    config = load_config(cli_config=vars(cli))
    text = build_text(config)
    print(text)
