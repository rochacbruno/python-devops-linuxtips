# Agendamento no Kubernetes com CronJob

## Visão Geral

Kubernetes CronJobs permitem executar tarefas periodicamente em um cluster, similar ao cron do Linux, mas com recursos adicionais:
- Execução em containers isolados
- Gestão de recursos (CPU, memória)
- Controle de acesso via RBAC
- Histórico de execuções
- Escalabilidade e alta disponibilidade

### Componentes desta Seção

1. **scan_images.py**: Script Python que usa a API do Kubernetes para listar pods e verificar tags de imagens
2. **Dockerfile**: Containeriza o script
3. **RBAC manifests**: ServiceAccount, Role e RoleBinding para permissões
4. **Deployment manifests**: Pods de exemplo (alguns com tag `latest`)
5. **CronJob manifest**: Agendamento da tarefa
6. **Scripts auxiliares**: Automação para setup do cluster

---

## Pré-requisitos

### 1. Instalar Docker

```bash
# Verificar se Docker está instalado
docker --version

# Se não estiver, instale:
# Ubuntu/Debian:
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Adicionar usuário ao grupo docker
sudo usermod -aG docker $USER

# Fazer logout e login para aplicar
```

### 2. Instalar kubectl

```bash
# Linux (amd64):
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl

# Verificar instalação
kubectl version --client
```

### 3. Instalar kind (Kubernetes in Docker)

```bash
# Linux (amd64):
curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.20.0/kind-linux-amd64
chmod +x ./kind
sudo mv ./kind /usr/local/bin/kind

# Verificar instalação
kind version
```

**O que é kind?**
- Kind (Kubernetes IN Docker) executa clusters Kubernetes dentro de containers Docker
- Perfeito para desenvolvimento e testes locais
- Rápido de criar e destruir clusters
- Suporta múltiplos nodes

### 4. Instalar biblioteca Python do Kubernetes

```bash
pip install kubernetes
```

---

> **Atenção**: Os passos descritos aqui também estão disponíveis em scripts ordenados, iniciando no `0-download.sh`

## Passo 1: Criar Cluster Kubernetes com kind

### Método Manual

```bash
# Criar cluster
kind create cluster --name image-scanner-cluster

# Verificar nodes
kubectl get nodes

# Verificar contexto
kubectl config current-context
# Deve mostrar: kind-image-scanner-cluster
```

### Verificar Cluster

```bash
# Ver informações do cluster
kubectl cluster-info

# Listar todos os contextos
kubectl config get-contexts

# Trocar de contexto (se necessário)
kubectl config use-context kind-image-scanner-cluster

# Ver pods do sistema
kubectl get pods -n kube-system
```

---

## Passo 2: Entender o Script scan_images.py

### Funcionalidades Principais

1. **Inicialização do cliente Kubernetes**:
   ```python
   config.load_incluster_config()  # Quando rodando em pod
   # OU
   config.load_kube_config()  # Quando rodando localmente
   ```

2. **Listar pods em um namespace**:
   ```python
   v1 = client.CoreV1Api()
   pods = v1.list_namespaced_pod(namespace="default")
   ```

3. **Verificar tags de imagens**:
   - Imagens sem tag (ex: `nginx`) → usa `latest` implicitamente ❌
   - Imagens com tag `latest` (ex: `nginx:latest`) ❌
   - Imagens com tag específica (ex: `nginx:1.25.3`) ✓

4. **Gerar alertas**: Escreve em `/tmp/alertas`

### Testar Localmente (Fora do Cluster)

```bash
# Executar script
uv run scan_images.py
```

Saída esperada (sem pods ainda):
```
Iniciando Kubernetes Image Scanner...
Namespace configurado: default

======================================================================
Kubernetes Image Scanner
Namespace: default
Timestamp: 2025-01-15 14:30:00
======================================================================

Obtendo pods do namespace 'default'...
Nenhum pod encontrado no namespace 'default'
```

---

## Passo 3: Construir e Carregar Imagem Docker

### Método Manual

```bash
# Construir imagem
docker build -t image-scanner:latest .

# Verificar imagem local
docker images | grep image-scanner

# Carregar no cluster kind
kind load docker-image image-scanner:latest --name image-scanner-cluster

# Verificar imagens no cluster
docker exec image-scanner-cluster-control-plane crictl images | grep image-scanner
```

