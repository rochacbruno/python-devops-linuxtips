# Exemplos de CLI em Python

Esta pasta contém exemplos práticos demonstrando as melhores práticas para desenvolvimento de aplicações CLI em Python moderno.

## 📁 Estrutura dos Exemplos

### 1. `app_com_docstring.py`
**Foco:** Documentação adequada com docstrings

**Demonstra:**
- Docstrings no formato Google/Sphinx
- Type hints completos
- Documentação de erros e exemplos
- Estrutura de help contextual

**🚀 Desafios para implementar:**
- [ ] Implementar validação de formato de saída mais robusta
- [ ] Adicionar suporte para mais formatos (xml, csv)
- [ ] Melhorar tratamento de erros específicos por tipo
- [ ] Implementar sistema de logging com diferentes níveis
- [ ] Adicionar opção --quiet para suprimir saída
- [ ] Implementar opção --output para salvar em arquivo
- [ ] Adicionar captura de KeyboardInterrupt
- [ ] Implementar cleanup de recursos se necessário

### 2. `app_com_multiplos_scripts/`
**Foco:** Múltiplos entry points e scripts executáveis

**Demonstra:**
- Configuração de múltiplos scripts no pyproject.toml
- Organização modular com diferentes funcionalidades
- Interface unificada vs. scripts independentes
- Empacotamento com uv

**🚀 Desafios para implementar:**
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

### 3. `app_com_argparser.py`
**Foco:** Uso avançado do argparse

**Demonstra:**
- Argumentos posicionais, opcionais, flags
- Validação customizada de tipos
- Grupos mutuamente exclusivos
- Formatação de help avançada

**🚀 Desafios para implementar:**
- [ ] Implementar subparsers para comandos diferentes
- [ ] Implementar grupos de argumentos relacionados
- [ ] Adicionar argumentos de configuração via arquivo
- [ ] Implementar validações mais sofisticadas
- [ ] Adicionar validação cruzada entre argumentos
- [ ] Implementar sistema de logging com níveis
- [ ] Adicionar filtros de exclusão
- [ ] Implementar cache de resultados
- [ ] Adicionar signal handlers para cleanup
- [ ] Implementar context managers para recursos

### 4. `app_com_subcomandos/`
**Foco:** CLI complexo com subcomandos hierárquicos

**Demonstra:**
- Estrutura similar ao git/docker
- Subcomandos aninhados
- Argumentos específicos por subcomando
- Organização em classes

**🚀 Desafios para implementar:**

#### Funcionalidades de Arquivo
- [ ] Comando `file move` para mover arquivos
- [ ] Comando `file mkdir` para criar diretórios
- [ ] Filtros por extensão em `file list`
- [ ] Barra de progresso para operações longas
- [ ] Operações em lote para múltiplos arquivos

#### Funcionalidades de Configuração
- [ ] Suporte a configurações hierárquicas (global/projeto/local)
- [ ] Import/export de configurações
- [ ] Validação de tipos e valores de configuração
- [ ] Configurações por ambiente (dev/staging/prod)
- [ ] Backup automático de configurações

#### Melhorias Gerais
- [ ] Sistema de plugins para subcomandos dinâmicos
- [ ] Autocompletion para bash/zsh
- [ ] Testes unitários para cada subcomando
- [ ] Documentação interativa (`myapp help`)
- [ ] Logs estruturados com diferentes níveis
- [ ] Context managers para cleanup de recursos

### 5. `zipapp_builder.py`
**Foco:** Criação de ZipApps para distribuição

**Demonstra:**
- Criação de aplicações executáveis únicas
- Inclusão de dependências
- Scripts wrapper
- Validação de ZipApps

**🚀 Desafios para implementar:**
- [ ] Implementar cache de dependências para builds mais rápidos
- [ ] Adicionar suporte a wheels pré-compilados
- [ ] Usar uv ou pip-tools para instalação mais rápida
- [ ] Criar scripts para diferentes shells (bash, fish, zsh)
- [ ] Adicionar detecção automática do interpretador Python
- [ ] Implementar verificação de assinatura digital
- [ ] Verificar se todas as dependências estão incluídas
- [ ] Preservar permissões de arquivos
- [ ] Implementar extração seletiva de arquivos
- [ ] Adicionar subcomando para listar conteúdo sem extrair
- [ ] Implementar subcomando para atualizar ZipApp existente

