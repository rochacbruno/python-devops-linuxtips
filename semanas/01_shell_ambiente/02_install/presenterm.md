---
title: Instalação do Python
sub_title: Múltiplas versões sem conflitos
author: Python para DevOps
options:
  implicit_slide_ends: true
  end_slide_shorthand: true
  incremental_lists: true
---

O Problema
===

Você gerencia 3 aplicações:

* **App A**: Python 3.8 (legado)
* **App B**: Python 3.11 (produção)  
* **App C**: Python 3.12 (novo projeto)

<!-- pause -->

Como fazer isso sem quebrar o sistema?

<!-- pause -->

```
$ python3 --version
Python 3.6.9  # 😱 Sistema antigo!
```

<!-- end_slide -->

Por que não usar o Python do sistema?
===

<!-- incremental_lists: true -->

* Versão antiga e fixa
* Dependências do OS podem quebrar
* Um `pip install` errado = sistema morto
* Sem flexibilidade para projetos

<!-- pause -->

```bash
# NUNCA faça isso!
sudo pip install requests  # 🚫
```

<!-- end_slide -->

Opção 1: Gerenciador de Pacotes
===

```bash
# Ubuntu/Debian
apt install python3

# RedHat/Fedora  
dnf install python3
```

<!-- pause -->

**✅ Prós:**
* Simples e rápido
* Integrado ao sistema

<!-- pause -->

**❌ Contras:**
* Uma versão só
* Risco ao sistema
* Versão da distro

<!-- end_slide -->

Opção 2: Compilar do Fonte
===

```bash
# Baixar e compilar
wget https://www.python.org/ftp/python/3.12.0/Python-3.12.0.tgz
tar -xf Python-3.12.0.tgz
cd Python-3.12.0

./configure --enable-optimizations
make -j $(nproc)
```

<!-- pause -->

## ⚠️ IMPORTANTE: make altinstall

```bash
# ERRADO: sobrescreve python3
make install  # 🚫

# CERTO: cria python3.12
make altinstall  # ✅
```

<!-- end_slide -->

Por que make altinstall?
===

<!-- column_layout: [1, 1] -->

<!-- column: 0 -->

### make install 🚫

```
/usr/bin/python3 → 3.12
```

* Sobrescreve sistema
* Quebra ferramentas
* apt/yum param de funcionar

<!-- column: 1 -->

### make altinstall ✅

```
/usr/bin/python3     → 3.6
/usr/bin/python3.12  → 3.12
```

* Versões coexistem
* Sistema seguro
* Escolha manual

<!-- end_slide -->

<!-- jump_to_middle -->

A Solução Moderna: UV
===

<!-- end_slide -->

UV: Instalação
===

```bash
# Uma linha só!
curl -LsSf https://astral.sh/uv/install.sh | sh
```

<!-- pause -->

**Configurando autocompletion:**

```bash
# Bash
echo 'eval "$(uv generate-shell-completion bash)"' >> ~/.bashrc

# Zsh
echo 'eval "$(uv generate-shell-completion zsh)"' >> ~/.zshrc

# Fish
uv generate-shell-completion fish | source
```

<!-- end_slide -->

UV: Gerenciando Pythons
===

```bash
# Listar versões disponíveis
uv python list

# Instalar versões
uv python install 3.12
uv python install 3.11
uv python install 3.10

# Ver instaladas
uv python list --only-installed
```

<!-- pause -->

**Onde ficam?**
```
~/.local/share/uv/python/
├── cpython-3.10*/
├── cpython-3.11*/
└── cpython-3.12*/
```

<!-- end_slide -->

UV: Definindo versão por projeto
===

```bash
cd meu-projeto/

# Define Python 3.12 para este diretório
uv python pin 3.12

# Cria arquivo .python-version
cat .python-version
# 3.12
```

<!-- pause -->

**No pyproject.toml:**
```toml
[project]
name = "meu-projeto"
requires-python = ">=3.11"

[tool.uv]
python-preference = "managed"
```

<!-- end_slide -->

UV: O segredo do isolamento
===

O UV **não** coloca Python no PATH!

```bash
# Isso NÃO funciona
python --version  # ❌ Command not found

# Sempre use uv run
uv run python --version  # ✅ Python 3.12.0
```

<!-- pause -->

**Exemplos práticos:**
```bash
uv run python script.py
uv run pip install pandas
uv run pytest
uv run jupyter lab
```

<!-- end_slide -->

Demonstração Prática
===

<!-- column_layout: [1, 1] -->

<!-- column: 0 -->

**Projeto Legado**
```bash
cd projeto-legado/
uv python pin 3.8
uv run python --version
# Python 3.8.18
```

<!-- column: 1 -->

**Projeto Novo**
```bash
cd projeto-novo/
uv python pin 3.12  
uv run python --version
# Python 3.12.0
```

<!-- reset_layout -->

<!-- pause -->

Cada projeto usa sua versão, sem conflitos! 🎉

<!-- end_slide -->

Comparação Final
===

| Método | Quando usar |
|--------|-------------|
| **apt/dnf** | Desenvolvimento casual |
| **Compilar** | Controle total, otimizações |
| **UV** | ⭐ DevOps, múltiplos projetos |

<!-- pause -->

## Por que UV para DevOps?

<!-- incremental_lists: true -->

* Múltiplas versões sem conflito
* Reprodutibilidade garantida  
* CI/CD simplificado
* Zero risco ao sistema

<!-- end_slide -->

Exemplo: CI/CD com UV
===

```yaml
# .github/workflows/test.yml
name: Tests
on: [push]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Instalar UV
        run: curl -LsSf https://astral.sh/uv/install.sh | sh
        
      - name: Executar testes
        run: |
          uv python install
          uv run pytest
```

<!-- pause -->

Simples, rápido e confiável! 🚀

<!-- end_slide -->

<!-- jump_to_middle -->

Conclusão
===

`uv run` não é um bug, é uma **feature**!

<!-- pause -->

Garante isolamento total entre projetos

<!-- end_slide -->

Próximos Passos
===

1. **Instale o UV** em seu ambiente
2. **Experimente** com um projeto teste
3. **Migre** projetos gradualmente
4. **Padronize** no time

<!-- pause -->

## Recursos

* Documentação UV: https://docs.astral.sh/uv/
* Python.org: https://www.python.org/
* Este curso: Python para DevOps

<!-- end_slide -->

<!-- jump_to_middle -->

Dúvidas?
===

Vamos praticar! 💪