# Exercícios Práticos - Formatos Estruturados

Este diretório contém arquivos de exemplo em diferentes formatos (INI, JSON, YAML, TOML) para praticar serialização e desserialização em Python.

## 📁 Estrutura dos Arquivos

```
estruturados/
├── ini/           # Arquivos .ini (configparser)
├── json/          # Arquivos .json (válidos e inválidos)
├── yaml/          # Arquivos .yaml (válidos, com erros, exemplos reais)
└── toml/          # Arquivos .toml (pyproject.toml, configs)
```

## 🎯 Desafios e Exercícios

### 📌 Nível 1: Básico - Leitura e Escrita

#### Exercício 1.1: Leitor Universal de Configs
**Objetivo:** Criar um script que lê qualquer formato e imprime de forma formatada.

```bash
# Comando esperado
python ler_config.py json/pessoa_valido.json
python ler_config.py yaml/pessoa_valido.yaml
python ler_config.py toml/config_simples.toml
```

**Template para implementar:**
```python
#!/usr/bin/env python3
"""Leitor universal de arquivos de configuração"""

import sys
import json
from pathlib import Path

def ler_arquivo(caminho):
    """
    Lê arquivo baseado na extensão e retorna dict.

    Suporta: .json, .yaml, .yml, .toml, .ini
    """
    arquivo = Path(caminho)
    extensao = arquivo.suffix.lower()

    if extensao == '.json':
        # TODO: Implementar leitura JSON
        pass
    elif extensao in ['.yaml', '.yml']:
        # TODO: Implementar leitura YAML (import yaml)
        pass
    elif extensao == '.toml':
        # TODO: Implementar leitura TOML (import tomllib)
        pass
    elif extensao == '.ini':
        # TODO: Implementar leitura INI (import configparser)
        pass
    else:
        raise ValueError(f"Formato não suportado: {extensao}")

def imprimir_formatado(dados, indent=0):
    """Imprime dados de forma hierárquica"""
    # TODO: Implementar impressão recursiva
    pass

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Uso: python ler_config.py <arquivo>")
        sys.exit(1)

    dados = ler_arquivo(sys.argv[1])
    imprimir_formatado(dados)
```

**Testes:**
```bash
python ler_config.py json/pessoa_valido.json
python ler_config.py yaml/config_com_ancoras.yaml
python ler_config.py toml/config_app.toml
```

---

#### Exercício 1.2: Conversor de Formatos
**Objetivo:** Converter entre JSON, YAML e TOML.

```bash
# Comandos esperados
python converter.py json/pessoa_valido.json yaml/pessoa_convertido.yaml
python converter.py yaml/pessoa_valido.yaml json/pessoa_convertido.json
python converter.py toml/config_simples.toml json/config_simples.json
```

**Template:**
```python
#!/usr/bin/env python3
"""Conversor entre formatos estruturados"""

import sys
import json
from pathlib import Path

def converter(entrada, saida):
    """
    Converte arquivo de entrada para formato de saída.

    Args:
        entrada: Caminho do arquivo de entrada
        saida: Caminho do arquivo de saída
    """
    # TODO: 1. Detectar formato de entrada pela extensão
    # TODO: 2. Ler dados do arquivo de entrada
    # TODO: 3. Detectar formato de saída pela extensão
    # TODO: 4. Escrever dados no formato de saída
    # TODO: 5. Usar ensure_ascii=False para JSON
    # TODO: 6. Usar allow_unicode=True para YAML
    pass

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Uso: python converter.py <entrada> <saida>")
        sys.exit(1)

    converter(sys.argv[1], sys.argv[2])
    print(f"✓ Convertido: {sys.argv[1]} -> {sys.argv[2]}")
```

---

### 📌 Nível 2: Intermediário - Validação e Tratamento de Erros

#### Exercício 2.1: Validador de JSON
**Objetivo:** Validar arquivos JSON e reportar erros detalhados.

```bash
# Testar com arquivos válidos e inválidos
python validar_json.py json/pessoa_valido.json          # ✓ Válido
python validar_json.py json/invalido_virgula_extra.json # ✗ Erro na linha X
python validar_json.py json/invalido_aspas.json         # ✗ Erro: aspas inválidas
```

