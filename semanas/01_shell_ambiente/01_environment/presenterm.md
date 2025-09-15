---
title: O Ambiente de Execução Python
sub_title: Entendendo variáveis de ambiente e PATH
author: Python para DevOps
options:
  implicit_slide_ends: true
  end_slide_shorthand: true
  incremental_lists: true
# theme:
#   name: light
---

O Problema
===

<!-- pause -->

<!-- font_size: 2 -->
<!-- alignment: center -->

"Por que meu script funciona na minha máquina mas não no servidor?"

<!-- pause -->
<!-- font_size: 1 -->
```bash
# Na sua máquina
$ python meu_script.py
✓ Script executado com sucesso!

# No servidor
$ python meu_script.py
ModuleNotFoundError: No module named 'requests'
```

<!-- pause -->

<!-- alignment: center -->
Ou ainda pior...

```bash
# Na sua máquina
$ python processar_logs.py
Processando logs em português...

# No servidor  
$ python processar_logs.py
Processing logs in English...
```

<!-- end_slide -->

O que é "Ambiente"?
===

<!-- font_size: 2 -->
No contexto de execução de programas, o ambiente é o conjunto de configurações que determinam como um programa vai se comportar.

<!-- pause -->

<!-- column_layout: [1, 1] -->

<!-- column: 0 -->

```
Terminal 1
    ↓
Shell/Ambiente 1
    ↓
Variáveis 1
    ↓
Python Process 1
```

<!-- column: 1 -->

```
Terminal 2
    ↓
Shell/Ambiente 2
    ↓
Variáveis 2
    ↓
Python Process 2
```

<!-- reset_layout -->

<!-- pause -->
<!-- alignment: center -->
**Cada sessão é isolada!**

<!-- end_slide -->

Variáveis de Ambiente
===
<!-- font_size: 2 -->
As variáveis de ambiente controlam:

* Onde encontrar executáveis (`PATH`)
* Qual idioma usar (`LANG`, `LC_ALL`)
* Configurações do Python (`PYTHONPATH`, `PYTHONVERBOSE`)
* Credenciais (`AWS_ACCESS_KEY`, `API_TOKEN`)

<!-- alignment: center -->

## Verificando o ambiente

```bash
$ env | head -5
USER=usuario
HOME=/home/usuario
PATH=/usr/local/bin:/usr/bin:/bin
SHELL=/bin/bash
TERM=xterm-256color
```

<!-- end_slide -->

PATH: A Variável Mais Importante
===

<!-- font_size: 2 -->

## O problema do "command not found"

<!-- pause -->

```bash
$ python3.12
bash: python3.12: command not found

$ /usr/local/bin/python3.12
Python 3.12.0 (main, Oct  2 2023, 00:00:00)
>>>
```

<!-- pause -->

Por que o primeiro falha mas o segundo funciona?

<!-- pause -->

**A resposta está no PATH!**

<!-- end_slide -->

Como o Shell Encontra Executáveis
===

<!-- font_size: 2 -->
Quando você digita `python`:

1. **É caminho absoluto?** → Executa diretamente
2. **Não?** → Consulta o PATH:
   - `/usr/local/bin/python` existe? → Executa!
   - `/usr/bin/python` existe? → Executa!
   - `/bin/python` existe? → Executa!
3. **Não encontrou?** → `command not found`


**O shell para na primeira ocorrência!**

<!-- end_slide -->

Anatomia do PATH
===

<!-- pause -->
<!-- font_size: 2 -->
```bash
$ echo $PATH
/home/user/.local/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin
```
<!-- alignment: center -->
<!-- pause -->

Separando por linhas:

```bash
$ echo $PATH | tr ':' '\n'
/home/user/.local/bin
/usr/local/bin
/usr/bin
/bin
/usr/sbin
/sbin
```

<!-- pause -->

**A ordem importa!** Primeiro diretório tem prioridade.

<!-- end_slide -->

Descobrindo Executáveis
===
<!-- alignment: center -->
<!-- pause -->
## Qual executável será usado se eu tiver muitos?
<!-- pause -->
<!-- font_size: 2 -->
```bash
$ which python3
/usr/bin/python3
```
<!-- font_size: 1 -->

<!-- pause -->

## Mostrando TODAS as ocorrências

```bash
$ which -a python3
/usr/bin/python3
/usr/local/bin/python3
/home/user/.local/bin/python3
```

<!-- pause -->

## Informações detalhadas

```bash
$ type python3
python3 is /usr/bin/python3

$ ls -la /usr/bin/python3
lrwxrwxrwx 1 root root 9 Mar 13  2023 /usr/bin/python3 -> python3.9
```

<!-- end_slide -->

Demonstração: Isolamento de Ambientes
===
<!-- pause -->
<!-- column_layout: [1, 1] -->

<!-- column: 0 -->

## Terminal 1

```bash +exec
export AMBIENTE="producao"
echo "AMBIENTE: $AMBIENTE"
# AMBIENTE: producao

export API_KEY="chave-producao"
echo "API_KEY: $API_KEY"
# API_KEY: chave-producao
```

