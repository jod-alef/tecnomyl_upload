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
    "ACARIGEN",
    "ADVER_240_SC",
    "AMPLUS",
    "ARCEUS",
    "ATRIVO",
    "AVERT",
    "AVERT_MAX",
    "BORO_10",
    "CAPEX",
    "CETRIX_200",
    "DAGA",
    "DESALI",
    "DITOR",
    "DUMPER",    
    "EFICAX",
    "ERRADICUR",
    "FAVORITO",
    "FECYD_E",
    "FLUID_MAX",
    "FOCKER",
    "FURIOSO",
    "GRANO_K",
    "GUNTER",
    "GUNTER_PRO_360",
    "HALEB",
    "HAMPTON_400_EC",
    "JUDOKA",
    "JUDOKA_SUPER_250_CS",
    "LANEX_800_WG",
    "LEGATUS",
    "LISOR",
    "LITUS",
    "LOYER_200_TM",
    "MAGMA_500_SC",
    "MARKUP",
    "MATTOR",
    "MAUSER_500_SC",
    "METHOS",
    "NS_11_25",
    "ONEFIX",
    "ORSA_400_EC",
    "PASTOR",
    "PLATINUM_NEO",
    "PROSOY",
    "PROSOY_TRIO",
    "PROTEIN_+NI",
    "RAISOR",
    "RAINIL",
    "RESIL",
    "RESPECTOR",
    "SANDAL_200_SP",
    "SEMMER",
    "SPILL_DROP",
    "SPILL_FIX",
    "SPRAY_CLEAN",
    "SUMMIT_250_FS",
    "TECNOSOLO_B10",
    "TECNOSOLO_S90",
    "TECNUP",
    "TECNUP_MAX_720",
    "TECNUP_PREMIUM",
    "TECNUP_SUPER_608",
    "TEMIBLE",
    "TENNOX",
    "TOPINAM",
    "TRIPLEC",
    "TRIZEB",
    "TRUDOR",
    "VALLEX",
    "VALLEX_FULL",
    "VELLSAN",
    "VERSO",
    "VIANCE",
    "VITTARIUM",
    "ZAPAR",
    "ZN_XTRA",

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