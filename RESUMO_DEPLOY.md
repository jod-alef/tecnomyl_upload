# 🚀 Deploy Rápido no Coolify - Upload Tecnomyl

## ⚡ Passos Rápidos

### 1. Preparar o Projeto
```bash
./prepare-deploy.sh
```

### 2. Fazer Push para Git
```bash
git remote add origin https://github.com/seuusuario/tecnomyl_upload.git
git push -u origin main
```

### 3. Configurar no Coolify

#### Criar Aplicação:
- **Tipo:** Docker Compose
- **Repositório:** URL do seu Git
- **Branch:** main
- **Compose File:** `docker-compose.prod.yml`

#### Variáveis de Ambiente Obrigatórias:
```bash
# MinIO (OBRIGATÓRIO)
MINIO_ENDPOINT=seu-minio.com:9000
MINIO_ACCESS_KEY=sua_chave
MINIO_SECRET_KEY=sua_senha_secreta
MINIO_SECURE=true
MINIO_BUCKET=tecnomyl

# Frontend
REACT_APP_API_URL=https://api.tecnomyl-upload.seudominio.com

# CORS
CORS_ORIGINS=https://tecnomyl-upload.seudominio.com
```

### 4. Configurar Domínios
- **Frontend:** `tecnomyl-upload.seudominio.com` → Porta 3000
- **API:** `api.tecnomyl-upload.seudominio.com` → Porta 8000

### 5. Deploy
1. Clique em **"Deploy"**
2. Aguarde o build
3. Verifique os health checks

## ✅ Verificações Pós-Deploy

### URLs para Testar:
- 🌐 **Frontend:** https://tecnomyl-upload.seudominio.com
- 🔧 **API Docs:** https://api.tecnomyl-upload.seudominio.com/docs
- ❤️ **Health Check:** https://api.tecnomyl-upload.seudominio.com/health

### Funcionalidades Principais:
- [ ] Upload de arquivos funciona
- [ ] Dropdown de produtos carrega
- [ ] Arquivos são salvos no MinIO
- [ ] API retorna URLs corretas

## 🆘 Problemas Comuns

### Backend não inicia:
```bash
# Verificar logs no Coolify
# Problema mais comum: credenciais MinIO incorretas
```

### Frontend em branco:
```bash
# Verificar se REACT_APP_API_URL está correto
# Verificar se CORS_ORIGINS inclui o domínio do frontend
```

### 413 Request Entity Too Large:
- Configurar nginx no Coolify para aceitar uploads maiores
- Aumentar `client_max_body_size` se necessário

## 📞 Suporte

📖 **Documentação Completa:** `DEPLOY_COOLIFY.md`
🔧 **Script de Preparação:** `./prepare-deploy.sh`
🐛 **Troubleshooting:** `TROUBLESHOOTING.md` 