### 6. `monitor_tool/`
**Foco:** Exemplo completo e profissional

**Demonstra:**
- Estrutura de projeto completa
- Configuração avançada
- Logging estruturado
- Empacotamento profissional

**🚀 Desafios para implementar:**
- [ ] Implementar métricas reais com psutil
- [ ] Adicionar métricas de rede, disco, processos
- [ ] Implementar logging estruturado com contexto
- [ ] Adicionar rotação de logs
- [ ] Implementar formatação mais precisa
- [ ] Usar rich para formatação mais bonita
- [ ] Implementar formatação com cores e tabelas
- [ ] Adicionar alertas baseados em thresholds
- [ ] Implementar salvamento de dados históricos
- [ ] Implementar sistema de logging baseado em verbosidade
- [ ] Adicionar context managers para recursos
- [ ] Adicionar signal handlers para cleanup graceful
- [ ] Implementar plugins para subcomandos dinâmicos

## 🎯 Desafios Gerais para Todos os Exemplos

### Qualidade de Código
- [ ] Adicionar testes unitários completos
- [ ] Implementar testes de integração
- [ ] Configurar linting com ruff/black
- [ ] Adicionar type checking com mypy
- [ ] Implementar coverage reports

### User Experience
- [ ] Criar autocompletion para bash/zsh/fish
- [ ] Implementar mensagens de erro mais informativas
- [ ] Adicionar modo interativo quando apropriado
- [ ] Implementar progress bars para operações longas
- [ ] Adicionar cores na saída quando disponível

### Configuração e Deployment
- [ ] Suporte a arquivos de configuração (YAML/TOML/JSON)
- [ ] Variáveis de ambiente para configuração
- [ ] Docker containers para distribuição
- [ ] GitHub Actions para CI/CD
- [ ] Documentação automática com Sphinx

### Performance e Observabilidade
- [ ] Implementar logging estruturado
- [ ] Adicionar métricas de performance
- [ ] Implementar cache inteligente
- [ ] Paralelização onde apropriado
- [ ] Otimização de memória para arquivos grandes

### Segurança
- [ ] Validação rigorosa de entrada
- [ ] Sanitização de paths de arquivo
- [ ] Tratamento seguro de credenciais
- [ ] Audit logs para operações sensíveis
- [ ] Rate limiting onde necessário

## 📚 Como Usar os Exemplos

1. **Estude o código:** Leia e entenda cada implementação
2. **Execute os exemplos:** Teste todas as funcionalidades
3. **Implemente os desafios:** Escolha TODOs que interessam
4. **Crie variações:** Adapte para suas necessidades
5. **Compartilhe:** Contribua com melhorias

## 🛠️ Setup para Desenvolvimento

```bash
# Para cada exemplo com pyproject.toml
cd exemplo_escolhido/
uv venv
uv pip install -e .

# Para scripts individuais
python exemplo.py --help
```

## 🎓 Objetivos de Aprendizado

Após completar os desafios, você deve estar apto a:

- ✅ Criar CLIs profissionais com argparse
- ✅ Organizar código de forma modular e testável
- ✅ Implementar documentação e help contextual
- ✅ Distribuir aplicações Python modernas
- ✅ Aplicar melhores práticas de desenvolvimento
- ✅ Criar interfaces intuitivas e robustas

## 🚀 Próximos Passos

1. Implemente pelo menos 3 TODOs de cada exemplo
2. Crie um projeto CLI próprio aplicando os conceitos
3. Contribua com melhorias para os exemplos
4. Explore bibliotecas avançadas como `click`, `typer`, `rich`

---

**Lembre-se:** O objetivo não é completar todos os TODOs, mas entender os conceitos e aplicá-los em seus próprios projetos! 🎯