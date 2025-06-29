# Variáveis de Ambiente - Coolify

## Configuração para Deployment no Coolify

### Variáveis Obrigatórias para o Backend:

#### MinIO Configuration
```
MINIO_ENDPOINT=seu-servidor-minio.com:9000
MINIO_ACCESS_KEY=sua_access_key_minio
MINIO_SECRET_KEY=sua_secret_key_minio
MINIO_SECURE=false
MINIO_BUCKET=tecnomyl
```

#### CORS Configuration
```
CORS_ORIGINS=https://uploadtecnomyl.alef.host
```

#### Authentication (Single User) - **NOVAS VARIÁVEIS**
```
AUTH_USERNAME=admin
AUTH_PASSWORD=SuaSenhaSeguraAqui123!
JWT_SECRET_KEY=sua-chave-jwt-muito-longa-e-segura-de-pelo-menos-64-caracteres-aqui
JWT_ALGORITHM=HS256
JWT_EXPIRE_HOURS=24
```

### Variáveis para o Frontend (Build Args):

```
REACT_APP_API_URL=https://api-uploadtecnomyl.alef.host
```

---

## Como Gerar JWT_SECRET_KEY Segura

Execute este comando no terminal para gerar uma chave segura:

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(64))"
```

Ou use este comando online: https://generate-secret.vercel.app/64

**Exemplo de chave gerada:**
```
JWT_SECRET_KEY=OazsK2bJAWCxMZ8oHVFEtbpQ7yxuTaenoRiy79k5GlzuWbR81WYBoBLRqKKCgXTDbsGMEXM9K3h_sYitNsScUQ
```

---

## Configuração Completa no Coolify

### Passo 1: No painel do Coolify, adicione todas as variáveis de ambiente:

**Backend Service:**
- `MINIO_ENDPOINT`: `seu-servidor-minio.com:9000`
- `MINIO_ACCESS_KEY`: `sua_access_key_minio`
- `MINIO_SECRET_KEY`: `sua_secret_key_minio`
- `MINIO_SECURE`: `false`
- `MINIO_BUCKET`: `tecnomyl`
- `CORS_ORIGINS`: `https://uploadtecnomyl.alef.host`
- `AUTH_USERNAME`: `admin`
- `AUTH_PASSWORD`: `SuaSenhaSeguraAqui123!`
- `JWT_SECRET_KEY`: `[sua chave gerada de 64+ caracteres]`
- `JWT_ALGORITHM`: `HS256`
- `JWT_EXPIRE_HOURS`: `24`

**Frontend Service:**
- `REACT_APP_API_URL`: `https://api-uploadtecnomyl.alef.host`

### Passo 2: Redeploy dos serviços

Após adicionar as variáveis, faça redeploy de ambos os serviços para aplicar as mudanças.

---

## Credenciais de Login

Com as variáveis configuradas, o login será:
- **Usuário:** `admin` (ou o valor de AUTH_USERNAME)
- **Senha:** A senha definida em AUTH_PASSWORD

---

## Segurança

⚠️ **IMPORTANTE:**
1. Use uma senha forte para `AUTH_PASSWORD`
2. Gere uma `JWT_SECRET_KEY` única e segura (64+ caracteres)
3. Nunca compartilhe essas credenciais em repositórios públicos
4. Considere usar um gerenciador de senhas para armazenar essas informações

---

## Troubleshooting

Se o login não funcionar:
1. Verifique se todas as variáveis foram adicionadas no Coolify
2. Confirme que o redeploy foi feito após adicionar as variáveis
3. Verifique os logs do backend para erros de autenticação
4. Teste o endpoint `/health` para confirmar que o backend está funcionando 