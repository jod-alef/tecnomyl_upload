#!/bin/bash

# Script para preparar o projeto Upload Tecnomyl para deploy no Coolify

echo "🚀 Preparando Upload Tecnomyl para Deploy no Coolify"
echo "===================================================="

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Função para verificar se arquivo existe
check_file() {
    if [ -f "$1" ]; then
        echo -e "${GREEN}✅ $1 encontrado${NC}"
        return 0
    else
        echo -e "${RED}❌ $1 não encontrado${NC}"
        return 1
    fi
}

# Função para verificar se diretório existe
check_dir() {
    if [ -d "$1" ]; then
        echo -e "${GREEN}✅ Diretório $1 encontrado${NC}"
        return 0
    else
        echo -e "${RED}❌ Diretório $1 não encontrado${NC}"
        return 1
    fi
}

echo "🔍 Verificando estrutura do projeto..."

# Verificar arquivos principais
FILES_REQUIRED=(
    "docker-compose.prod.yml"
    "backend/Dockerfile"
    "frontend/Dockerfile.prod"
    "frontend/nginx.conf"
    "backend/requirements.txt"
    "frontend/package.json"
    ".coolify.yml"
    "DEPLOY_COOLIFY.md"
)

missing_files=0
for file in "${FILES_REQUIRED[@]}"; do
    if ! check_file "$file"; then
        missing_files=$((missing_files + 1))
    fi
done

# Verificar diretórios
DIRS_REQUIRED=(
    "backend"
    "frontend"
    "frontend/src"
    "backend"
)

missing_dirs=0
for dir in "${DIRS_REQUIRED[@]}"; do
    if ! check_dir "$dir"; then
        missing_dirs=$((missing_dirs + 1))
    fi
done

if [ $missing_files -gt 0 ] || [ $missing_dirs -gt 0 ]; then
    echo -e "${RED}❌ Projeto incompleto para deploy!${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Estrutura do projeto OK${NC}"

# Verificar se está em um repositório Git
echo "🔍 Verificando repositório Git..."
if [ ! -d ".git" ]; then
    echo -e "${YELLOW}⚠️  Não é um repositório Git. Inicializando...${NC}"
    git init
    git add .
    git commit -m "Initial commit - Upload Tecnomyl"
else
    echo -e "${GREEN}✅ Repositório Git encontrado${NC}"
fi

# Verificar se há mudanças não commitadas
if ! git diff-index --quiet HEAD --; then
    echo -e "${YELLOW}⚠️  Há mudanças não commitadas${NC}"
    echo "📝 Fazendo commit das mudanças..."
    git add .
    git commit -m "Preparação para deploy Coolify - $(date)"
    echo -e "${GREEN}✅ Mudanças commitadas${NC}"
else
    echo -e "${GREEN}✅ Repositório atualizado${NC}"
fi

# Testar build dos containers localmente
echo "🐳 Testando build dos containers..."

echo "🔨 Testando build do backend..."
if docker build -t tecnomyl-backend-test ./backend > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Build do backend OK${NC}"
    docker rmi tecnomyl-backend-test > /dev/null 2>&1
else
    echo -e "${RED}❌ Falha no build do backend${NC}"
    echo "💡 Execute: docker build ./backend para ver detalhes"
    exit 1
fi

echo "🔨 Testando build do frontend..."
if docker build -f frontend/Dockerfile.prod -t tecnomyl-frontend-test ./frontend > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Build do frontend OK${NC}"
    docker rmi tecnomyl-frontend-test > /dev/null 2>&1
else
    echo -e "${RED}❌ Falha no build do frontend${NC}"
    echo "💡 Execute: docker build -f frontend/Dockerfile.prod ./frontend para ver detalhes"
    exit 1
fi

# Verificar configurações de produção
echo "⚙️  Verificando configurações de produção..."

# Verificar se existem arquivos .env de exemplo
if [ ! -f "backend/env-example" ]; then
    echo -e "${YELLOW}⚠️  Criando backend/env-example...${NC}"
    cat > backend/env-example << EOF
# MinIO Configuration
MINIO_ENDPOINT=seu-minio.exemplo.com:9000
MINIO_ACCESS_KEY=sua_access_key
MINIO_SECRET_KEY=sua_secret_key
MINIO_SECURE=true
MINIO_BUCKET=tecnomyl

# CORS Configuration
CORS_ORIGINS=https://tecnomyl-upload.exemplo.com

# WordPress Integration (opcional)
WORDPRESS_API_URL=https://tecnomyl.com/wp-json/wp/v2
WORDPRESS_USERNAME=usuario_api
WORDPRESS_PASSWORD=senha_aplicacao
EOF
fi

if [ ! -f "frontend/env-example" ]; then
    echo -e "${YELLOW}⚠️  Criando frontend/env-example...${NC}"
    cat > frontend/env-example << EOF
# Frontend Configuration
REACT_APP_API_URL=https://api.tecnomyl-upload.exemplo.com
EOF
fi

# Criar checklist para o usuário
echo ""
echo "📋 CHECKLIST PARA DEPLOY NO COOLIFY"
echo "===================================="
echo ""
echo "✅ Projeto preparado e validado"
echo "✅ Containers testados localmente"
echo "✅ Arquivos de configuração criados"
echo ""
echo "🔧 PRÓXIMOS PASSOS:"
echo "1. 📤 Fazer push para repositório Git remoto"
echo "2. 🌐 Configurar aplicação no painel Coolify"
echo "3. 🔐 Configurar variáveis de ambiente no Coolify"
echo "4. 🚀 Fazer deploy"
echo ""
echo "📖 Consulte DEPLOY_COOLIFY.md para instruções detalhadas"
echo ""
echo "🔗 URLs que você precisará configurar:"
echo "   • Frontend: https://tecnomyl-upload.seudominio.com"
echo "   • API: https://api.tecnomyl-upload.seudominio.com"
echo ""
echo "🔑 Variáveis obrigatórias no Coolify:"
echo "   • MINIO_ENDPOINT"
echo "   • MINIO_ACCESS_KEY"
echo "   • MINIO_SECRET_KEY"
echo "   • REACT_APP_API_URL"
echo "   • CORS_ORIGINS"
echo ""
echo -e "${GREEN}🎉 Projeto pronto para deploy no Coolify!${NC}" 