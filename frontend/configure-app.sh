#!/bin/sh

# Script para configurar a aplicação com variáveis de ambiente runtime
# Usado como fallback quando variáveis não foram definidas no build time

echo "🔧 Configurando aplicação frontend..."

# Arquivo principal da aplicação
MAIN_JS_FILE=$(find /usr/share/nginx/html/static/js -name "main.*.js" | head -1)

if [ -n "$MAIN_JS_FILE" ] && [ -n "$REACT_APP_API_URL" ]; then
    echo "📡 Configurando API URL: $REACT_APP_API_URL"
    
    # Substituir localhost:8000 pela URL real da API
    sed -i "s|http://localhost:8000|$REACT_APP_API_URL|g" "$MAIN_JS_FILE"
    
    echo "✅ API URL configurada com sucesso!"
else
    echo "⚠️  Usando configuração padrão (localhost:8000)"
fi

echo "🚀 Frontend configurado e pronto!" 