**Por que precisamos carregar a imagem?**
- O kind roda Kubernetes dentro do Docker
- O cluster kind não tem acesso direto às imagens Docker locais
- Precisamos "empurrar" a imagem para dentro do cluster

---

## Passo 4: Entender Manifests do Kubernetes

### 4.1. RBAC (Role-Based Access Control)

**Por que precisamos de RBAC?**
- Por padrão, pods não têm permissões para acessar a API do Kubernetes
- Precisamos criar uma ServiceAccount com permissões específicas
- Princípio do menor privilégio: damos apenas as permissões necessárias

**Arquivo: `k8s/rbac.yaml`**

```yaml
# 1. ServiceAccount: identidade para o pod
apiVersion: v1
kind: ServiceAccount
metadata:
  name: image-scanner

# 2. Role: define permissões
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: pod-reader
rules:
  - apiGroups: [""]
    resources: ["pods"]
    verbs: ["get", "list", "watch"]

# 3. RoleBinding: associa ServiceAccount à Role
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: image-scanner-binding
roleRef:
  kind: Role
  name: pod-reader
subjects:
  - kind: ServiceAccount
    name: image-scanner
```

### 4.2. Deployments de Teste

**Arquivo: `k8s/deployment-with-latest.yaml`**

Cria 3 deployments:

1. **nginx-latest** (2 replicas): Usa `nginx:latest` ❌
2. **nginx-no-tag** (1 replica): Usa `nginx` (sem tag) ❌
3. **nginx-pinned** (1 replica): Usa `nginx:1.25.3` ✓

**Por que tag `latest` é ruim?**
- `latest` não significa "versão mais recente"
- `latest` é apenas uma tag como qualquer outra
- Se você fizer pull da mesma imagem `latest` em dias diferentes, pode obter versões diferentes
- Quebra reprodutibilidade e pode causar bugs inesperados
- Impossível fazer rollback preciso

**Boas práticas:**
- Use tags específicas: `nginx:1.25.3`
- Ou use digests SHA256: `nginx@sha256:abc123...`
- Nunca use `latest` em produção

### 4.3. CronJob

**Arquivo: `k8s/cronjob.yaml`**

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: image-scanner-cronjob
spec:
  schedule: "*/5 * * * *"  # A cada 5 minutos
  jobTemplate:
    spec:
      template:
        spec:
          serviceAccountName: image-scanner
          containers:
            - name: scanner
              image: image-scanner:latest
              env:
                - name: SCAN_NAMESPACE
                  value: "default"
```

**Sintaxe do schedule** (mesma do cron):
```
┌─── minuto (0-59)
│ ┌─── hora (0-23)
│ │ ┌─── dia do mês (1-31)
│ │ │ ┌─── mês (1-12)
│ │ │ │ ┌─── dia da semana (0-6)
* * * * *
```

Exemplos:
```yaml
"*/5 * * * *"      # A cada 5 minutos
"0 * * * *"        # A cada hora
"0 */6 * * *"      # A cada 6 horas
"0 9 * * *"        # Todo dia às 9h
"0 9 * * 1-5"      # Segunda a sexta às 9h
"0 0 1 * *"        # Primeiro dia do mês à meia-noite
```

---

## Passo 5: Deploy dos Manifests

### Método Manual

```bash
# 1. Aplicar RBAC
kubectl apply -f k8s/rbac.yaml

# 2. Aplicar deployments de teste
kubectl apply -f k8s/deployment-with-latest.yaml

# 3. Aguardar pods ficarem prontos
kubectl wait --for=condition=ready pod -l app=nginx-bad-example --timeout=60s

# 4. Aplicar CronJob
kubectl apply -f k8s/cronjob.yaml

# 5. Verificar recursos criados
kubectl get all
```

### Verificar Recursos

```bash
# Ver pods
kubectl get pods

# Ver deployments
kubectl get deployments

# Ver cronjob
kubectl get cronjob

# Ver detalhes do cronjob
kubectl describe cronjob image-scanner-cronjob
```

---

## Passo 6: Executar e Monitorar o Scanner

### Opção 1: Aguardar Execução Automática

O CronJob está configurado para executar a cada 2 minutos. Aguarde até 2 minutos e:

```bash
# Ver jobs criados pelo CronJob
kubectl get jobs

