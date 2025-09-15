# /// script
# requires-python = ">=3.13"
# dependencies = ["fastmcp"]
# ///

from fastmcp import FastMCP
import subprocess

# Criar servidor MCP
mcp = FastMCP("DevOps Tools")

@mcp.tool()
def check_disk_usage(path: str = "/") -> str:
    """Verificar uso de disco no servidor"""
    result = subprocess.run(
        ["df", "-h", path], 
        capture_output=True, 
        text=True
    )
    return result.stdout

@mcp.tool()  
def get_running_containers() -> str:
    """Listar containers Docker em execução"""
    result = subprocess.run(
        ["docker", "ps", "--format", "table"],
        capture_output=True,
        text=True
    )
    return result.stdout

# Executar servidor
if __name__ == "__main__":
    mcp.run()