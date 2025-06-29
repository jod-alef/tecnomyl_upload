#!/bin/bash

# Script para configurar o ambiente virtual Python para o Upload Tecnomyl

echo "🐍 Configurando Ambiente Virtual Python - Upload Tecnomyl"
echo "========================================================="

cd backend

# Remover ambiente virtual antigo se existir e estiver com problemas
if [ -d "venv" ]; then
    echo "🔍 Verificando ambiente virtual existente..."
    if ! . venv/bin/activate 2>/dev/null; then
        echo "⚠️  Ambiente virtual corrompido detectado. Removendo..."
        rm -rf venv
    else
        echo "✅ Ambiente virtual existente funcional"
        deactivate 2>/dev/null || true
    fi
fi

# Criar novo ambiente virtual se necessário
if [ ! -d "venv" ]; then
    echo "📦 Criando novo ambiente virtual..."
    
    # Verificar se python3 está disponível
    if ! command -v python3 >/dev/null 2>&1; then
        echo "❌ Python3 não encontrado! Instale o Python 3.8+ primeiro."
        exit 1
    fi
    
    # Verificar versão do Python
    python_version=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
    echo "🐍 Usando Python $python_version"
    
    if ! python3 -m venv venv; then
        echo "❌ Falha ao criar ambiente virtual!"
        exit 1
    fi
    
    echo "✅ Ambiente virtual criado com sucesso!"
fi

# Ativar ambiente virtual
echo "🔄 Ativando ambiente virtual..."
. venv/bin/activate

# Verificar ativação
if [ "$VIRTUAL_ENV" = "" ]; then
    echo "❌ Falha ao ativar ambiente virtual!"
    exit 1
fi

echo "✅ Ambiente virtual ativado: $VIRTUAL_ENV"

# Atualizar pip
echo "⬆️  Atualizando pip..."
pip install --upgrade pip

# Instalar dependências
echo "📦 Instalando dependências do projeto..."
if pip install -r requirements.txt; then
    echo "✅ Dependências instaladas com sucesso!"
else
    echo "❌ Falha ao instalar dependências!"
    echo "📝 Verifique o arquivo requirements.txt e sua conexão com a internet"
    exit 1
fi

# Testar importações básicas
echo "🧪 Testando importações críticas..."
python3 -c "
try:
    import fastapi
    import uvicorn
    import minio
    print('✅ Todas as importações críticas funcionando')
except ImportError as e:
    print(f'❌ Erro de importação: {e}')
    exit(1)
"

echo ""
echo "✅ Ambiente virtual configurado e pronto para uso!"
echo "========================================================="
echo "💡 Para ativar manualmente: cd backend && source venv/bin/activate"
echo "🚀 Execute ./run-dev.sh para iniciar a aplicação"
echo ""

deactivate

cd .. 