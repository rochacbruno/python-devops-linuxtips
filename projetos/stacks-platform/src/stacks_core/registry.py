"""Registry pattern para gerenciar stacks disponíveis."""

from typing import Dict, Type


class StackRegistry:
    """Registro central de stacks disponíveis."""

    def __init__(self):
        self._stacks: Dict[str, Type] = {}
        self._params_classes: Dict[str, Type] = {}

    def register(self, name: str, stack_class: Type, params_class: Type):
        """Registra um novo stack."""
        self._stacks[name] = stack_class
        self._params_classes[name] = params_class

    def get_stack(self, name: str) -> Type:
        """Obtém classe do stack pelo nome."""
        if name not in self._stacks:
            raise ValueError(f"Stack '{name}' não encontrado")
        return self._stacks[name]

    def get_params_class(self, name: str) -> Type:
        """Obtém classe de parâmetros pelo nome."""
        if name not in self._params_classes:
            raise ValueError(f"Params para '{name}' não encontrado")
        return self._params_classes[name]

    def list_stacks(self) -> dict:
        """Lista todos os stacks disponíveis."""
        return {
            name: {"params_schema": params_class.model_json_schema()}
            for name, params_class in self._params_classes.items()
        }


# Instância global do registry
registry = StackRegistry()
