# Questionário Final - Python para DevOps

Este questionário contém 2 questões de múltipla escolha para cada semana do curso.
Apenas **uma alternativa** está correta em cada questão.

---

## Semana 00 - Introdução

### Questão 1
Qual é o principal objetivo do curso "Python para DevOps"?

- a) Ensinar programação web com Django
- b) Ensinar Python aplicado a tarefas comuns de DevOps, automação e qualidade
- c) Preparar para certificação AWS
- d) Desenvolver aplicações mobile com Python

### Questão 2
Qual é a duração total do curso e a frequência das aulas ao vivo?

- a) 8 semanas com aulas diárias
- b) 16 semanas com aulas ao vivo a cada 2 semanas
- c) 12 semanas com aulas semanais
- d) 20 semanas com aulas mensais

---

## Semana 01 - Shell e Ambiente

### Questão 1
Qual ferramenta é recomendada no curso para gerenciamento de pacotes Python e ambientes virtuais?

- a) pip com virtualenv
- b) conda
- c) uv
- d) poetry

### Questão 2
Qual comando cria um ambiente virtual usando a ferramenta `uv`?

- a) `uv create venv`
- b) `uv virtualenv .venv`
- c) `uv venv`
- d) `uv init --venv`

---

## Semana 02 - Interpretador e I/O

### Questão 1
Qual é a forma correta de executar um módulo Python diretamente como script usando o interpretador?

- a) `python run meu_modulo`
- b) `python --exec meu_modulo`
- c) `python -m meu_modulo`
- d) `python start meu_modulo`

### Questão 2
Em Python, qual método é usado para ler todo o conteúdo de um arquivo de texto de uma vez?

- a) `file.readline()`
- b) `file.readlines()`
- c) `file.read()`
- d) `file.get_content()`

---

## Semana 03 - Protocolos

### Questão 1
Qual biblioteca Python é recomendada para fazer requisições HTTP assíncronas?

- a) urllib
- b) requests
- c) httpx
- d) socket

### Questão 2
Qual biblioteca Python é usada para automação SSH, incluindo execução de comandos remotos e transferência de arquivos via SFTP?

- a) ssh-python
- b) paramiko
- c) fabric
- d) sshlib

---

## Semana 04 - Segurança e Serviços

### Questão 1
Qual é a biblioteca padrão do Python usada para criar conexões SSL/TLS seguras?

- a) crypto
- b) ssl
- c) tls
- d) secure

### Questão 2
Ao gerar um SBOM (Software Bill of Materials) para segurança, qual ferramenta é mencionada no curso para scanning de vulnerabilidades?

- a) Bandit
- b) Safety
- c) Trivy
- d) SonarQube

---

## Semana 05 - Serialização/Deserialização (Serde)

### Questão 1
Qual encoding é recomendado como padrão para novos projetos Python, sendo compatível com ASCII e suportando todos os caracteres Unicode?

- a) Latin-1 (ISO-8859-1)
- b) ASCII
- c) UTF-8
- d) UTF-16

### Questão 2
Qual método do módulo `csv` retorna cada linha como um dicionário, usando o cabeçalho como chaves?

- a) `csv.reader()`
- b) `csv.DictReader()`
- c) `csv.dict_reader()`
- d) `csv.parse_dict()`

---

## Semana 06 - CLI (Interface de Linha de Comando)

### Questão 1
Qual módulo da biblioteca padrão do Python é usado para criar parsers de argumentos de linha de comando?

- a) optparse
- b) getopt
- c) argparse
- d) click

### Questão 2
No `pyproject.toml`, qual seção é usada para definir os entry points que criam comandos executáveis?

- a) `[project.commands]`
- b) `[tool.scripts]`
- c) `[project.scripts]`
- d) `[build.entrypoints]`

---

## Semana 07 - Typing e Validação

### Questão 1
Qual biblioteca Python é amplamente usada para validação de dados com suporte a type hints?

- a) marshmallow
- b) cerberus
- c) pydantic
- d) voluptuous

### Questão 2
No Pydantic, qual decorator é usado para criar validadores customizados para campos específicos?

- a) `@validator`
- b) `@field_validator`
- c) `@validate_field`
- d) `@check_field`

---

## Semana 08 - Configuração

### Questão 1
Qual é a ordem de precedência correta para fontes de configuração (da maior para menor prioridade)?

- a) Files → Envvars → CLI args → Defaults
- b) Defaults → Files → Envvars → CLI args
- c) CLI args → Envvars → Files → Defaults
- d) Envvars → CLI args → Files → Defaults

### Questão 2
Qual biblioteca Python é mencionada no curso para gerenciamento avançado de configurações com suporte a múltiplos loaders e validação?

- a) python-dotenv
- b) configparser
- c) dynaconf
- d) environs

---

## Semana 09 - Testes e Qualidade

### Questão 1
Qual tipo de teste verifica se a API mantém seu contrato (estrutura de request/response) entre versões?

- a) Unit test
- b) Integration test
- c) Contract test
- d) Load test

### Questão 2
Qual biblioteca Python é comumente usada para criar clientes HTTP síncronos e assíncronos para consumir APIs?

- a) requests
- b) urllib3
- c) httpx
- d) aiohttp

---

## Semana 10 - Tasks e Agendamento

### Questão 1
Em Kubernetes, qual recurso é usado para executar tarefas periodicamente, similar ao cron do Linux?

- a) Job
- b) Deployment
- c) CronJob
- d) DaemonSet

### Questão 2
Qual expressão de schedule do CronJob executa uma tarefa a cada 5 minutos?

- a) `0 */5 * * *`
- b) `5 * * * *`
- c) `*/5 * * * *`
- d) `* 5 * * *`

---

## Semana 11 - Slack e Email

### Questão 1
Para enviar mensagens para o Slack via Python, qual método de integração é mais simples para notificações automatizadas?

- a) Slack API com OAuth
- b) Slack Bot Token
- c) Webhook URL
- d) Socket Mode

### Questão 2
Qual módulo da biblioteca padrão Python é usado para enviar emails via SMTP?

- a) email
- b) smtplib
- c) mailbox
- d) imaplib

---

## Semana 12 - Cloud e IaC

### Questão 1
Qual biblioteca Python é a SDK oficial para interagir com serviços AWS como S3, EC2 e IAM?

- a) awscli
- b) aws-sdk
- c) boto3
- d) pyaws

### Questão 2
No Terraform, qual comando é usado para visualizar as mudanças que serão aplicadas antes de executá-las?

- a) `terraform preview`
- b) `terraform show`
- c) `terraform plan`
- d) `terraform diff`

---

## Semana 13 - Stacks Platform (SSP)

### Questão 1
O projeto "Gancho" desenvolvido no curso é um receptor de webhooks que responde a eventos do GitHub. Qual evento dispara a execução de scripts de deploy?

- a) push
- b) pull_request
- c) create (para tags)
- d) release

### Questão 2
Qual framework web Python é usado no projeto Gancho para criar a API que recebe webhooks?

- a) Flask
- b) Django
- c) FastAPI
- d) Bottle

---

## Semana 14 - Automação

### Questão 1
Qual biblioteca Python permite executar comandos remotos via SSH de forma programática, sendo uma alternativa de alto nível ao paramiko?

- a) ansible
- b) saltstack
- c) fabric
- d) invoke

### Questão 2
Em um playbook Ansible, qual diretiva é usada para executar comandos com privilégios de superusuário (sudo)?

- a) `sudo: true`
- b) `privilege_escalation: true`
- c) `become: true`
- d) `root: true`