**Template:**
```python
#!/usr/bin/env python3
"""Validador de arquivos JSON"""

import json
import sys

def validar_json(caminho):
    """
    Valida arquivo JSON e reporta erros.

    Returns:
        tuple: (valido: bool, mensagem: str)
    """
    try:
        with open(caminho, 'r', encoding='utf-8') as f:
            # TODO: Tentar fazer parse do JSON
            # TODO: Retornar (True, "JSON válido!")
            pass
    except json.JSONDecodeError as e:
        # TODO: Extrair informações do erro
        # TODO: Retornar (False, mensagem_detalhada)
        # Dica: e.msg, e.lineno, e.colno
        pass
    except FileNotFoundError:
        # TODO: Tratar arquivo não encontrado
        pass

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Uso: python validar_json.py <arquivo.json>")
        sys.exit(1)

    valido, mensagem = validar_json(sys.argv[1])

    if valido:
        print(f"✓ {mensagem}")
        sys.exit(0)
    else:
        print(f"✗ {mensagem}")
        sys.exit(1)
```

---

#### Exercício 2.2: Validador de YAML
**Objetivo:** Validar YAML e detectar problemas comuns.

```bash
python validar_yaml.py yaml/pessoa_valido.yaml           # ✓ Válido
python validar_yaml.py yaml/invalido_indentacao.yaml     # ✗ Erro de indentação
python validar_yaml.py yaml/inferencia_tipos_problema.yaml  # ⚠ Avisos sobre tipos
```

**Template:**
```python
#!/usr/bin/env python3
"""Validador de arquivos YAML com detecção de problemas"""

import yaml
import sys

def validar_yaml(caminho):
    """
    Valida YAML e detecta problemas comuns.

    Returns:
        dict: {
            'valido': bool,
            'mensagem': str,
            'avisos': list
        }
    """
    resultado = {
        'valido': False,
        'mensagem': '',
        'avisos': []
    }

    try:
        with open(caminho, 'r', encoding='utf-8') as f:
            dados = yaml.safe_load(f)

        # TODO: Marcar como válido

        # TODO: Verificar problemas comuns:
        # - CEPs sem aspas (ex: 01000-000)
        # - Versões como float (ex: 1.0)
        # - Booleanos especiais (yes, no, on, off)

        # Dica: percorrer dados recursivamente

    except yaml.YAMLError as e:
        # TODO: Extrair informações do erro
        pass

    return resultado

def verificar_tipos_suspeitos(dados, caminho=""):
    """
    Verifica tipos que podem ter sido inferidos incorretamente.

    Args:
        dados: Dados parseados do YAML
        caminho: Caminho atual no documento (para mensagens)

    Returns:
        list: Lista de avisos encontrados
    """
    avisos = []

    # TODO: Implementar verificação recursiva
    # Verificar:
    # - Números que parecem CEP (ex: 1000)
    # - Floats que parecem versão (ex: 1.0)
    # - Valores booleanos yes/no/on/off

    return avisos

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Uso: python validar_yaml.py <arquivo.yaml>")
        sys.exit(1)

    resultado = validar_yaml(sys.argv[1])

    if resultado['valido']:
        print(f"✓ {resultado['mensagem']}")
        if resultado['avisos']:
            print("\n⚠ Avisos:")
            for aviso in resultado['avisos']:
                print(f"  - {aviso}")
    else:
        print(f"✗ {resultado['mensagem']}")
        sys.exit(1)
```

---

### 📌 Nível 3: Avançado - Manipulação e Transformação

#### Exercício 3.1: Merge de Configurações
**Objetivo:** Combinar múltiplos arquivos YAML com override.

```bash
# Merge configs (último tem prioridade)
python merge_configs.py \
    yaml/pessoa_valido.yaml \
    yaml/config_com_ancoras.yaml \
    -o merged_config.yaml
```

**Template:**
```python
#!/usr/bin/env python3
"""Merge de múltiplos arquivos de configuração"""

import yaml
import sys

def merge_dict(base, override):
    """
    Faz merge recursivo de dicionários.

    Args:
        base: Dicionário base
        override: Dicionário que sobrescreve valores

    Returns:
        dict: Dicionário merged

    Exemplo:
        base = {'a': 1, 'b': {'c': 2}}
        override = {'b': {'d': 3}, 'e': 4}
        resultado = {'a': 1, 'b': {'c': 2, 'd': 3}, 'e': 4}
    """
    # TODO: Implementar merge recursivo
    # Dica: Se ambos são dict, merge recursivo
    #       Caso contrário, override substitui
    pass

def merge_configs(*arquivos):
    """
    Combina múltiplos arquivos YAML.

    Args:
        *arquivos: Caminhos dos arquivos a combinar

    Returns:
        dict: Configuração final merged
    """
    # TODO: Implementar leitura e merge de todos os arquivos
    pass

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Merge de configs YAML')
    parser.add_argument('arquivos', nargs='+', help='Arquivos para merge')
    parser.add_argument('-o', '--output', required=True, help='Arquivo de saída')

    args = parser.parse_args()

    # TODO: Fazer merge
    # TODO: Salvar resultado

    print(f"✓ Merged {len(args.arquivos)} arquivos -> {args.output}")
```

