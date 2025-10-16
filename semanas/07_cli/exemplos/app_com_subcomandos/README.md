# App com Subcomandos - Exemplo Avançado de CLI

Este exemplo demonstra como criar uma aplicação CLI complexa com múltiplos subcomandos, similar a ferramentas como `git`, `docker`, ou `kubectl`.

## Estrutura de Comandos

```
myapp <comando_global> <subcomando> <argumentos>

Exemplos:
myapp file list --recursive /home/user
myapp file copy arquivo.txt backup.txt --force
myapp config set editor vim
myapp config get editor
```

## Comandos Disponíveis

### 1. Grupo `file` - Operações com Arquivos

#### `file list` - Lista arquivos e diretórios
```bash
python cli.py file list                    # Lista diretório atual
python cli.py file list /home/user         # Lista diretório específico
python cli.py file list --recursive        # Lista recursivamente
python cli.py file list --hidden          # Inclui arquivos ocultos
python cli.py file list --json            # Saída em JSON
```

#### `file copy` - Copia arquivos
```bash
python cli.py file copy origem.txt destino.txt
python cli.py file copy arquivo.txt backup.txt --force
```

#### `file delete` - Remove arquivos
```bash
python cli.py file delete arquivo.txt
python cli.py file delete arquivo.txt --force  # Sem confirmação
```

### 2. Grupo `config` - Gerenciamento de Configuração

#### `config get` - Obtém configurações
```bash
python cli.py config get                  # Lista todas
python cli.py config get editor          # Obtém configuração específica
```

#### `config set` - Define configurações
```bash
python cli.py config set editor vim
python cli.py config set theme dark
python cli.py config set max_files 1000
```

#### `config list` - Lista todas as configurações
```bash
python cli.py config list
python cli.py config list --json
```

#### `config delete` - Remove configurações
```bash
python cli.py config delete editor
```

## Argumentos Globais

Estes argumentos funcionam com qualquer comando:

- `--verbose, -v`: Saída detalhada
- `--quiet, -q`: Suprime saída não-essencial
- `--version`: Mostra versão da aplicação

```bash
python cli.py --verbose file list
python cli.py --quiet config set theme dark
```

## Estrutura do Código

```python
def create_main_parser():
    # Parser principal com argumentos globais
    
def create_file_subparser(subparsers):
    # Subparsers para comandos de arquivo
    
def create_config_subparser(subparsers):
    # Subparsers para comandos de configuração
    
def execute_file_commands(args):
    # Lógica para comandos de arquivo
    
def execute_config_commands(args):
    # Lógica para comandos de configuração
```

## Conceitos Demonstrados

### 1. **Hierarquia de Subcomandos**
```
aplicação
├── file
│   ├── list
│   ├── copy
│   └── delete
└── config
    ├── get
    ├── set
    ├── list
    └── delete
```

### 2. **Argumentos Específicos por Subcomando**
Cada subcomando pode ter seus próprios argumentos únicos:
- `file list` tem `--recursive` e `--hidden`
- `file copy` tem `--force`
- `config list` tem `--json`

### 3. **Classes para Organização**
- `FileManager`: Encapsula operações com arquivos
- `ConfigManager`: Gerencia configurações persistentes

### 4. **Validação e Tratamento de Erros**
- Validação de arquivos existentes
- Tratamento de erros específicos por operação
- Códigos de saída apropriados

### 5. **Configuração Persistente**
- Armazena configurações em `~/.myapp/config.json`
- CRUD completo para configurações

## Casos de Uso Práticos

### Backup de Arquivos com Configuração
```bash
# Configurar diretório de backup
python cli.py config set backup_dir /backup

# Copiar arquivo para backup
python cli.py file copy importante.txt /backup/importante.txt

# Verificar configuração
python cli.py config get backup_dir
```

### Limpeza com Confirmação
```bash
# Remove com confirmação interativa
python cli.py file delete temp.txt

# Remove sem confirmação
python cli.py file delete temp.txt --force
```

### Auditoria de Sistema
```bash
# Lista todos os arquivos recursivamente em JSON
python cli.py file list --recursive --hidden --json > system_files.json

# Salva configurações atuais
python cli.py config list --json > current_config.json
```

## TODOs para Extensão

### Funcionalidades de Arquivo
- [ ] Comando `file move` para mover arquivos
- [ ] Comando `file mkdir` para criar diretórios
- [ ] Filtros por extensão em `file list`
- [ ] Barra de progresso para operações longas
- [ ] Operações em lote para múltiplos arquivos

### Funcionalidades de Configuração
- [ ] Suporte a configurações hierárquicas (global/projeto/local)
- [ ] Import/export de configurações
- [ ] Validação de tipos e valores de configuração
- [ ] Configurações por ambiente (dev/staging/prod)
- [ ] Backup automático de configurações

### Melhorias Gerais
- [ ] Sistema de plugins para subcomandos dinâmicos
- [ ] Autocompletion para bash/zsh
- [ ] Testes unitários para cada subcomando
- [ ] Documentação interativa (`myapp help`)
- [ ] Logs estruturados com diferentes níveis
- [ ] Context managers para cleanup de recursos

## Executando o Exemplo

```bash
# Torna o script executável
chmod +x cli.py

# Testa comandos básicos
./cli.py --help
./cli.py file --help
./cli.py config --help

# Executa operações
./cli.py file list
./cli.py config set test_key test_value
./cli.py config get test_key
```

Este exemplo serve como base para criar CLIs complexos e extensíveis em Python, demonstrando padrões profissionais de desenvolvimento de ferramentas de linha de comando.