<!-- column: 1 -->

<!-- pause -->

## Terminal 2

```bash +exec
echo "AMBIENTE: $AMBIENTE"
# AMBIENTE:

echo "API_KEY: $API_KEY"
# API_KEY:
```

<!-- reset_layout -->

<!-- pause -->
<!-- font_size: 2 -->
<!-- alignment: center -->
**Cada sessão tem suas próprias variáveis!**

<!-- end_slide -->

Python e Variáveis de Ambiente
===
<!-- alignment: center -->
## Lendo variáveis com segurança

```python +exec
import os

# Método seguro - retorna None se não existir
api_key = os.getenv('API_KEY')
print(f"API_KEY: {api_key}")  # API_KEY: None

# Com valor padrão
ambiente = os.getenv('AMBIENTE', 'desenvolvimento')
print(f"AMBIENTE: {ambiente}")  # AMBIENTE: desenvolvimento

# Acessar diretamente (cuidado!)
# database_url = os.environ['DATABASE_URL']  # KeyError se não existir!
```

-----
<!-- alignment: center -->
## Listando todas as variáveis

```python +exec
# Ver todas as variáveis
/// import os
/// os.environ["PYTHON_PATH"] = "/tmp"
/// os.environ["PYTHON_BREAKPOINT"] = "pdb.set_trace"
/// os.environ["PYTHON_VERBOSE"] = "1"
for key, value in os.environ.items():
    if key.startswith('PYTHON'):
        print(f"{key}={value}")
```

<!-- end_slide -->

O Problema da Persistência
===

```python +exec
# alterar_ambiente.py
import os

# Definindo uma variável
os.environ['NOVA_VAR'] = 'valor_temporario'
print(f"Dentro do Python: {os.environ['NOVA_VAR']}")
# Output: Dentro do Python: valor_temporario
```

<!-- pause -->
<!-- alignment: center -->
Executando e verificando:

```bash +exec
# $ python alterar_ambiente.py
# Dentro do Python: valor_temporario

echo $NOVA_VAR 
# (vazio)
```

<!-- pause -->

**A mudança não persiste!**

<!-- end_slide -->

Por Que Não Persiste?
===

<!-- column_layout: [1, 2] -->

<!-- column: 0 -->

```
Shell (Parent)
PID: 1234
 ↓ cria
Python (Child)
PID: 5678
 ↓ modifica
os.environ
 ↓ termina
Mudanças perdidas!
```

<!-- column: 1 -->

**Regra do Sistema Operacional:**

Processos filhos não podem modificar o ambiente do pai!

É uma proteção de segurança.

<!-- reset_layout -->

<!-- end_slide -->

Solução: Configuração Explícita
===

<!-- column_layout: [1, 1] -->

<!-- column: 0 -->

## `.env.development`

```bash
DATABASE_URL=sqlite:///dev.db
DEBUG=true
API_ENDPOINT=http://localhost:8000
LOG_LEVEL=DEBUG
```

<!-- column: 1 -->

## `.env.production`

```bash
DATABASE_URL=postgresql://prod/db
DEBUG=false
API_ENDPOINT=https://api.prod.com
LOG_LEVEL=ERROR
```

<!-- reset_layout -->

<!-- end_slide -->

Carregando Configurações
===

<!-- alignment: center -->
Just Python

```python +line_numbers
import os
from pathlib import Path

# Detecta o ambiente
ambiente = os.getenv('AMBIENTE', 'development')

# Carrega o arquivo correto
env_file = Path(f'.env.{ambiente}')

if env_file.exists():
    with open(env_file) as f:
        for linha in f:
            linha = linha.strip()
            if '=' in linha and not linha.startswith('#'):
                key, value = linha.split('=', 1)
                os.environ[key] = value
                
print(f"Ambiente {ambiente} carregado!")
```

<!-- pause -->

Biblioteca

```python
from dynaconf import Dynaconf
settings = Dynaconf(load_dotenv=True)
```

<!-- end_slide -->

<!-- alignment: center -->
Boas Práticas para DevOps
===
<!-- pause -->
## 1. Documente SEMPRE

```markdown
## Variáveis de Ambiente Necessárias

- `DATABASE_URL`: URL de conexão com o banco
- `API_KEY`: Chave de API (obrigatória em produção)
- `LOG_LEVEL`: Nível de log (default: INFO)
- `WORKERS`: Número de workers (default: 4)
```

<!-- pause -->

## 2. Use valores padrão sensatos

```python
log_level = os.getenv('LOG_LEVEL', 'INFO')
timeout = int(os.getenv('TIMEOUT', '30'))
workers = int(os.getenv('WORKERS', '4'))
debug = os.getenv('DEBUG', 'false').lower() == 'true'
```

<!-- end_slide -->

Validação de Ambiente
===
<!-- pause -->
<!-- alignment: center -->
## Valide cedo, falhe rápido!

