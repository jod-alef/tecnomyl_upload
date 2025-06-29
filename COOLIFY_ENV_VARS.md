# Variáveis de Ambiente para Coolify

Configure estas variáveis de ambiente no seu projeto Coolify:

## 🔧 **Backend (Obrigatórias)**
```bash
# MinIO Configuration
MINIO_ENDPOINT=seu-minio.com:9000
MINIO_ACCESS_KEY=sua_access_key
MINIO_SECRET_KEY=sua_secret_key
MINIO_SECURE=false
MINIO_BUCKET=tecnomyl

# CORS Configuration
CORS_ORIGINS=https://uploadtecnomyl.alef.host
```

## 🎨 **Frontend (Obrigatórias)**
```bash
# URL da API Backend
REACT_APP_API_URL=https://api-uploadtecnomyl.alef.host
```

## 🔌 **WordPress Integration (Opcionais)**
```bash
WORDPRESS_API_URL=https://seu-wordpress.com/wp-json/wp/v2
WORDPRESS_USERNAME=seu_usuario
WORDPRESS_PASSWORD=sua_senha_aplicacao
```

## 📋 **Exemplo Completo para Coolify**

### **Variáveis que você DEVE configurar:**
1. `MINIO_ENDPOINT` - Endpoint do seu MinIO
2. `MINIO_ACCESS_KEY` - Chave de acesso MinIO
3. `MINIO_SECRET_KEY` - Chave secreta MinIO 
4. `MINIO_SECURE` - `false` para HTTP, `true` para HTTPS
5. `MINIO_BUCKET` - Nome do bucket (ex: `tecnomyl`)
6. `CORS_ORIGINS` - URL do frontend (ex: `https://uploadtecnomyl.alef.host`)
7. `REACT_APP_API_URL` - URL da API backend (ex: `https://api-uploadtecnomyl.alef.host`)

### **URLs de exemplo baseadas no seu domínio:**
- **Frontend**: `https://uploadtecnomyl.alef.host`
- **Backend API**: `https://api-uploadtecnomyl.alef.host` 
- **MinIO**: `minio.alef.host:9000`

## ⚠️ **Importante**

1. **CORS_ORIGINS** deve conter a URL EXATA do frontend
2. **REACT_APP_API_URL** deve apontar para onde o backend estará acessível
3. **MINIO_SECURE=false** se seu MinIO não tem SSL configurado
4. As URLs devem ser **sem barra no final**

## 🚀 **Como configurar no Coolify**

1. Vá para seu projeto no Coolify
2. Clique em "Environment Variables" 
3. Adicione cada variável listada acima
4. Faça deploy novamente

**Após configurar, o frontend conseguirá se conectar ao backend!** 🎉 