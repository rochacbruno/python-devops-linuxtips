# /// script  
# requires-python = ">=3.13"
# dependencies = ["pydantic-ai", "mcp"]
# ///

from pydantic_ai import Agent
from mcp import ClientSession, StdioServerParameters

# Conectar ao servidor MCP
server_params = StdioServerParameters(
    command="python",
    args=["mcp_server.py"]
)

async def create_devops_agent():
    # Agent com acesso ao servidor MCP
    agent = Agent(
        "claude-3-5-sonnet-20241022",
        system_prompt="""
        Você é um assistente DevOps.
        Use as ferramentas MCP para:
        - Monitorar recursos do sistema
        - Gerenciar containers Docker  
        - Analisar logs e métricas
        """
    )
    
    # Conectar ferramentas MCP
    async with ClientSession(server_params) as session:
        tools = await session.list_tools()
        agent.add_tools(tools.tools)
        
        # Executar tarefas
        response = await agent.run(
            "Verifique o uso de disco e containers ativos"
        )
        return response