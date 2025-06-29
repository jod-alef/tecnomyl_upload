from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext
import logging

from config import AUTH_USERNAME, AUTH_PASSWORD, JWT_SECRET_KEY, JWT_ALGORITHM, JWT_EXPIRE_HOURS

logger = logging.getLogger(__name__)

# Configuração para hash de senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configuração do bearer token
security = HTTPBearer()


class SimpleAuth:
    def __init__(self):
        self.username = AUTH_USERNAME
        self.password_hash = pwd_context.hash(AUTH_PASSWORD)
    
    def verify_password(self, plain_password: str) -> bool:
        """Verifica se a senha está correta"""
        return pwd_context.verify(plain_password, self.password_hash)
    
    def create_access_token(self) -> str:
        """Cria um token JWT"""
        expire = datetime.utcnow() + timedelta(hours=JWT_EXPIRE_HOURS)
        data = {
            "sub": self.username,
            "exp": expire,
            "iat": datetime.utcnow()
        }
        
        encoded_jwt = jwt.encode(data, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
        return encoded_jwt
    
    def verify_token(self, token: str) -> bool:
        """Verifica se o token JWT é válido"""
        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
            username: str = payload.get("sub")
            
            if username != self.username:
                return False
                
            return True
            
        except JWTError as e:
            logger.warning(f"Token JWT inválido: {e}")
            return False


# Instância global
auth = SimpleAuth()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """Dependency para verificar autenticação"""
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    if not credentials:
        raise credentials_exception
    
    if not auth.verify_token(credentials.credentials):
        raise credentials_exception
    
    return auth.username


# Dependency opcional (pode ser usado para rotas que precisam de auth)
RequireAuth = Depends(get_current_user) 