---

#### Exercício 3.2: Custom JSON Encoder
**Objetivo:** Serializar objetos Python não-suportados nativamente.

```bash
python custom_encoder.py
# Deve serializar datetime, set, Decimal, etc.
```

**Template:**
```python
#!/usr/bin/env python3
"""JSON encoder customizado para tipos Python"""

import json
from datetime import datetime, date, time
from decimal import Decimal
from pathlib import Path

class CustomJSONEncoder(json.JSONEncoder):
    """
    Encoder customizado que suporta:
    - datetime, date, time -> ISO format
    - Decimal -> float
    - set, frozenset -> list
    - Path -> string
    - bytes -> base64 string
    """

    def default(self, obj):
        # TODO: Implementar conversões
        # datetime -> obj.isoformat()
        # Decimal -> float(obj)
        # set -> list(obj)
        # Path -> str(obj)
        # bytes -> base64.b64encode(obj).decode()

        # Se não for nenhum tipo conhecido, chamar super()
        return super().default(obj)

def exemplo_uso():
    """Demonstra uso do encoder customizado"""
    dados = {
        'timestamp': datetime.now(),
        'data': date.today(),
        'hora': time(14, 30, 0),
        'valor': Decimal('99.99'),
        'tags': {'python', 'devops', 'json'},
        'caminho': Path('/home/user/file.txt'),
        'dados_binarios': b'hello world'
    }

    # TODO: Usar CustomJSONEncoder para serializar
    # json_str = json.dumps(dados, cls=CustomJSONEncoder, indent=2)

    pass

if __name__ == '__main__':
    exemplo_uso()
```

---

#### Exercício 3.3: Config Loader Inteligente
**Objetivo:** Carregar configs de múltiplas fontes com prioridade.

```bash
# Carregar config baseado em ambiente
ENV=production python config_loader.py

# Override com variáveis de ambiente
ENV=dev DB_HOST=custom-host python config_loader.py
```

**Template:**
```python
#!/usr/bin/env python3
"""Carregador inteligente de configurações"""

import os
import yaml
from pathlib import Path

class ConfigLoader:
    """
    Carrega configuração de múltiplas fontes em ordem de prioridade:

    1. config/default.yaml (base)
    2. config/{ENV}.yaml (específico do ambiente)
    3. config/local.yaml (overrides locais, gitignored)
    4. Variáveis de ambiente (prefixo APP_)

    Exemplo de variável de ambiente:
        APP_DATABASE_HOST=localhost -> config['database']['host'] = 'localhost'
    """

    def __init__(self, config_dir='config', env_prefix='APP_'):
        self.config_dir = Path(config_dir)
        self.env = os.getenv('ENV', 'dev')
        self.env_prefix = env_prefix
        self.config = {}

    def load(self):
        """Carrega todas as fontes de configuração"""
        # TODO: 1. Carregar config/default.yaml
        # TODO: 2. Carregar config/{self.env}.yaml
        # TODO: 3. Carregar config/local.yaml (se existir)
        # TODO: 4. Carregar variáveis de ambiente

        return self.config

    def _load_yaml(self, arquivo):
        """Carrega arquivo YAML se existir"""
        # TODO: Implementar
        pass

    def _load_env_vars(self):
        """
        Carrega variáveis de ambiente com prefixo.

        Exemplos:
            APP_DATABASE_HOST -> config['database']['host']
            APP_API_PORT -> config['api']['port']
            APP_DEBUG -> config['debug']
        """
        # TODO: Implementar parsing de env vars
        # Dica: split por '_' e usar _set_nested()
        pass

    def _set_nested(self, dicionario, path, valor):
        """
        Define valor em caminho aninhado.

        Exemplo:
            _set_nested(config, ['database', 'host'], 'localhost')
            -> config['database']['host'] = 'localhost'
        """
        # TODO: Implementar
        pass

    def get(self, key, default=None):
        """
        Obtém valor usando notação de ponto.

        Exemplo:
            config.get('database.host')
        """
        # TODO: Implementar
        # Dica: split por '.' e navegar no dict
        pass

if __name__ == '__main__':
    loader = ConfigLoader()
    config = loader.load()

    # TODO: Imprimir configuração final
    print(json.dumps(config, indent=2))
```

---

