# Upload Tecnomyl

Sistema de upload de arquivos para produtos da Tecnomyl com integração MinIO.

## 🚀 Tecnologias

- **Frontend**: React + TypeScript + Tailwind CSS
- **Backend**: Python FastAPI
- **Storage**: MinIO
- **Upload**: 3 arquivos por produto (Bula, FISPQ, Ficha de Emergência)

## 📁 Estrutura do Projeto

```
upload-tecnomyl/
├── backend/          # API Python FastAPI
├── frontend/         # React Application
├── docker-compose.yml
└── README.md
```

## 🎯 Funcionalidades

- ✅ Dropdown de seleção de produtos
- ✅ Upload drag & drop para 3 tipos de arquivos
- ✅ Renomeação automática: `[produto]_bula.pdf`, `[produto]_FISPQ.pdf`, `[produto]_Ficha_de_Emergencia.pdf`
- ✅ Integração com bucket MinIO "tecnomyl"
- ✅ URLs permanentes para WordPress

## 🛠️ Como executar

### 🚀 **Primeira execução (RECOMENDADO)**
```bash
# Resolver todos os problemas de dependências
./setup-project.sh

# Depois disso, usar normalmente:
./run-dev.sh
```

### ⚡ **Execuções seguintes**
```bash
./run-dev.sh
```

### 🔧 **Instalação Manual (se necessário)**

#### Backend
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

#### Frontend
```bash
cd frontend
npm install
# Instalar versão correta do Tailwind
npm install @tailwindcss/postcss7-compat@^2.2.17 postcss@^7 autoprefixer@^9
npm start
```

### 🐳 **Docker Compose**
```bash
docker-compose up --build
```

## 📋 Pré-requisitos

- **Python 3.11+**
- **Node.js 18+**
- **MinIO Server** (configurado com bucket "tecnomyl")
- **Git**

## 🔐 Configuração Segura

### 1. **Configurar Credenciais (.env)**
```bash
# Backend - copie e configure
cp backend/env-example backend/.env

# Frontend - copie e configure  
cp frontend/env-example frontend/.env
```

### 2. **MinIO Setup**
- **Bucket**: tecnomyl (com versioning habilitado)
- **Credenciais**: Configure no arquivo `.env` (NUNCA use padrões em produção!)

⚠️ **IMPORTANTE**: Leia o arquivo `SEGURANCA.md` antes do deploy em produção!

## 🆘 Problemas?

Se encontrar erros de dependências ou configuração:
1. 📖 Consulte o `TROUBLESHOOTING.md`
2. 🔄 Execute `./setup-project.sh` para resolver automaticamente
3. 🧹 Em último caso, faça reset completo conforme o guia

## ⚙️ Configuração MinIO

- **Bucket**: tecnomyl
- **Versioning**: Habilitado
- **Estrutura**: `/produtos/{nome_produto}/` 