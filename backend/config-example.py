# Exemplo de configuração para o Upload Tecnomyl
# Copie este arquivo para config.py e ajuste conforme necessário

import os
from typing import List

# MinIO Configuration
MINIO_ENDPOINT = "localhost:9000"  # Seu endpoint MinIO
MINIO_ACCESS_KEY = "minioadmin"    # Sua access key
MINIO_SECRET_KEY = "minioadmin"    # Sua secret key
MINIO_SECURE = False               # True para HTTPS, False para HTTP
MINIO_BUCKET = "tecnomyl"          # Nome do bucket

# API Configuration
API_HOST = "0.0.0.0"
API_PORT = 8000
CORS_ORIGINS = ["http://localhost:3000"]  # URLs permitidas para CORS

# Lista de produtos da Tecnomyl
# CUSTOMIZE ESTA LISTA COM SEUS PRODUTOS REAIS
PRODUTOS: List[str] = [
    "PRODUTO_EXEMPLO_1",
    "PRODUTO_EXEMPLO_2", 
    "PRODUTO_EXEMPLO_3",
    # Adicione seus produtos aqui...
]

# Tipos de arquivo permitidos (NÃO ALTERAR)
TIPOS_ARQUIVO = ["bula", "FISPQ", "Ficha_de_Emergencia"]

# Configurações de upload
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_EXTENSIONS = [".pdf"] 