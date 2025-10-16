---
title: Python CLI Moderno
sub_title: Melhores práticas para desenvolver aplicações CLI em Python
author: Bruno Rocha - LINUXtips
options:
  implicit_slide_ends: true
  end_slide_shorthand: true
  incremental_lists: true
---

Melhores práticas para desenvolver aplicações CLI em Python Moderno
===

<!-- alignment: center -->

**Python para DevOps - Semana 07**

<!-- pause --> 

Bruno Rocha - LINUXtips

Agenda
===

- Organização de projetos CLI
- Documentação com docstrings
- Entry points e executáveis
- Build system e empacotamento
- Ferramentas modernas: uv
- ZipApps para distribuição
- Boas práticas de CLI (clig.dev)
- Argparse para argumentos
- Projeto prático: **ft** (File Tool)

Organização de Projetos CLI
===

Estrutura recomendada:

```
meu_cli/
├── pyproject.toml
├── src/
│   └── meu_cli/
│       ├── __init__.py
│       ├── __main__.py
│       ├── cli.py
│       ├── core.py
│       └── utils.py
├── tests/
└── README.md
```

<!-- pause -->

- **src/** layout para evitar imports acidentais
- **__main__.py** para `python -m meu_cli`
- **cli.py** para interface de comando
- **core.py** para lógica de negócio

Docstrings
===

<!-- column_layout: [1, 1] -->
<!-- column: 0 -->

**❌ Sem documentação:**

```python
def convert_file(input_file, output_file, 
                input_format, output_format):
    # código aqui
    pass
```

<!-- column: 1 -->

**✅ Com docstring:**

```python
def convert_file(input_file: str, output_file: str, 
                input_format: str, output_format: str) -> bool:
    """Converte arquivo entre formatos.
    
    Args:
        input_file: Caminho do arquivo origem
        output_file: Caminho do arquivo destino
        input_format: Formato origem (json, yaml, csv)
        output_format: Formato destino (json, yaml, csv)
        
    Returns:
        True se conversão foi bem-sucedida
        
    Raises:
        FileNotFoundError: Arquivo não encontrado
        ValueError: Formato não suportado
    """
    # código aqui
    pass
```

Entry Points e Scripts Executáveis
===

**pyproject.toml** - Configurando executáveis:

```toml
[project]
name = "meu-cli"
scripts = ["src/meu_cli/scripts/meu_script.py"]

[project.scripts]
meu-cli = "meu_cli.cli:main"
ft = "meu_cli.cli:main"

[project.entry-points."console_scripts"]
meu-cli-dev = "meu_cli.cli:dev_main"
```

<!-- pause -->

- **scripts**: Arquivos Python executáveis
- **project.scripts**: Entry points principais
- **console_scripts**: Entry points específicos

Build System e Empacotamento
===

```toml
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[tool.setuptools.packages.find]
where = ["src"]

[tool.setuptools.package-data]
meu_cli = ["data/*.json", "templates/*.txt"]
```

<!-- pause -->

**MANIFEST.in** para arquivos extras:

```
include README.md
include LICENSE
recursive-include src/meu_cli/data *
recursive-include src/meu_cli/templates *
global-exclude *.pyc __pycache__
```

uv init --package
===

Criando projeto moderno com **uv**:

```bash +exec
uv init --package meu-cli
```

<!-- pause -->

Estrutura gerada:

```
meu-cli/
├── pyproject.toml
├── src/
│   └── meu_cli/
│       ├── __init__.py
│       └── py.typed
└── README.md
```

<!-- pause -->

**py.typed** indica suporte a type hints

uv run e uv tool install
===

<!-- column_layout: [1, 1] -->
<!-- column: 0 -->

**uv run** - Desenvolvimento:

```bash
# Executa durante desenvolvimento
uv run meu-cli --help

# Com dependências extras
uv run --extra dev meu-cli test

# Script específico
uv run python -m meu_cli
```

<!-- column: 1 -->

**uv tool install** - Instalação global:

```bash
# Instala globalmente
uv tool install meu-cli

# Instala de repositório
uv tool install git+https://github.com/user/meu-cli

# Instala versão específica
uv tool install meu-cli==1.2.3
```

ZipApps
===

Distribuição como arquivo único executável:

```python
import zipapp
import sys
from pathlib import Path

def create_zipapp():
    source = Path("src")
    target = Path("dist/meu-cli.pyz")
    
    zipapp.create_archive(
        source, 
        target,
        interpreter="/usr/bin/env python3",
        main="meu_cli.cli:main"
    )

if __name__ == "__main__":
    create_zipapp()
```

<!-- pause -->

```bash
chmod +x meu-cli.pyz
./meu-cli.pyz --help
```

Boas Práticas CLI (clig.dev)
===

**Princípios fundamentais:**

- **Human-first**: Interface clara e intuitiva
- **Simple**: Comportamento previsível
- **Consistent**: Padrões consistentes
- **Helpful**: Mensagens de erro úteis
- **Future-proof**: Extensível e versionado

<!-- pause -->

**Exemplos:**

```bash
# ✅ Bom
ft convert --from json --to yaml file.json

# ❌ Ruim  
ft -f json -t yaml file.json
```

Argumentos CLI: Conceitos
===

<!-- column_layout: [1, 1] -->
<!-- column: 0 -->

**Comando:**
```bash
ft convert file.json
```

**Subcomando:**
```bash
git commit -m "message"
docker run ubuntu
```

<!-- column: 1 -->

**Opção (com valor):**
```bash
ft --format json
ft --output result.yaml
```

**Flag (booleana):**
```bash
ft --verbose
ft --help
```

Argparse Básico
===

```python
import argparse

def main():
    parser = argparse.ArgumentParser(
        description="File Tool - Canivete suíço para arquivos"
    )
    
    parser.add_argument('filename', help='Arquivo para processar')
    parser.add_argument('--format', '-f', 
                       choices=['json', 'yaml', 'csv'],
                       help='Formato do arquivo')
    parser.add_argument('--verbose', '-v', 
                       action='store_true',
                       help='Saída detalhada')
    
    args = parser.parse_args()
    print(f"Processando {args.filename} como {args.format}")
    
if __name__ == "__main__":
    main()
```

Subcomandos com Argparse
===

```python
def create_parser():
    parser = argparse.ArgumentParser(description='File Tool')
    subparsers = parser.add_subparsers(dest='command', help='Comandos disponíveis')
    
    # Subcomando convert
    convert_parser = subparsers.add_parser('convert', help='Converte entre formatos')
    convert_parser.add_argument('--from', dest='input_format', required=True)
    convert_parser.add_argument('--to', dest='output_format', required=True)
    convert_parser.add_argument('input_file', help='Arquivo de entrada')
    
    # Subcomando detect-encoding
    detect_parser = subparsers.add_parser('detect-encoding', help='Detecta encoding')
    detect_parser.add_argument('file', help='Arquivo para analisar')
    
    return parser

def main():
    parser = create_parser()
    args = parser.parse_args()
    
    if args.command == 'convert':
        convert_file(args.input_file, args.input_format, args.output_format)
    elif args.command == 'detect-encoding':
        detect_encoding(args.file)
```

Projeto Prático: ft (File Tool)
===

**Funcionalidades principais:**

```bash
ft convert --from json --to yaml file.json
ft convert --from csv --to json data.csv
ft detect-encoding mysterious_file.txt
```

<!-- pause -->

**Funcionalidade extra (se der tempo):**

```bash
ft convert --from json --to yaml --watch source/ dest/
```

<!-- pause -->

Baseado no conhecimento da **Semana 05 - Serialização/Deserialização**

Estrutura do Projeto ft
===

```
ft/
├── pyproject.toml
├── src/
│   └── ft/
│       ├── __init__.py
│       ├── __main__.py
│       ├── cli.py
│       ├── converters/
│       │   ├── __init__.py
│       │   ├── json_converter.py
│       │   ├── yaml_converter.py
│       │   └── csv_converter.py
│       ├── detectors/
│       │   ├── __init__.py
│       │   └── encoding_detector.py
│       └── utils.py
├── exemplos/
└── tests/
```

Demonstração Prática
===

<!-- font_size: 2 -->

Vamos implementar o projeto **ft** passo a passo:

1. **Setup inicial** com `uv init --package`
2. **Estrutura** de módulos
3. **CLI** com argparse e subcomandos  
4. **Conversores** para diferentes formatos
5. **Detector** de encoding
6. **Testes** básicos

<!-- pause -->

**Mãos à obra!** 🚀

Exemplos Práticos
===

Na pasta **exemplos/** veremos:

- **app_com_docstring** - Documentação adequada
- **app_com_multiplos_scripts** - Vários entry points
- **app_com_argparser** - CLI básico
- **app_com_subcomandos** - CLI complexo
- **zipapp_builder** - Criação de ZipApps
- **monitor_tool** - Exemplo completo

<!-- pause -->

Cada exemplo contém **TODO:** com desafios para implementar!

Desafios para os Alunos
===

**TODOs incluídos nos exemplos:**

- Melhorar tratamento de erros
- Adicionar validação de entrada
- Implementar logs estruturados
- Adicionar testes unitários
- Melhorar mensagens de ajuda
- Implementar configuração via arquivo
- Adicionar suporte a plugins

<!-- pause -->

**Objetivo:** Aprender fazendo e explorando!

Recursos Adicionais
===

**Referências importantes:**

- **clig.dev** - Command Line Interface Guidelines
- **argparse** - Documentação oficial Python
- **uv** - Ferramenta moderna de packaging
- **zipapp** - Distribuição como executável único

<!-- pause -->

**Próximos passos:**
- Implementar projeto ft
- Explorar exemplos
- Resolver desafios
- Criar seus próprios CLIs!

Conclusão
===

<!-- alignment: center -->

**"A melhor interface de linha de comando é aquela que você não precisa pensar para usar."**

-- Filosofia clig.dev

<!-- pause -->

**Obrigado!** 

Bruno Rocha - LINUXtips
