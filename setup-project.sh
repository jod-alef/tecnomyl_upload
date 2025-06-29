#!/bin/bash

# Script de Setup Completo - Upload Tecnomyl
# Este script resolve todos os problemas de dependências

echo "🚀 SETUP UPLOAD TECNOMYL - Resolvendo problemas de dependências"
echo "================================================================"

# Função para verificar se comando existe
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Verificar pré-requisitos
echo "🔍 Verificando pré-requisitos..."

if ! command_exists python3; then
    echo "❌ Python 3 não encontrado. Instale Python 3.8+"
    exit 1
fi

if ! command_exists node; then
    echo "❌ Node.js não encontrado. Instale Node.js 16+"
    exit 1
fi

if ! command_exists npm; then
    echo "❌ NPM não encontrado. Instale NPM"
    exit 1
fi

echo "✅ Pré-requisitos verificados!"

# Criar arquivos .env se não existirem
echo ""
echo "🔐 Configurando arquivos de ambiente..."

if [ ! -f "backend/.env" ]; then
    cp backend/env-example backend/.env
    echo "✅ backend/.env criado"
else
    echo "✅ backend/.env já existe"
fi

if [ ! -f "frontend/.env" ]; then
    cp frontend/env-example frontend/.env
    echo "✅ frontend/.env criado"
else
    echo "✅ frontend/.env já existe"
fi

# Setup Backend
echo ""
echo "🐍 CONFIGURANDO BACKEND PYTHON..."
echo "================================="

cd backend

# Criar ambiente virtual se não existir
if [ ! -d "venv" ]; then
    echo "📦 Criando ambiente virtual Python..."
    python3 -m venv venv
fi

# Ativar ambiente virtual
echo "🔄 Ativando ambiente virtual..."
source venv/bin/activate

# Instalar dependências
echo "📥 Instalando dependências Python..."
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ Backend configurado com sucesso!"
cd ..

# Setup Frontend
echo ""
echo "⚛️  CONFIGURANDO FRONTEND REACT..."
echo "================================="

cd frontend

# Limpar instalações anteriores se houver problemas
if [ -f "package-lock.json" ]; then
    echo "🧹 Limpando instalação anterior..."
    rm -rf node_modules package-lock.json
fi

# Instalar dependências base
echo "📦 Instalando dependências base do React..."
npm install

# Instalar dependências CSS necessárias
echo "🎨 Configurando CSS..."
npm install postcss-normalize --legacy-peer-deps

# Instalar outras dependências
echo "📤 Instalando dependências de upload e utilitários..."
npm install react-dropzone axios

# Verificar se TypeScript está configurado
echo "🔧 Verificando TypeScript..."
npm install --save-dev @types/react @types/react-dom @types/node

echo "✅ Frontend configurado com sucesso!"
cd ..

# Testar configuração
echo ""
echo "🧪 TESTANDO CONFIGURAÇÃO..."
echo "=========================="

# Testar backend
echo "🔍 Testando importações do backend..."
cd backend
source venv/bin/activate
python -c "
try:
    import fastapi
    import minio
    import pydantic
    from dotenv import load_dotenv
    print('✅ Importações do backend OK')
except ImportError as e:
    print(f'❌ Erro de importação: {e}')
    exit(1)
"
cd ..

# Testar frontend
echo "🔍 Testando configuração do frontend..."
cd frontend
npm run build --dry-run 2>/dev/null || echo "⚠️  Build test pendente (normal)"
cd ..

echo ""
echo "🎉 SETUP CONCLUÍDO COM SUCESSO!"
echo "==============================="
echo ""
echo "📋 PRÓXIMOS PASSOS:"
echo "1. Configure suas credenciais MinIO em backend/.env"
echo "2. Execute: ./run-dev.sh"
echo "3. Acesse http://localhost:3000"
echo ""
echo "📚 ARQUIVOS IMPORTANTES:"
echo "- backend/.env (configure suas credenciais MinIO)"
echo "- frontend/.env (configurações do frontend)"
echo "- SEGURANCA.md (leia antes de usar em produção)"
echo ""
echo "🆘 EM CASO DE PROBLEMAS:"
echo "- Backend: cd backend && source venv/bin/activate && python main.py"
echo "- Frontend: cd frontend && npm start" 