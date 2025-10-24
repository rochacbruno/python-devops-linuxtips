# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "psutil",
#     "xdg-base-dirs",
#     "pygithub",
#     "hvac",
#     "dynaconf",
# ]
# ///
import os
import json
from typing import Any
import psutil
import tomllib
from pathlib import Path
from xdg_base_dirs import xdg_config_home
from argparse import ArgumentParser, Namespace
from github import Github, Auth
import getpass
import hvac


# ---- settings ----------
from dynaconf import Dynaconf, ValidationError, Validator


default_config = {"enabled_components": ["CPU", "MEM", "DISC"]}

config = Dynaconf(
    root_path=Path(xdg_config_home()) / "dash",
    settings_files=["config.toml"],
    envvar_prefix="DASH",
    vault_enabled=True,
    vault_path="dash",
    **default_config,
)
validators = [
    Validator("enabled_components", is_type_of=list),
    Validator(
        "github_token", required=True, when=Validator("github_repo", must_exist=True)
    ),
    Validator(
        "github_repo", required=True, when=Validator("enabled_components", cont="GHA")
    ),
]
config.validators.register(*validators)
# -----------------------


def check_cpu_usage():
    return psutil.cpu_percent(interval=1)


def check_memory_usage():
    return psutil.virtual_memory().percent


def check_disk_usage():
    return psutil.disk_usage("/").percent


def check_ci_status(repo_name: str) -> str:
    g = Github(auth=Auth.Token(config.get("github_token")))
    repo = g.get_repo(repo_name)
    runs = repo.get_workflow_runs()
    latest = runs[0]
    if latest.status == "completed":
        return latest.conclusion
    return latest.status


def build_text() -> str:
    components = {
        "CPU": {"icon": "", "data": f"{check_cpu_usage()}%"},
        "MEM": {"icon": "", "data": f"{check_memory_usage()}%"},
        "DISC": {"icon": "", "data": f"{check_disk_usage()}%"},
    }
    if repo := config.get("github_repo"):
        components["GHA"] = {
            "icon": "",
            "data": check_ci_status(repo_name=repo),
        }
    parts = []

    for title in config["enabled_components"]:
        component = components[title]
        icon = component.get("icon", "")
        data = component["data"]
        parts.append(f"{icon} {title}: {data}")

    return "\n".join(parts)


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
    client = hvac.Client(
        f"http://{os.environ['VAULT_HOST_FOR_DYNACONF']}:8200",
        token=os.environ["VAULT_TOKEN_FOR_DYNACONF"],
    )
    assert client.is_authenticated()
    return client


def handle_auth():
    client = create_vault_client()
    github_token = getpass.getpass("Github Token: ")
    client.secrets.kv.v2.create_or_update_secret(
        path="dash", secret={"github_token": github_token}
    )
    print("auth credentials saved")


if __name__ == "__main__":
    cli = build_cli()
    if cli.enabled_components:
        config.set("enabled_components", cli.enabled_components)

    try:
        config.validators.validate()
    except ValidationError as e:
        print(f"Config error: {e}")
        exit(1)

    if cli.auth:
        handle_auth()
        exit(0)
    text = build_text()
    print(text)
