# Deploy Upload Tecnomyl no Coolify

Este guia detalha como fazer o deploy do sistema Upload Tecnomyl em um painel Coolify.

## 📋 Pré-requisitos

### 1. Servidor MinIO
Você precisará de um servidor MinIO configurado e acessível. Opções:
- **MinIO Cloud** (recomendado para produção)
- **Self-hosted MinIO** no seu servidor
- **Amazon S3** (compatível com MinIO SDK)

### 2. Coolify Configurado
- Painel Coolify instalado e funcionando
- Acesso ao repositório Git do projeto
- Domínios configurados (opcional, mas recomendado)

## 🚀 Processo de Deploy

### Passo 1: Preparar o Repositório

1. **Fazer commit de todas as alterações:**
   ```bash
   git add .
   git commit -m "Preparação para deploy Coolify"
   git push origin main
   ```

2. **Verificar arquivos necessários:**
   - ✅ `docker-compose.prod.yml`
   - ✅ `frontend/Dockerfile.prod`
   - ✅ `frontend/nginx.conf`
   - ✅ `backend/Dockerfile`

### Passo 2: Configurar Aplicação no Coolify

1. **Acessar o painel Coolify**
2. **Criar nova aplicação:**
   - Clique em "New Resource" → "Application"
   - Escolha "Docker Compose"
   - Cole a URL do seu repositório Git

3. **Configurar Build:**
   - Branch: `main`
   - Docker Compose File: `docker-compose.prod.yml`
   - Build Pack: Docker Compose

### Passo 3: Configurar Variáveis de Ambiente

No painel Coolify, adicione as seguintes variáveis de ambiente:

#### MinIO Configuration (OBRIGATÓRIO)
```bash
MINIO_ENDPOINT=seu-minio.exemplo.com:9000
MINIO_ACCESS_KEY=sua_access_key
MINIO_SECRET_KEY=sua_secret_key
MINIO_SECURE=true
MINIO_BUCKET=tecnomyl
```

#### Frontend Configuration
```bash
REACT_APP_API_URL=https://api.tecnomyl-upload.exemplo.com
```

#### CORS Configuration
```bash
CORS_ORIGINS=https://tecnomyl-upload.exemplo.com,https://www.tecnomyl-upload.exemplo.com
```

#### WordPress Integration (OPCIONAL)
```bash
WORDPRESS_API_URL=https://tecnomyl.com/wp-json/wp/v2
WORDPRESS_USERNAME=usuario_api
WORDPRESS_PASSWORD=senha_aplicacao
```

### Passo 4: Configurar Domínios

1. **Backend API:**
   - Domínio: `api.tecnomyl-upload.exemplo.com`
   - Porta: `8000`
   - Habilitar HTTPS

2. **Frontend:**
   - Domínio: `tecnomyl-upload.exemplo.com`
   - Porta: `3000` (interno: `80`)
   - Habilitar HTTPS

### Passo 5: Deploy

1. **Iniciar Deploy:**
   - Clique em "Deploy"
   - Aguarde o build dos containers
   - Monitore os logs para identificar possíveis erros

2. **Verificar Health Checks:**
   - Backend: `https://api.tecnomyl-upload.exemplo.com/health`
   - Frontend: `https://tecnomyl-upload.exemplo.com/health`

## 🔧 Configurações Avançadas

### SSL/TLS
O Coolify gerencia automaticamente os certificados SSL via Let's Encrypt.

### Backup MinIO
Configure backup automático do bucket MinIO:
```bash
# Exemplo com script de backup
mc mirror minio/tecnomyl backup/tecnomyl-$(date +%Y%m%d)
```

### Monitoramento
Configure alertas no Coolify para:
- Falhas de deploy
- Health checks falhando
- Alto uso de recursos

## 🐛 Troubleshooting

### Problema: Backend não inicia
```bash
# Verificar logs
docker logs tecnomyl-backend

# Possíveis causas:
# 1. Variáveis de ambiente MinIO incorretas
# 2. MinIO inacessível
# 3. Dependências Python faltando
```

### Problema: Frontend não carrega
```bash
# Verificar logs
docker logs tecnomyl-frontend

# Possíveis causas:
# 1. REACT_APP_API_URL incorreta
# 2. Build do React falhou
# 3. Nginx mal configurado
```

### Problema: CORS
```bash
# Verificar se CORS_ORIGINS está configurado corretamente
# Deve incluir o domínio do frontend
```

## 📊 Monitoramento de Produção

### Logs Importantes
```bash
# Backend API
docker logs -f tecnomyl-backend

# Frontend Nginx
docker logs -f tecnomyl-frontend

# Sistema geral
docker-compose -f docker-compose.prod.yml logs -f
```

### Métricas de Performance
- Tempo de upload de arquivos
- Resposta da API MinIO
- Uso de memória/CPU dos containers

## 🔐 Segurança em Produção

### Checklist de Segurança
- [ ] HTTPS habilitado em todos os domínios
- [ ] Variáveis de ambiente seguras (não hardcoded)
- [ ] MinIO com credenciais fortes
- [ ] CORS configurado adequadamente
- [ ] Headers de segurança configurados (nginx)
- [ ] Backup regular dos dados

### Atualizações
```bash
# Para atualizar a aplicação:
git push origin main
# Coolify fará redeploy automaticamente
```

## 📞 Suporte

### URLs Importantes
- **Frontend:** https://tecnomyl-upload.exemplo.com
- **API:** https://api.tecnomyl-upload.exemplo.com
- **Docs API:** https://api.tecnomyl-upload.exemplo.com/docs
- **Health Backend:** https://api.tecnomyl-upload.exemplo.com/health
- **Health Frontend:** https://tecnomyl-upload.exemplo.com/health

### Contatos
- Documentação Coolify: https://coolify.io/docs
- MinIO Documentation: https://docs.min.io/ 