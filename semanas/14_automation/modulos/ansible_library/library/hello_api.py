from ansible.module_utils.basic import AnsibleModule

DOCUMENTATION = r"""
---
module: hello_api
short_description: Interage com a Hello API
description:
    - Envia requisicoes para a Hello API
    - Suporta GET /hello e GET /history
version_added: "1.0.0"
author: "Seu Nome (@github)"
options:
    endpoint:
        description: Endpoint da API (hello ou history)
        required: true
        type: str
        choices: ['hello', 'history']
    word:
        description: Palavra para o endpoint /hello
        required: false
        type: str
        default: 'world'
    base_url:
        description: URL base da API
        required: false
        type: str
        default: 'http://localhost:8000'
    username:
        description: Usuario para autenticacao (endpoint history)
        required: false
        type: str
    password:
        description: Senha para autenticacao (endpoint history)
        required: false
        type: str
        no_log: true
"""

EXAMPLES = r"""
# Chamar /hello
- name: Saudar o mundo
  hello_api:
    endpoint: hello

# Chamar /hello/Bruno
- name: Saudar uma pessoa
  hello_api:
    endpoint: hello
    word: Bruno

# Obter historico (requer auth)
- name: Ver historico
  hello_api:
    endpoint: history
    username: admin
    password: Batata123
"""

RETURN = r"""
message:
    description: Mensagem retornada pela API
    type: str
    returned: quando endpoint=hello
    sample: "Hello World"
history:
    description: Historico de requisicoes
    type: dict
    returned: quando endpoint=history
    sample: {"/hello": 5, "/hello/Bruno": 2}
status_code:
    description: Codigo HTTP da resposta
    type: int
    returned: always
    sample: 200
"""


# Imports condicionais para dependencias externas
try:
    import requests

    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False


def call_hello(base_url, word):
    """Chama o endpoint /hello"""
    url = f"{base_url}/hello/{word}"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.json(), response.status_code


def call_history(base_url, username, password):
    """Chama o endpoint /history com autenticacao"""
    url = f"{base_url}/history"
    response = requests.get(url, auth=(username, password), timeout=10)
    response.raise_for_status()
    return response.json(), response.status_code


def run_module():
    # Definir argumentos aceitos pelo modulo
    module_args = dict(
        endpoint=dict(type="str", required=True, choices=["hello", "history"]),
        word=dict(type="str", required=False, default="world"),
        base_url=dict(type="str", required=False, default="http://localhost:8000"),
        username=dict(type="str", required=False),
        password=dict(type="str", required=False, no_log=True),
    )

    # Resultado inicial
    result = dict(
        changed=False,
        message="",
        status_code=0,
    )

    # Criar instancia do modulo
    module = AnsibleModule(
        argument_spec=module_args,
        required_if=[
            ("endpoint", "history", ["username", "password"]),
        ],
        supports_check_mode=True,
    )

    # Verificar dependencia
    if not HAS_REQUESTS:
        module.fail_json(
            msg="O modulo 'requests' e necessario. Instale com: pip install requests"
        )

    # Check mode - nao executa nada
    if module.check_mode:
        module.exit_json(**result)

    # Extrair parametros
    endpoint = module.params["endpoint"]
    word = module.params["word"]
    base_url = module.params["base_url"]
    username = module.params["username"]
    password = module.params["password"]

    try:
        if endpoint == "hello":
            data, status_code = call_hello(base_url, word)
            result["message"] = data.get("message", "")
            result["status_code"] = status_code
            result["changed"] = True  # Incrementou contador na API

        elif endpoint == "history":
            data, status_code = call_history(base_url, username, password)
            result["history"] = data
            result["status_code"] = status_code
            result["changed"] = False  # Apenas leitura

    except requests.exceptions.ConnectionError:
        module.fail_json(msg=f"Nao foi possivel conectar em {base_url}", **result)
    except requests.exceptions.Timeout:
        module.fail_json(msg="Timeout ao conectar na API", **result)
    except requests.exceptions.HTTPError as e:
        module.fail_json(msg=f"Erro HTTP: {e}", **result)
    except Exception as e:
        module.fail_json(msg=f"Erro inesperado: {str(e)}", **result)

    # Sucesso
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
