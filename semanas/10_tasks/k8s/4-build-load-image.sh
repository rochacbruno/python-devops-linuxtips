#!/bin/bash
# Script para construir a imagem do scanner e carregá-la no kind

set -e

PATH="$PWD:$PATH"
IMAGE_NAME="image-scanner"
IMAGE_TAG="latest"
FULL_IMAGE="${IMAGE_NAME}:${IMAGE_TAG}"
CLUSTER_NAME="image-scanner-cluster"

echo "=============================================="
echo "Construindo e carregando imagem no kind"
echo "=============================================="

# Verificar se Dockerfile existe
if [ ! -f "Dockerfile" ]; then
    echo "❌ Dockerfile não encontrado!"
    echo "Execute este script no diretório k8s"
    exit 1
fi

# Verificar se docker está instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Docker não encontrado!"
    exit 1
fi

# Construir imagem
echo "Construindo imagem Docker..."
docker build -t "$FULL_IMAGE" .

echo ""
echo "✓ Imagem construída: $FULL_IMAGE"
echo ""

# Verificar se cluster kind existe
if ! kind get clusters 2>/dev/null | grep -q "^${CLUSTER_NAME}$"; then
    echo "⚠️  Cluster '$CLUSTER_NAME' não encontrado!"
    echo "Execute primeiro: ./1-setup-kind-cluster.sh"
    exit 1
fi

# Carregar imagem no kind
echo "Carregando imagem no cluster kind..."
kind load docker-image "$FULL_IMAGE" --name "$CLUSTER_NAME"

echo ""
echo "✓ Imagem carregada no cluster!"
echo ""

# Verificar imagens no cluster (se crictl estiver disponível no node)
echo "Verificando imagem no cluster..."
docker exec "${CLUSTER_NAME}-control-plane" crictl images | grep "$IMAGE_NAME" || true

echo ""
echo "=============================================="
echo "Imagem pronta para uso no cluster!"
echo "=============================================="
echo ""
echo "Próximo passo:"
echo "  ./deploy-to-cluster.sh"
echo ""
