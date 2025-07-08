import os
from typing import List
from dotenv import load_dotenv

# Carregar variáveis do arquivo .env
load_dotenv()

# Verificar se as variáveis obrigatórias estão definidas
required_env_vars = [
    'MINIO_ENDPOINT',
    'MINIO_ACCESS_KEY', 
    'MINIO_SECRET_KEY',
    'MINIO_BUCKET'
]

missing_vars = [var for var in required_env_vars if not os.getenv(var)]
if missing_vars:
    raise ValueError(f"Variáveis de ambiente obrigatórias não encontradas: {', '.join(missing_vars)}. "
                     f"Copie o arquivo 'env-example' para '.env' e configure suas credenciais.")

# MinIO Configuration
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY")
MINIO_SECURE = os.getenv("MINIO_SECURE", "False").lower() == "true"
MINIO_BUCKET = os.getenv("MINIO_BUCKET")

# API Configuration
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8000"))
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")

# Lista fixa de produtos da Tecnomyl
PRODUTOS: List[str] = [
    "2,4D_TECNOMYL",
    "ADVER",
    "ARCEUS",
    "AVERT_MAX",
    "CETRIX_200",
    "DAGA",
    "FECYD_E",
    "FOCKER",
    "JUDOKA_SUPER_250_CS",
    "LANEX_800_WG",
    "LOYER_200_TM",
    "ONEFIX",
    "ORSA_400_EC",
    "PASTOR",
    "PROSOY",
    "PROSOY_TRIO",
    "RESIL",
    "SANDAL_200_SP",
    "SUMMIT_FS",
    "TECNOMYL_PRO"
    "TECNUP_MAX_720",
    "TEMIBLE",
    "TENNOX",
    "TOPINAM",
    "TRIPLEC",
    "TRIZEB",
    "VALLEX",
    "VIANCE",

]

# Tipos de arquivo permitidos
TIPOS_ARQUIVO = ["bula", "FISPQ", "Ficha_de_Emergencia"]

# Configurações de upload
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_EXTENSIONS = [".pdf"]

# Authentication Configuration (Single User)
AUTH_USERNAME = os.getenv("AUTH_USERNAME", "admin")
AUTH_PASSWORD = os.getenv("AUTH_PASSWORD", "admin123")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "sua-chave-secreta-aqui-muito-longa-e-segura-para-jwt")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRE_HOURS = int(os.getenv("JWT_EXPIRE_HOURS", "24")) 