```python
# validate_env.py
import os
import sys

required_vars = ['DATABASE_URL', 'API_KEY']
missing = []

for var in required_vars:
    if not os.getenv(var):
        missing.append(var)

if missing:
    print("❌ ERRO: Variáveis obrigatórias não definidas:")
    for var in missing:
        print(f"   - {var}")
    sys.exit(1)
    
print("✅ Ambiente validado com sucesso!")
```
<!-- pause -->
```python
from dynaconf import Validator
settings = Dynaconf(
    validators=[
        Validator("DATABASE_URL", required=True),
        Validator("API_KEY", required=True),
    ]
)
```

<!-- end_slide -->

Script de Diagnóstico
===
<!-- pause -->

```python +line_numbers +exec
# diagnostico.py
import os
import sys
print("=== DIAGNÓSTICO DE AMBIENTE ===\n")
print("Python:")
print(f"  Versão: {sys.version.split()[0]}")
print(sys.executable)
print("\nPATH (primeiros 2 diretórios):")
paths = os.environ.get('PATH', '').split(':')
for i, p in enumerate(paths[:2], 1):
    exists = "✓" if os.path.exists(p) else "✗"
    print(f"  {i}. [{exists}] {p}")
print(f"\nTotal de variáveis de ambiente: {len(os.environ)}")
# Variáveis USER_
print("\nVariáveis USER*:")
for key in sorted(os.environ.keys()):
    if key.startswith('USER'):
        print(f"  {key}={os.environ[key]}")
```

<!-- end_slide -->

Exercício Prático
===

<!-- pause -->
<!-- alignment: center -->
Crie o arquivo `ambiente_demo.py`:

```python
#!/usr/bin/env python3
import os

def main():
    print("=== Demonstração de Ambiente ===")

    # Mostra PID para provar isolamento
    print(f"Processo ID: {os.getpid()}")
    
    # Variáveis importantes
    for var in ['USER', 'PATH', 'CUSTOM_VAR']:
        valor = os.getenv(var, 'NÃO DEFINIDA')
        if var == 'PATH':
            # Mostra apenas quantidade de diretórios
            valor = f"{len(valor.split(':'))} diretórios"
        print(f"{var}: {valor}")
    
    # Tenta modificar
    os.environ['TESTE'] = 'temporario'
    print(f"\nTESTE definida como: {os.environ['TESTE']}")
    print("(mas não persistirá após o script terminar)")

if __name__ == "__main__":
    main()
    print()
```
```bash +exec
# Permissão para executar
chmod +x ambiente_demo.py
```

<!-- end_slide -->

Testando o Isolamento
===

<!-- pause -->
<!-- alignment: center -->
Execute em diferentes contextos:

<!-- column_layout: [1, 1] -->

<!-- column: 0 -->

```bash
# Teste 1: Execução normal
$ python ambiente_demo.py

# Teste 2: Com variável temporária
$ CUSTOM_VAR=temporaria python ambiente_demo.py

# Teste 3: Com export
$ export CUSTOM_VAR=persistente
$ ./ambiente_demo.py
$ echo "CUSTOM_VAR: $CUSTOM_VAR"  # ainda existe!

# Teste 4: Verificar que mudanças não persistem
$ python -c "import os; os.environ['NOVA']='teste'"
$ echo "NOVA: $NOVA"  # vazio!
```

<!-- column: 1 -->


```bash +exec
/// chmod +x ambiente_demo.py
/// python ambiente_demo.py
/// CUSTOM_VAR=temporaria python ambiente_demo.py
/// export CUSTOM_VAR=persistente
/// ./ambiente_demo.py
/// echo "CUSTOM_VAR: $CUSTOM_VAR"  # ainda existe!
/// python -c "import os; os.environ['NOVA']='teste'"
/// echo "NOVA: $NOVA"  # vazio!
```

<!-- reset_layout -->

<!-- end_slide -->


<!-- alignment: center -->

Conclusão
===

<!-- font_size: 2 -->

- **O ambiente determina o comportamento**
- **Cada sessão é isolada**
- **PATH controla onde encontrar executáveis**
- **Python lê mas não persiste mudanças**
- **Documente e valide sempre!**

-------

Principais Aprendizados
===


<!-- font_size: 2 -->

1. Variáveis de ambiente são configurações temporárias da sessão

2. PATH determina a ordem de busca por executáveis

3. Processos filhos herdam mas não modificam o ambiente do pai

4. Ambientes virtuais funcionam modificando o PATH

5. Use arquivos `.env` para configurações por ambiente

6. Sempre valide variáveis obrigatórias no início

<!-- end_slide -->

<!-- jump_to_middle -->

Próxima Aula
===

## Instalação e Gerenciamento do Python

<!-- pause -->

* Diferentes formas de instalar Python
* Gerenciando múltiplas versões
* Python Site e ambientes virtuais
* Ferramentas modernas: UV, pyenv, asdf

<!-- pause -->

**Até a próxima!**