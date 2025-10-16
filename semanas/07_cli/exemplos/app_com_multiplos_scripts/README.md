# Multi Tools - Exemplo de Múltiplos Scripts

Este exemplo demonstra como criar uma aplicação Python com múltiplos entry points e scripts executáveis independentes.

## Estrutura do Projeto

```
app_com_multiplos_scripts/
├── pyproject.toml          # Configuração do projeto com múltiplos entry points
├── src/
│   └── multi_tools/
│       ├── __init__.py     # Inicialização do pacote
│       ├── cli.py          # Interface unificada
│       ├── file_info.py    # Script para informações de arquivos
│       ├── text_processor.py # Script para processamento de texto
│       └── system_monitor.py # Script para monitoramento do sistema
└── README.md
```

## Scripts Disponíveis

### 1. file-info
Exibe informações detalhadas sobre arquivos:
```bash
file-info arquivo.txt
file-info --json documento.pdf
```

### 2. text-processor
Processa e analisa arquivos de texto:
```bash
text-processor arquivo.txt
text-processor --pattern "error" logs.txt
text-processor --case-insensitive --pattern "warning" app.log
```

### 3. system-monitor
Monitora informações do sistema:
```bash
system-monitor
system-monitor --json
system-monitor --continuous --interval 10
```

### 4. multi-tools (Interface Unificada)
Acesso a todas as ferramentas através de uma interface única:
```bash
multi-tools file-info arquivo.txt
multi-tools text-processor --pattern "test" arquivo.txt
multi-tools system-monitor --continuous
```

## Instalação e Uso

### Usando uv (recomendado)

```bash
# Instalar em modo desenvolvimento
uv pip install -e .

# Executar diretamente durante desenvolvimento
uv run file-info exemplo.txt
uv run multi-tools --help
```

### Usando pip tradicional

```bash
# Instalar em modo desenvolvimento
pip install -e .

# Os comandos ficam disponíveis globalmente
file-info exemplo.txt
text-processor arquivo.txt
system-monitor
multi-tools --help
```

## Entry Points Configurados

O arquivo `pyproject.toml` define os seguintes entry points:

```toml
[project.scripts]
file-info = "multi_tools.file_info:main"
text-processor = "multi_tools.text_processor:main"
system-monitor = "multi_tools.system_monitor:main"
multi-tools = "multi_tools.cli:main"
```

Isso permite que cada script seja executado independentemente como um comando do sistema.

## Conceitos Demonstrados

1. **Múltiplos Entry Points**: Cada funcionalidade pode ser um comando separado
2. **Interface Unificada**: Um comando principal que agrupa todas as funcionalidades
3. **Organização Modular**: Cada script é um módulo independente
4. **Documentação Consistente**: Todos os scripts seguem padrões de documentação
5. **Tratamento de Erros**: Cada script retorna códigos de saída apropriados

## TODOs para Implementação Completa

- [ ] Implementar sistema de plugins dinâmicos
- [ ] Adicionar configuração centralizada via arquivo
- [ ] Implementar logging estruturado
- [ ] Adicionar testes unitários para cada script
- [ ] Melhorar tratamento de erros específicos
- [ ] Implementar suporte a múltiplos arquivos
- [ ] Adicionar validação de entrada mais robusta
- [ ] Criar sistema de cache para operações caras
- [ ] Implementar paralelização para operações em lote
- [ ] Adicionar métricas de performance

## Dependências Opcionais

Para funcionalidades completas, considere adicionar:

```bash
# Para monitoramento avançado do sistema
uv pip install psutil

# Para processamento de texto avançado
uv pip install regex

# Para interfaces mais bonitas
uv pip install rich click

# Para configuração via arquivo
uv pip install pydantic pyyaml
```