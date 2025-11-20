#!/bin/bash
# Script para criar cluster Kubernetes com kind

set -e

CLUSTER_NAME="image-scanner-cluster"
PATH="$PWD:$PATH"


echo "=============================================="
echo "Configurando cluster Kubernetes com kind"
echo "=============================================="

# Verificar se kind está instalado
if ! command -v kind &> /dev/null; then
    echo "❌ kind não encontrado!"
    echo ""
    echo "Instale o kind seguindo as instruções em:"
    echo "https://kind.sigs.k8s.io/docs/user/quick-start/#installation"
    echo ""
    echo "Instalação rápida (Linux):"
    echo "  curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.20.0/kind-linux-amd64"
    echo "  chmod +x ./kind"
    echo "  sudo mv ./kind /usr/local/bin/kind"
    exit 1
fi

# Verificar se kubectl está instalado
if ! command -v kubectl &> /dev/null; then
    echo "❌ kubectl não encontrado!"
    echo ""
    echo "Instale o kubectl seguindo as instruções em:"
    echo "https://kubernetes.io/docs/tasks/tools/"
    exit 1
fi

echo "✓ kind instalado: $(kind version)"
echo "✓ kubectl instalado: $(kubectl version --client --short 2>/dev/null || kubectl version --client)"
echo ""

# Verificar se cluster já existe
if kind get clusters 2>/dev/null | grep -q "^${CLUSTER_NAME}$"; then
    echo "⚠️  Cluster '$CLUSTER_NAME' já existe!"
    read -p "Deseja deletar e recriar? (s/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Ss]$ ]]; then
        echo "Deletando cluster existente..."
        kind delete cluster --name "$CLUSTER_NAME"
    else
        echo "Usando cluster existente."
        exit 0
    fi
fi

# Criar cluster
echo "Criando cluster '$CLUSTER_NAME'..."
kind create cluster --name "$CLUSTER_NAME" --config - <<EOF
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
  - role: control-plane
  - role: worker
EOF

echo ""
echo "✓ Cluster criado com sucesso!"
echo ""

# Verificar nodes
echo "Verificando nodes..."
kubectl get nodes
echo ""

# Verificar contexto
echo "Contexto atual do kubectl:"
kubectl config current-context
echo ""

echo "=============================================="
echo "Cluster Kubernetes está pronto para uso!"
echo "=============================================="
echo ""
echo "Próximos passos:"
echo "  1. Construir a imagem: ./build-and-load-image.sh"
echo "  2. Aplicar manifests: ./deploy-to-cluster.sh"
echo ""