# Ver pods dos jobs
kubectl get pods | grep image-scanner
```

### Opção 2: Executar Manualmente (Recomendado para Testes)

```bash
# Criar job manualmente a partir do CronJob
kubectl create job --from=cronjob/image-scanner-cronjob manual-scan-1

# Ver status do job
kubectl get job manual-scan-1

# Ver pod criado
kubectl get pods | grep manual-scan-1
```

### Ver Logs do Scanner

```bash
# Obter nome do pod
POD_NAME=$(kubectl get pods -l app=image-scanner --no-headers -o custom-columns=":metadata.name" | head -1)

# Ver logs
kubectl logs $POD_NAME

# OU ver logs do job diretamente
kubectl logs job/manual-scan-1
```

Saída esperada:
```
Iniciando Kubernetes Image Scanner...
Namespace configurado: default

======================================================================
Kubernetes Image Scanner
Namespace: default
Timestamp: 2025-01-15 14:35:22
======================================================================

Obtendo pods do namespace 'default'...
✓ Encontrados 4 pod(s)

Pod: nginx-latest-abc123-xyz
  Container: nginx
  Imagem: nginx:latest
  Status: Running
  ⚠️  ALERTA: Usando tag 'latest'!

Pod: nginx-latest-abc123-def
  Container: nginx
  Imagem: nginx:latest
  Status: Running
  ⚠️  ALERTA: Usando tag 'latest'!

Pod: nginx-no-tag-abc456-xyz
  Container: nginx
  Imagem: nginx
  Status: Running
  ⚠️  ALERTA: Usando tag 'latest'!

Pod: nginx-pinned-abc789-xyz
  Container: nginx
  Imagem: nginx:1.25.3
  Status: Running
  ✓ OK: Imagem pinada

======================================================================
RESUMO:
  Total de pods: 4
  Total de containers: 4
  Containers com 'latest': 3
======================================================================

⚠️  ALERTA: Encontrados 3 container(s) usando tag 'latest' no namespace 'default'
```

---

## Passo 7: Acessar Alertas

### Método 1: Ver logs do pod

```bash
kubectl logs job/manual-scan-1
```

### Método 2: Exec no pod (se ainda estiver rodando)

```bash
# Obter nome do pod
POD_NAME=$(kubectl get pods -l app=image-scanner --no-headers -o custom-columns=":metadata.name" | head -1)

# Executar comando no pod
kubectl exec $POD_NAME -- cat /tmp/alertas
```

### Método 3: Copiar arquivo para local

```bash
kubectl cp $POD_NAME:/tmp/alertas ./alertas
cat alertas
```

---

## Passo 8: Gerenciar CronJobs

### Ver Histórico de Execuções

```bash
# Listar todos os jobs criados pelo CronJob
kubectl get jobs

# Ver detalhes de um job específico
kubectl describe job <job-name>

# Ver pods de todos os jobs (incluindo completados)
kubectl get pods --show-all
```

### Suspender CronJob

```bash
# Suspender (parar de criar novos jobs)
kubectl patch cronjob image-scanner-cronjob -p '{"spec":{"suspend":true}}'

# Verificar
kubectl get cronjob
# Saída: SUSPEND = True

# Retomar
kubectl patch cronjob image-scanner-cronjob -p '{"spec":{"suspend":false}}'
```

### Alterar Schedule

```bash
# Editar CronJob
kubectl edit cronjob image-scanner-cronjob

# Altere a linha:
#   schedule: "*/5 * * * *"
# Para:
#   schedule: "0 */6 * * *"  # A cada 6 horas

# Salvar e sair (ESC :wq no vim)
```

### Limitar Histórico

```yaml
spec:
  successfulJobsHistoryLimit: 3  # Manter últimos 3 jobs bem-sucedidos
  failedJobsHistoryLimit: 3      # Manter últimos 3 jobs com falha
```

Jobs mais antigos são automaticamente deletados.

### Deletar Jobs Manualmente

```bash
# Deletar job específico
kubectl delete job manual-scan-1

# Deletar todos os jobs do CronJob
kubectl delete jobs -l app=image-scanner

