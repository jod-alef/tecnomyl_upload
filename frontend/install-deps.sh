#!/bin/bash

# Script para instalar dependências do frontend Upload Tecnomyl

echo "🧹 Limpando instalações anteriores..."
rm -rf node_modules package-lock.json

echo "📦 Instalando dependências do React..."
npm install

echo "🎨 Instalando dependências CSS necessárias..."
npm install postcss-normalize --legacy-peer-deps

echo "📤 Instalando dependências de upload..."
npm install react-dropzone axios

echo "🔧 Instalando dependências de desenvolvimento..."
npm install --save-dev @types/react @types/react-dom @types/node

echo "✅ Todas as dependências instaladas com sucesso!"
echo "🚀 Execute 'npm start' para iniciar o frontend" 