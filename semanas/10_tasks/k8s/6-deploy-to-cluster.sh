#!/bin/bash
set -e

PATH="$PWD:$PATH"
CLUSTER_NAME="image-scanner-cluster"

echo "=============================================="
echo "Fazendo deploy no cluster Kubernetes"
echo "=============================================="

# Verificar se cluster existe
if ! kind get clusters 2>/dev/null | grep -q "^${CLUSTER_NAME}$"; then
    echo "❌ Cluster '$CLUSTER_NAME' não encontrado!"
    echo "Execute primeiro: ./setup-kind-cluster.sh"
    exit 1
fi

# Verificar se kubectl está configurado corretamente
if ! kubectl cluster-info &> /dev/null; then
    echo "❌ kubectl não está conectado ao cluster!"
    echo "Execute: kubectl config use-context kind-$CLUSTER_NAME"
    exit 1
fi

echo "Cluster: $(kubectl config current-context)"
echo ""

# Aplicar RBAC
echo "1. Aplicando RBAC (ServiceAccount, Role, RoleBinding)..."
kubectl apply -f k8s/rbac.yaml
echo "   ✓ RBAC aplicado"
echo ""

# Aplicar deployments de teste
echo "2. Aplicando deployments de teste..."
kubectl apply -f k8s/deployment-with-latest.yaml
echo "   ✓ Deployments aplicados"
echo ""

# Aguardar pods ficarem prontos
echo "3. Aguardando pods ficarem prontos..."
kubectl wait --for=condition=ready pod -l app=nginx-bad-example --timeout=60s || true
kubectl wait --for=condition=ready pod -l app=nginx-worse-example --timeout=60s || true
kubectl wait --for=condition=ready pod -l app=nginx-good-example --timeout=60s || true
echo ""

# Aplicar CronJob
echo "4. Aplicando CronJob do scanner..."
kubectl apply -f k8s/cronjob.yaml
echo "   ✓ CronJob aplicado"
echo ""

# Aplicar Mailhog pod e service
kubectl apply -f k8s/mailhog.yaml

# Mostrar status
echo "=============================================="
echo "Deploy concluído!"
echo "=============================================="
echo ""

echo "Pods em execução:"
kubectl get pods
echo ""

echo "CronJob criado:"
kubectl get cronjob
echo ""

echo "Próximos passos:"
echo "  1. Aguardar execução automática do CronJob (a cada 5 minutos)"
echo "  2. OU executar manualmente: kubectl create job --from=cronjob/image-scanner-cronjob manual-scan-1"
echo "  3. Ver logs: kubectl logs job/manual-scan-1"
echo ""