# Deletar o CronJob (para de criar novos jobs)
kubectl delete cronjob image-scanner-cronjob
```

---

## Passo 9: Recursos Avançados

### 9.1. Concurrency Policy

Controla o que fazer se um job ainda estiver rodando quando chega a hora do próximo:

```yaml
spec:
  concurrencyPolicy: Allow  # Padrão: permite jobs concorrentes

  # OU
  concurrencyPolicy: Forbid  # Pula execução se anterior ainda rodando

  # OU
  concurrencyPolicy: Replace  # Cancela job anterior e inicia novo
```

### 9.2. Starting Deadline

Define quanto tempo após o schedule o job pode iniciar:

```yaml
spec:
  startingDeadlineSeconds: 300  # Se perder o schedule, pode iniciar até 5min depois
```

Útil quando:
- Cluster estava indisponível
- Recursos insuficientes no horário agendado

### 9.3. Resources e Limits

```yaml
spec:
  jobTemplate:
    spec:
      template:
        spec:
          containers:
            - name: scanner
              resources:
                requests:
                  memory: "128Mi"
                  cpu: "100m"
                limits:
                  memory: "256Mi"
                  cpu: "200m"
```

- **requests**: Recursos garantidos
- **limits**: Máximo que o pod pode usar

### 9.4. Timeout

```yaml
spec:
  jobTemplate:
    spec:
      activeDeadlineSeconds: 600  # Job é terminado se rodar mais de 10min
```

### 9.5. Retry Policy

```yaml
spec:
  jobTemplate:
    spec:
      backoffLimit: 2  # Tentar até 2 vezes em caso de falha
```

### 9.6. Múltiplos Namespaces

Para escanear múltiplos namespaces, crie ClusterRole em vez de Role:

```yaml
# ClusterRole: permissões em todos os namespaces
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: pod-reader-cluster
rules:
  - apiGroups: [""]
    resources: ["pods"]
    verbs: ["get", "list", "watch"]

---
# ClusterRoleBinding
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: image-scanner-cluster-binding
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: pod-reader-cluster
subjects:
  - kind: ServiceAccount
    name: image-scanner
    namespace: default
```

Depois modifique o script para iterar namespaces:

```python
v1 = client.CoreV1Api()
namespaces = v1.list_namespace()
for ns in namespaces.items:
    scan(ns.metadata.name)
```

---

## Passo 10: Integração com Alertas Externos

### 10.1. Slack Webhook

```python
import urllib.request
import json

def enviar_slack(mensagem, webhook_url):
    payload = {"text": mensagem}
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(
        webhook_url,
        data=data,
        headers={'Content-Type': 'application/json'}
    )
    urllib.request.urlopen(req)
```

Configure via ConfigMap ou Secret:

```yaml
env:
  - name: SLACK_WEBHOOK_URL
    valueFrom:
      secretKeyRef:
        name: slack-webhook
        key: url
```

### 10.2. Email via SMTP

```python
import smtplib
from email.mime.text import MIMEText

def enviar_email(mensagem):
    msg = MIMEText(mensagem)
    msg['Subject'] = 'Alerta: Imagens com tag latest'
    msg['From'] = 'scanner@example.com'
    msg['To'] = 'admin@example.com'

    with smtplib.SMTP('smtp.example.com', 587) as smtp:
        smtp.starttls()
        smtp.login('user', 'password')
        smtp.send_message(msg)
```
---

## Troubleshooting

### CronJob não está executando

```bash
# Ver eventos do CronJob
kubectl describe cronjob image-scanner-cronjob

# Ver eventos do namespace
kubectl get events --sort-by='.lastTimestamp'

# Verificar se está suspenso
kubectl get cronjob
# SUSPEND deve ser False
```

### Pod não inicia (ImagePullBackOff)

```bash
# Ver detalhes do pod
kubectl describe pod <pod-name>

# Problema comum: imagem não está no cluster kind
# Solução: ./build-and-load-image.sh
```

### Erro de permissão (Forbidden)

```bash
# Verificar ServiceAccount
kubectl get serviceaccount image-scanner

# Verificar Role
kubectl get role pod-reader

# Verificar RoleBinding
kubectl get rolebinding image-scanner-binding

# Ver se estão associados corretamente
kubectl describe rolebinding image-scanner-binding
```

### Script falha ao executar

```bash
# Ver logs do pod
kubectl logs <pod-name>

