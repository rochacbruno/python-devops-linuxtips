import logging
from typing import Any

from fastapi import APIRouter, Body, HTTPException
from pydantic import ValidationError

from stacks_core.core import DeployManager
from stacks_core.models import DeployResult
from stacks_core.registry import registry

router = APIRouter(prefix="/api/v1", tags=["stacks"])
deploy_manager = DeployManager()
logger = logging.getLogger(__name__)


@router.post("/deploy/{stack_name}", response_model=DeployResult)
async def deploy_stack(
    stack_name: str, params: dict[str, Any] = Body(examples=[{"name": "my_app"}])
):
    """Deploy de um stack específico."""
    try:
        # Obter stack e validar params
        stack_class = registry.get_stack(stack_name)
        params_class = registry.get_params_class(stack_name)

        # Validar parâmetros
        validated_params = params_class(**params)

        # Executar deploy
        result = deploy_manager.deploy(
            stack_name=stack_name, stack_class=stack_class, params=validated_params
        )

        return result

    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e.errors())
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.exception("Erro inesperado no deploy")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stacks")
async def list_stacks():
    """Lista todos os stacks disponíveis."""
    return registry.list_stacks()


@router.get("/health")
async def health():
    """Health check."""
    return {"status": "healthy"}
