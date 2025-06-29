# 🔐 NOVAS VARIÁVEIS DE AUTENTICAÇÃO - COOLIFY

## ⚡ Ação Necessária: Adicionar estas 5 variáveis no Backend do Coolify

### 📋 Lista das Novas Variáveis:

```bash
# 1. Nome de usuário para login
AUTH_USERNAME=admin

# 2. Senha para login (DEFINA UMA SENHA FORTE!)
AUTH_PASSWORD=SuaSenhaSeguraAqui123!

# 3. Chave secreta JWT (USE A CHAVE GERADA ABAIXO)
JWT_SECRET_KEY=OazsK2bJAWCxMZ8oHVFEtbpQ7yxuTaenoRiy79k5GlzuWbR81WYBoBLRqKKCgXTDbsGMEXM9K3h_sYitNsScUQ

# 4. Algoritmo JWT (manter como está)
JWT_ALGORITHM=HS256

# 5. Expiração do token em horas (24h = 1 dia)
JWT_EXPIRE_HOURS=24
```

---

## 🚀 Passos no Coolify:

1. **Acesse o painel do Coolify**
2. **Vá para o serviço Backend**
3. **Na aba "Environment"**, adicione as 5 variáveis acima
4. **Clique em "Save" ou "Deploy"** para aplicar

---

## 🔑 Credenciais de Login:

Após configurar, o login será:
- **Usuário:** `admin`
- **Senha:** `SuaSenhaSeguraAqui123!` (ou a que você definir)

---

## ⚠️ IMPORTANTE:

1. **Mude a senha padrão** - Use uma senha forte e única
2. **A chave JWT já está gerada** - Pode usar a fornecida acima
3. **Redeploy obrigatório** - Após adicionar as variáveis, faça redeploy do backend
4. **Teste o login** - Acesse o frontend e teste com as credenciais

---

## 🔧 Gerar Nova Chave JWT (Opcional):

Se quiser gerar sua própria chave:
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(64))"
```

---

**✅ Depois de configurar essas variáveis e fazer redeploy, o sistema de login estará funcionando!** 