### 📌 Nível 4: Expert - Casos Reais de DevOps

#### Exercício 4.1: Parser de Logs JSONL
**Objetivo:** Analisar logs em formato JSON Lines.

```bash
# Filtrar logs por nível
python parse_logs.py json/jsonlines_logs.jsonl --level ERROR

# Filtrar por timestamp range
python parse_logs.py json/jsonlines_logs.jsonl \
    --start "2025-01-15T10:30:10" \
    --end "2025-01-15T10:30:25"

# Estatísticas
python parse_logs.py json/jsonlines_logs.jsonl --stats
```

**Template:**
```python
#!/usr/bin/env python3
"""Parser de logs em formato JSON Lines"""

import json
from datetime import datetime
from collections import Counter

def parse_logs(arquivo, level=None, start=None, end=None, stats=False):
    """
    Faz parse de arquivo JSONL de logs.

    Args:
        arquivo: Caminho do arquivo .jsonl
        level: Filtrar por nível (INFO, ERROR, etc.)
        start: Timestamp inicial (ISO format)
        end: Timestamp final (ISO format)
        stats: Se True, mostra estatísticas
    """
    logs = []

    # TODO: 1. Ler arquivo linha por linha
    # TODO: 2. Parse de cada linha como JSON
    # TODO: 3. Aplicar filtros (level, start, end)
    # TODO: 4. Se stats=True, calcular estatísticas

    pass

def calcular_stats(logs):
    """
    Calcula estatísticas dos logs.

    Returns:
        dict: {
            'total': int,
            'por_nivel': Counter,
            'usuarios_unicos': set,
            'erros': list
        }
    """
    # TODO: Implementar
    pass

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Parse de logs JSONL')
    parser.add_argument('arquivo', help='Arquivo .jsonl')
    parser.add_argument('--level', help='Filtrar por nível')
    parser.add_argument('--start', help='Timestamp inicial')
    parser.add_argument('--end', help='Timestamp final')
    parser.add_argument('--stats', action='store_true', help='Mostrar stats')

    args = parser.parse_args()

    parse_logs(
        args.arquivo,
        level=args.level,
        start=args.start,
        end=args.end,
        stats=args.stats
    )
```

---

#### Exercício 4.2: Gerador de Kubernetes Manifests
**Objetivo:** Gerar YAML de deployment K8s a partir de template.

```bash
# Gerar deployment
python k8s_generator.py \
    --app nginx \
    --image nginx:1.14.2 \
    --replicas 3 \
    --port 80 \
    -o deployment.yaml
```

**Template:**
```python
#!/usr/bin/env python3
"""Gerador de manifests Kubernetes"""

import yaml

def gerar_deployment(app, image, replicas=1, port=80, env_vars=None):
    """
    Gera deployment YAML para Kubernetes.

    Args:
        app: Nome da aplicação
        image: Imagem Docker
        replicas: Número de réplicas
        port: Porta do container
        env_vars: Dict de variáveis de ambiente

    Returns:
        dict: Manifest do deployment
    """
    # TODO: Criar estrutura do deployment
    # Use yaml/kubernetes_deployment.yaml como referência

    deployment = {
        'apiVersion': 'apps/v1',
        'kind': 'Deployment',
        'metadata': {
            # TODO: Preencher metadata
        },
        'spec': {
            # TODO: Preencher spec
            # - replicas
            # - selector
            # - template
            #   - metadata
            #   - spec
            #     - containers
        }
    }

    return deployment

def gerar_service(app, port, target_port):
    """Gera service YAML"""
    # TODO: Implementar
    pass

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Gerador de K8s manifests')
    parser.add_argument('--app', required=True, help='Nome da app')
    parser.add_argument('--image', required=True, help='Imagem Docker')
    parser.add_argument('--replicas', type=int, default=1)
    parser.add_argument('--port', type=int, default=80)
    parser.add_argument('--env', action='append', help='VAR=value')
    parser.add_argument('-o', '--output', required=True)

    args = parser.parse_args()

    # TODO: Parse env vars (format: KEY=VALUE)
    # TODO: Gerar deployment
    # TODO: Salvar YAML
```

---

#### Exercício 4.3: Validador de pyproject.toml
**Objetivo:** Validar estrutura de pyproject.toml.

```bash
python validar_pyproject.py toml/pyproject_exemplo.toml
```

