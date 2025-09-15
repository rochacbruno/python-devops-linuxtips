---
title: "O Interpretador **Python**"
sub_title: Python para DevOps
author: Bruno Rocha
options:
  implicit_slide_ends: true
  end_slide_shorthand: true
  incremental_lists: true
---

O Problema
===

<!-- alignment: center -->

<!-- pause -->

Você recebe um script Python para automatizar deploys...

<!-- pause -->

```bash
$ ./deploy.py
bash: ./deploy.py: Permission denied
```

<!-- pause -->

```bash
$ chmod +x deploy.py
$ ./deploy.py
bash: ./deploy.py: /usr/bin/python: bad interpreter
```

<!-- pause -->

🤔 **O que está acontecendo?**



Ambiente de Testes
===

<!-- alignment: center -->
Para todos os exemplos, usaremos Docker:

```bash
$ docker run -it --rm ubuntu:latest bash

# Dentro do container
root@9f546e4433b2:/# apt update && apt install -y python3 python3-pip vim
```

<!-- pause -->

✅ Ambiente limpo e reproduzível!



O que é o Interpretador?
===

<!-- alignment: center --> 
<!-- font_size: 2 -->

* Lê código Python
* Executa instruções
* Retorna resultados




REPL - Modo Interativo
===

```mermaid +render
graph LR
    A[Read] --> B[Eval]
    B --> C[Print]
    C --> D[Loop]
    D --> A
    
    style A fill:#f9f,stroke:#333,color:#000
    style B fill:#9f9,stroke:#333,color:#000
    style C fill:#99f,stroke:#333,color:#000
    style D fill:#ff9,stroke:#333,color:#000
```

<!-- pause -->

<!-- alignment: center -->
**Problema**: Testar se uma biblioteca está instalada

<!-- pause -->

```python
$ python3
>>> import requests
>>> requests.__version__
'2.31.0'
>>> exit()
```
<!-- pause -->

✨ **Perfeito para testes rápidos!**



Modos de Execução
===

<!-- font_size: 2 -->

<!-- pause -->

## 1️⃣ Modo Script (Arquivo)

<!-- pause -->

## 2️⃣ Modo Comando (-c)

<!-- pause -->

## 3️⃣ Modo Módulo (-m)

<!-- pause -->

## 4️⃣ Modo Interativo + Script (-i)



1 Modo Script
===

**Problema**: Script de monitoramento periódico

<!-- pause -->

```bash
cat > monitor.py << 'EOF'
#!/usr/bin/env python3
import psutil
import datetime

print(f"[{datetime.datetime.now()}] CPU: {psutil.cpu_percent()}%")
EOF
```

<!-- pause -->

```bash
python3 monitor.py
# [2024-01-20 10:30:45] CPU: 23.5%
```



2 Modo Comando (-c)
===

**Problema**: Verificar porta em pipeline bash

<!-- pause -->

```bash
# Verificar se porta 8080 está livre
python3 -c "import socket; s=socket.socket(); print(s.connect_ex(('localhost', 8080)) != 0)"
```

<!-- pause -->

```bash
# Em script bash
if python3 -c "import sys; sys.exit(0 if sys.version_info >= (3,8) else 1)"; then
    echo "Python 3.8+ ✓"
fi
```



3 Modo Módulo (-m)
===

**Problema**: Executar ferramenta complexa

<!-- pause -->

```bash
mkdir -p mytools
echo "" > mytools/__init__.py
```

<!-- pause -->
<!-- alignment: center -->
💡 **Dunder = Double UNDERscore**

<!-- pause -->

`mytools/__main__.py`
```python
#!/usr/bin/env python3
"""Entry point - arquivo dunder main"""
print("🚀 Ferramenta DevOps iniciada!")
```

<!-- pause -->

```bash
python3 -m mytools
# 🚀 Ferramenta DevOps iniciada!
```



4 Modo Script Interativo (-i)
===

<!-- alignment: center -->

**Problema**: Script falhou, preciso debugar!

<!-- pause -->

```python
# debug_example.py
data = {"servers": ["web01", "web02", "db01"]}
failed_servers = []

for server in data["servers"]:
    if "db" in server:
        failed_servers.append(server)
```

<!-- pause -->

```bash
python3 -i debug_example.py
>>> failed_servers
['db01']
>>> data
{'servers': ['web01', 'web02', 'db01']}
```



Shebang
===


<!-- alignment: center -->
<!-- pause -->

❌ **Ruim** - Caminho hardcoded:
```bash
#!/usr/bin/python3
```

<!-- pause -->

✅ **Bom** - Usa o PATH:
```bash
#!/usr/bin/env python3
```

<!-- pause -->

⛑️ **permissão** de execução

```bash
chmod +x deploy_tool.py
./deploy_tool.py 
```

IPython: REPL Turbinado
===

<!-- column_layout: [1, 1] -->

<!-- column: 0 -->

**REPL Padrão**

* Básico
* Sem cores
* Sem autocomplete
* História limitada
* Melhorado no Python 3.13+

<!-- column: 1 -->

**IPython**

* Syntax highlighting
* Autocomplete (TAB)
* Comandos mágicos
* História avançada

<!-- reset_layout -->

<!-- pause -->

```bash
apt install python3-ipython
```

```python
$ python3 -m IPython
In [1]: import requests
In [2]: requests.get?  # Mostra documentação
In [3]: %timeit requests.get('http://example.com')
```

Exercício Prático
===

<!-- alignment: center -->

Criar ferramenta de monitoramento modular:

<!-- pause -->

```bash
monitor_tool/
├── __init__.py      # Torna importável
├── __main__.py      # Entry point
└── core.py          # Lógica principal (dica: psutil)
```

<!-- pause -->

```bash
# Executar como módulo
$ python3 -m monitor_tool
CPU: 23.5% MEM: 50% DISK: 70%

# Importar em outro script
from monitor_tool.core import check_cpu_usage
check_cpu_usage()
# 23.5%

# Debug interativo
$ python3 -i -m monitor_tool
>>> check_cpu_usage()
23.5%
```

Resumo
===

<!-- alignment: center -->
* **REPL**: Testes e exploração rápida
* **Script**: Automações do dia a dia
* **-c**: Integração com shell
* **-m**: Ferramentas complexas
* **-i**: Debug e troubleshooting

<!-- pause -->

<!-- jump_to_middle -->

**Escolha a ferramenta certa** 
**para cada problema!** 🎯


<!-- pause -->

## Debugging Eficiente

> Teremos uma aula para falar sobre debugging eficiente usando `pdb` e outras ferramentas.


---

<!-- font_size: 3 -->

_"O estudante avançado que pula partes que parecem elementares perde mais do que o iniciante que pula partes que parecem complexas."_

**George Pólya** 