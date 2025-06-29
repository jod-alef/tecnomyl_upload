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
    "DAGA",
    "TECNUP_MAX_720",
    "LOYER_200_TM",
    "PASTOR",
    "TOPINAM",
    "VIANCE",
    "ADVER",
    "ARCEUS",
    "CETRIX_200",
    "FECYD_E",
    "FOCKER",
    "JUDOKA_SUPER_250_CS",
    "LANEX_800_WG",
    "ORSA_400_EC",
    "SANDAL_200_SP",
    "SUMMIT_FS",
    "TEMIBLE",
    "VALLEX",
    "AVERT_MAX"
    "RESIL"
    "TRIZEB"
    "TRIPLEC"
    "ONEFIX"
]

# Tipos de arquivo permitidos
TIPOS_ARQUIVO = ["bula", "FISPQ", "Ficha_de_Emergencia"]

# Configurações de upload
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_EXTENSIONS = [".pdf"] 