**Template:**
```python
#!/usr/bin/env python3
"""Validador de pyproject.toml"""

import tomllib
import sys

REQUIRED_FIELDS = {
    'project': ['name', 'version'],
    'build-system': ['requires', 'build-backend']
}

RECOMMENDED_FIELDS = {
    'project': ['description', 'readme', 'requires-python', 'license', 'authors']
}

def validar_pyproject(caminho):
    """
    Valida estrutura de pyproject.toml.

    Verifica:
    - Campos obrigatórios
    - Campos recomendados
    - Formato de versão (PEP 440)
    - Python version (>=X.Y)
    - Dependencies válidas
    """
    resultado = {
        'valido': True,
        'erros': [],
        'avisos': []
    }

    # TODO: 1. Ler arquivo TOML
    # TODO: 2. Verificar campos obrigatórios
    # TODO: 3. Verificar campos recomendados
    # TODO: 4. Validar formato de versão
    # TODO: 5. Validar requires-python

    return resultado

def validar_versao(versao):
    """Valida formato de versão (PEP 440)"""
    # TODO: Implementar validação básica
    # Formato: X.Y.Z ou X.Y.Z.devN, etc.
    pass

def validar_python_version(requires_python):
    """Valida formato de requires-python"""
    # TODO: Validar formatos como ">=3.10", ">=3.10,<4.0"
    pass

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Uso: python validar_pyproject.py <pyproject.toml>")
        sys.exit(1)

    resultado = validar_pyproject(sys.argv[1])

    if resultado['erros']:
        print("❌ Erros encontrados:")
        for erro in resultado['erros']:
            print(f"  - {erro}")

    if resultado['avisos']:
        print("\n⚠ Avisos:")
        for aviso in resultado['avisos']:
            print(f"  - {aviso}")

    if resultado['valido'] and not resultado['avisos']:
        print("✓ pyproject.toml válido!")

    sys.exit(0 if resultado['valido'] else 1)
```

---

## 🎓 Desafios Extras

### Desafio 1: GitHub Actions Validator
Valide arquivos de workflow do GitHub Actions (`yaml/github_actions.yaml`):
- Verificar campos obrigatórios (name, on, jobs)
- Validar sintaxe de triggers
- Verificar steps válidos

### Desafio 2: Config Diff Tool
Compare duas configurações e mostre diferenças:
```bash
python config_diff.py yaml/pessoa_valido.yaml json/pessoa_valido.json
```

### Desafio 3: Secrets Manager
Crie ferramenta para criptografar valores sensíveis em configs:
```bash
python secrets.py encrypt toml/config_app.toml \
    --fields database.password cache.password
```

### Desafio 4: Multi-Format Linter
Crie linter que verifica:
- JSON: trailing commas, aspas simples
- YAML: indentação, âncoras quebradas, tipos suspeitos
- TOML: arrays homogêneos, datas válidas

### Desafio 5: Config Template Engine
Implemente substituição de variáveis em configs:
```yaml
database:
  host: ${DB_HOST:localhost}  # Default: localhost
  port: ${DB_PORT}            # Obrigatório
```

---

## 📚 Recursos Adicionais

### Documentação
- JSON: https://docs.python.org/3/library/json.html
- YAML: https://pyyaml.org/wiki/PyYAMLDocumentation
- TOML: https://docs.python.org/3/library/tomllib.html
- INI: https://docs.python.org/3/library/configparser.html

### Ferramentas CLI Úteis
```bash
# Validar JSON
python -m json.tool arquivo.json

# Pretty print JSON
jq '.' arquivo.json

# Validar YAML
yamllint arquivo.yaml

# Converter YAML <-> JSON
yq eval arquivo.yaml -o json
```

### Dicas de Boas Práticas
1. **JSON**: Sempre use `ensure_ascii=False` para UTF-8
2. **YAML**: Prefira `safe_load()` ao invés de `load()`
3. **TOML**: Use `tomllib` (Python 3.11+) para leitura
4. **Encoding**: Sempre especifique `encoding='utf-8'`
5. **Validação**: Valide dados com schemas quando possível (jsonschema)

---

## 🏆 Como Submeter

1. Implemente os exercícios em arquivos separados
2. Teste com os arquivos fornecidos neste diretório
3. Adicione testes unitários (opcional)
4. Documente seu código com docstrings

**Estrutura recomendada:**
```
exercicios/
├── nivel1/
│   ├── ler_config.py
│   └── converter.py
├── nivel2/
│   ├── validar_json.py
│   └── validar_yaml.py
├── nivel3/
│   ├── merge_configs.py
│   ├── custom_encoder.py
│   └── config_loader.py
└── nivel4/
    ├── parse_logs.py
    ├── k8s_generator.py
    └── validar_pyproject.py
```

Boa sorte! 🚀
