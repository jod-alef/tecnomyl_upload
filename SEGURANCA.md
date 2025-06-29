# 🔒 Guia de Segurança - Upload Tecnomyl

## ⚠️ **IMPORTANTE - LEIA ANTES DE USAR EM PRODUÇÃO**

### 🚨 **NUNCA faça:**

❌ **Commitar arquivos `.env`** - Eles contêm credenciais sensíveis  
❌ **Deixar credenciais padrão** - Sempre altere `minioadmin`  
❌ **Usar HTTP em produção** - Configure HTTPS  
❌ **Expor MinIO publicamente** sem autenticação  
❌ **Hardcodar credenciais** no código  

### ✅ **SEMPRE faça:**

✅ **Use arquivos `.env`** para credenciais  
✅ **Configure o `.gitignore`** (já incluído)  
✅ **Altere credenciais padrão** do MinIO  
✅ **Use HTTPS** em produção  
✅ **Configure CORS** adequadamente  
✅ **Monitore logs** de acesso  

## 🔐 **Configuração Segura**

### 1. **Backend (.env)**

```bash
# Copie env-example para .env
cp backend/env-example backend/.env

# Configure com credenciais REAIS
MINIO_ENDPOINT=seu-minio-server.com:9000
MINIO_ACCESS_KEY=sua_access_key_segura
MINIO_SECRET_KEY=sua_secret_key_muito_forte
MINIO_SECURE=True  # Para HTTPS
MINIO_BUCKET=tecnomyl
```

### 2. **Frontend (.env)**

```bash
# Para produção
REACT_APP_API_URL=https://api.tecnomyl.com
REACT_APP_ENV=production
```

### 3. **MinIO Seguro**

```bash
# Gerar credenciais seguras
openssl rand -base64 32  # Access Key
openssl rand -base64 32  # Secret Key
```

## 🛡️ **Configurações de Produção**

### **MinIO**
- ✅ Credenciais fortes (32+ caracteres)
- ✅ HTTPS habilitado (certificado SSL)
- ✅ Bucket policy restritivo
- ✅ Versioning habilitado
- ✅ Backup regular dos dados

### **API Backend**
- ✅ Rate limiting implementado
- ✅ Logs de auditoria ativos
- ✅ Validação rigorosa de arquivos
- ✅ CORS configurado corretamente
- ✅ Timeouts adequados

### **Frontend**
- ✅ Build de produção otimizado
- ✅ URLs da API configuradas corretamente
- ✅ Tratamento de erros robusto

## 🔍 **Monitoramento**

### **Logs Importantes**
```bash
# Backend
tail -f backend/logs/upload.log

# MinIO
tail -f /var/log/minio/minio.log

# Nginx (se usar proxy)
tail -f /var/log/nginx/access.log
```

### **Métricas a Monitorar**
- ⚡ Taxa de upload/download
- 📊 Uso de storage
- 🚨 Tentativas de acesso negadas
- 📈 Performance da API

## 🚫 **Políticas de Bucket MinIO**

### **Exemplo de Política Restritiva**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": ["arn:aws:iam::*:user/upload-tecnomyl"]
      },
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject"
      ],
      "Resource": ["arn:aws:s3:::tecnomyl/produtos/*"]
    }
  ]
}
```

## 🔄 **Backup e Recuperação**

### **Estratégia de Backup**
1. **Backup diário** dos arquivos MinIO
2. **Backup semanal** da configuração
3. **Teste mensal** de recuperação
4. **Retenção de 30 dias** mínimo

### **Script de Backup**
```bash
#!/bin/bash
# Backup MinIO
mc mirror tecnomyl backup/$(date +%Y-%m-%d)
# Backup configuração
tar -czf config-backup-$(date +%Y-%m-%d).tar.gz backend/.env
```

## 🆘 **Incidente de Segurança**

### **Se credenciais forem expostas:**

1. **IMEDIATAMENTE:**
   - 🔄 Altere todas as credenciais MinIO
   - 🔄 Regenere tokens de API
   - 🔄 Revogue acessos comprometidos

2. **ANÁLISE:**
   - 📋 Verifique logs de acesso
   - 📋 Identifique arquivos acessados
   - 📋 Documente o incidente

3. **CORREÇÃO:**
   - 🔧 Implemente melhorias de segurança
   - 🔧 Atualize políticas de acesso
   - 🔧 Treine equipe

## 📞 **Contatos de Segurança**

- **Admin Sistema**: [seu-email@tecnomyl.com]
- **Emergency**: [emergencia@tecnomyl.com]
- **MinIO Support**: [se aplicável]

---

## ⚡ **Checklist Pré-Deploy**

- [ ] Credenciais padrão alteradas
- [ ] Arquivos `.env` configurados
- [ ] HTTPS configurado
- [ ] CORS configurado
- [ ] Backup strategy implementada
- [ ] Monitoramento ativo
- [ ] Logs configurados
- [ ] Testes de segurança realizados

---

🔐 **Lembre-se: Segurança não é opcional, é fundamental!** 