# Se erro de importação, verificar Dockerfile
# Se erro de conexão à API, verificar RBAC

# Testar localmente primeiro
python3 scan_images.py
```

### Job fica em estado "Pending"

```bash
# Ver detalhes do pod
kubectl describe pod <pod-name>

# Causas comuns:
# - Recursos insuficientes (CPU/memória)
# - ImagePullBackOff
# - Node sem espaço em disco

# Ver recursos do cluster
kubectl top nodes
```

---

## Limpeza

### Remover Recursos (Manter Cluster)

```bash
kubectl delete cronjob image-scanner-cronjob
kubectl delete deployment nginx-latest nginx-no-tag nginx-pinned
kubectl delete rolebinding image-scanner-binding
kubectl delete role pod-reader
kubectl delete serviceaccount image-scanner
```

### Deletar Cluster Completo

```bash
# Método automatizado
./cleanup.sh

# OU manualmente
kind delete cluster --name image-scanner-cluster
```

---

## Comandos Úteis de Kubernetes

### Gerenciamento de Recursos

```bash
# Ver todos os recursos
kubectl get all

# Ver recursos de um tipo específico
kubectl get pods
kubectl get deployments
kubectl get cronjobs
kubectl get jobs

# Ver com mais detalhes
kubectl get pods -o wide

# Ver em formato YAML
kubectl get pod <pod-name> -o yaml

# Ver em formato JSON
kubectl get pod <pod-name> -o json

# Filtrar por labels
kubectl get pods -l app=nginx-bad-example

# Ver recursos em todos os namespaces
kubectl get pods --all-namespaces
# OU
kubectl get pods -A
```

### Debugging

```bash
# Ver logs
kubectl logs <pod-name>
kubectl logs <pod-name> -f  # Follow (tempo real)
kubectl logs <pod-name> --previous  # Logs do container anterior (se crashou)

# Ver eventos
kubectl get events
kubectl get events --sort-by='.lastTimestamp'

# Descrever recurso (mostra eventos e detalhes)
kubectl describe pod <pod-name>
kubectl describe cronjob <cronjob-name>

# Executar comando em pod
kubectl exec <pod-name> -- ls /app
kubectl exec <pod-name> -- cat /tmp/alertas

# Shell interativo em pod
kubectl exec -it <pod-name> -- /bin/bash
```

### Edição e Atualização

```bash
# Editar recurso (abre editor)
kubectl edit cronjob image-scanner-cronjob

# Aplicar mudanças de arquivo
kubectl apply -f k8s/cronjob.yaml

# Deletar recurso
kubectl delete cronjob image-scanner-cronjob
kubectl delete -f k8s/cronjob.yaml

# Patch (alterar campo específico)
kubectl patch cronjob image-scanner-cronjob -p '{"spec":{"suspend":true}}'
```

### Informações do Cluster

```bash
# Info do cluster
kubectl cluster-info

# Ver nodes
kubectl get nodes

# Uso de recursos (requer metrics-server)
kubectl top nodes
kubectl top pods

# Ver configuração
kubectl config view
kubectl config current-context
kubectl config get-contexts
```

---

## Recursos Adicionais

### Documentação Oficial

- Kubernetes CronJobs: https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/
- Kubernetes Python Client: https://github.com/kubernetes-client/python
- Kind: https://kind.sigs.k8s.io/
- RBAC: https://kubernetes.io/docs/reference/access-authn-authz/rbac/

### Ferramentas Úteis

- **k9s**: Terminal UI para Kubernetes
  ```bash
  # Instalação
  brew install k9s  # macOS
  # https://k9scli.io/topics/install/
  ```

- **kubectx/kubens**: Trocar contextos e namespaces facilmente
  ```bash
  brew install kubectx
  ```

- **stern**: Ver logs de múltiplos pods
  ```bash
  brew install stern
  stern image-scanner
  ```

### Alternativas ao kind

- **minikube**: Outra solução para cluster local
- **k3s/k3d**: Kubernetes leve
- **Docker Desktop**: Inclui Kubernetes
- **microk8s**: Kubernetes para Ubuntu

## Conteúdo Extra

https://linuxtips.io/como-automatizar-a-deteccao-de-health-checks-em-kubernetes-com-python-e-slack/
