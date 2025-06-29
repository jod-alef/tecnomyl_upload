#!/bin/bash

# Script para iniciar o ambiente de desenvolvimento Upload Tecnomyl

echo "🚀 Iniciando Upload Tecnomyl - Ambiente de Desenvolvimento"
echo "================================================="

# Função para verificar se uma porta está em uso
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null ; then
        echo "⚠️  Porta $1 já está em uso"
        return 1
    else
        return 0
    fi
}

# Verificar e criar arquivos .env se não existirem
echo "🔐 Verificando configuração de segurança..."

# Backend .env
if [ ! -f "backend/.env" ]; then
    echo "⚠️  Arquivo backend/.env não encontrado! Criando a partir do template..."
    cp backend/env-example backend/.env
    echo "✅ Arquivo backend/.env criado."
    echo "🔑 IMPORTANTE: Configure suas credenciais reais de MinIO no arquivo backend/.env"
    echo ""
fi

# Frontend .env  
if [ ! -f "frontend/.env" ]; then
    echo "⚠️  Arquivo frontend/.env não encontrado! Criando a partir do template..."
    cp frontend/env-example frontend/.env
    echo "✅ Arquivo frontend/.env criado."
fi

# Verificar se backend/.env tem credenciais padrão (inseguras)
if grep -q "sua_access_key_aqui" backend/.env 2>/dev/null; then
    echo ""
    echo "🚨 ATENÇÃO: Credenciais padrão detectadas no backend/.env"
    echo "📝 Edite o arquivo backend/.env com suas configurações reais de MinIO"
    echo ""
    read -p "Pressione Enter após configurar as credenciais para continuar..."
fi

# Verificar portas necessárias
echo "🔍 Verificando portas disponíveis..."
check_port 8000 || exit 1
check_port 3000 || exit 1

# Verificar e configurar ambiente virtual
echo "🐍 Preparando Backend Python..."

# Verificar se o ambiente virtual está configurado
if [ ! -d "backend/venv" ] || [ ! -f "backend/venv/bin/activate" ]; then
    echo "📦 Configurando ambiente virtual..."
    ./setup-venv.sh
    if [ $? -ne 0 ]; then
        echo "❌ Falha ao configurar ambiente virtual!"
        exit 1
    fi
fi

cd backend

# Ativar ambiente virtual
echo "🔄 Ativando ambiente virtual..."
source venv/bin/activate

# Verificar se a ativação foi bem-sucedida
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "✅ Ambiente virtual ativado: $VIRTUAL_ENV"
else
    echo "❌ Falha ao ativar ambiente virtual!"
    echo "💡 Tente executar ./setup-venv.sh primeiro"
    exit 1
fi

echo "✅ Backend configurado!"

echo "🚀 Iniciando Backend..."
uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
cd ..

# Aguardar backend inicializar
echo "⏳ Aguardando backend inicializar..."
sleep 5

# Verificar e instalar dependências do frontend
echo "⚛️  Preparando Frontend React..."
cd frontend

# Verificar se node_modules existe, se não, reinstalar tudo
if [ ! -d "node_modules" ] || [ ! -f "node_modules/.package-lock.json" ]; then
    echo "📦 Instalando dependências do Frontend..."
    ./install-deps.sh
else
    echo "📦 Verificando dependências do Frontend..."
    npm install
fi

echo "✅ Frontend configurado!"
echo "🚀 Iniciando Frontend..."
npm start &
FRONTEND_PID=$!
cd ..

echo ""
echo "✅ Aplicação iniciada com sucesso!"
echo "================================================="
echo "📖 Backend API: http://localhost:8000"
echo "📖 Documentação API: http://localhost:8000/docs"
echo "🌐 Frontend: http://localhost:3000"
echo "================================================="
echo ""
echo "Para parar a aplicação, pressione Ctrl+C"

# Função para parar todos os processos
cleanup() {
    echo ""
    echo "🛑 Parando aplicação..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    
    # Desativar ambiente virtual se estiver ativo
    if [[ "$VIRTUAL_ENV" != "" ]]; then
        echo "🔄 Desativando ambiente virtual..."
        deactivate 2>/dev/null || true
    fi
    
    echo "✅ Aplicação parada"
    exit 0
}

# Capturar sinal de interrupção
trap cleanup SIGINT SIGTERM

# Aguardar até que um dos processos termine
wait 