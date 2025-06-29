from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List, Optional
import logging
import uvicorn

from config import PRODUTOS, TIPOS_ARQUIVO, MAX_FILE_SIZE, ALLOWED_EXTENSIONS, CORS_ORIGINS, API_HOST, API_PORT, JWT_EXPIRE_HOURS
from models import UploadResponse, ProductInfo, UploadStatus, FileInfo, LoginRequest, LoginResponse
from minio_client import minio_client
from auth import auth, RequireAuth

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicialização do FastAPI
app = FastAPI(
    title="Upload Tecnomyl API",
    description="API para upload de arquivos da Tecnomyl para MinIO",
    version="1.0.0"
)

# Configuração CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def validate_file(file: UploadFile) -> None:
    """Valida o arquivo enviado"""
    # Verifica se é PDF
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Apenas arquivos PDF são permitidos")
    
    # Verifica tamanho (FastAPI já faz isso automaticamente, mas podemos adicionar validação customizada)
    if file.size and file.size > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail=f"Arquivo muito grande. Máximo permitido: {MAX_FILE_SIZE/1024/1024}MB")


@app.get("/")
async def root():
    """Endpoint de teste da API"""
    return {"message": "Upload Tecnomyl API está funcionando!"}


@app.post("/api/login", response_model=LoginResponse)
async def login(credentials: LoginRequest):
    """Endpoint de login simples"""
    
    if credentials.username != auth.username:
        raise HTTPException(
            status_code=401, 
            detail="Usuário ou senha incorretos"
        )
    
    if not auth.verify_password(credentials.password):
        raise HTTPException(
            status_code=401, 
            detail="Usuário ou senha incorretos"
        )
    
    # Gerar token
    token = auth.create_access_token()
    
    return LoginResponse(
        success=True,
        message="Login realizado com sucesso",
        token=token,
        expires_in_hours=JWT_EXPIRE_HOURS
    )


@app.get("/api/products", response_model=List[str])
async def get_products():
    """Retorna lista de produtos disponíveis"""
    return PRODUTOS


@app.get("/api/file-types", response_model=List[str])
async def get_file_types():
    """Retorna tipos de arquivo aceitos"""
    return TIPOS_ARQUIVO


@app.post("/api/upload/{produto}", response_model=UploadResponse)
async def upload_files(
    produto: str,
    current_user: str = RequireAuth,
    bula: Optional[UploadFile] = File(None),
    fispq: Optional[UploadFile] = File(None),
    ficha_emergencia: Optional[UploadFile] = File(None)
):
    """
    Upload de arquivos para um produto específico
    
    Args:
        produto: Nome do produto (deve estar na lista de produtos)
        bula: Arquivo PDF da bula
        fispq: Arquivo PDF do FISPQ
        ficha_emergencia: Arquivo PDF da ficha de emergência
    """
    
    # Validar se produto existe
    if produto not in PRODUTOS:
        raise HTTPException(status_code=400, detail=f"Produto '{produto}' não encontrado na lista")
    
    files_map = {
        "bula": bula,
        "FISPQ": fispq,
        "Ficha_de_Emergencia": ficha_emergencia
    }
    
    # Verificar se pelo menos um arquivo foi enviado
    uploaded_files = {k: v for k, v in files_map.items() if v is not None}
    if not uploaded_files:
        raise HTTPException(status_code=400, detail="Pelo menos um arquivo deve ser enviado")
    
    uploaded_urls = []
    successful_uploads = []
    
    try:
        for tipo_arquivo, file in uploaded_files.items():
            # Validar arquivo
            validate_file(file)
            
            # Ler conteúdo do arquivo
            file_content = await file.read()
            
            # Gerar nome do objeto no MinIO
            object_name = minio_client.generate_object_name(produto, tipo_arquivo)
            
            # Fazer upload para MinIO
            success = minio_client.upload_file(file_content, object_name)
            
            if success:
                file_url = minio_client.get_file_url(object_name)
                uploaded_urls.append(file_url)
                successful_uploads.append(tipo_arquivo)
                logger.info(f"Upload realizado com sucesso: {object_name}")
            else:
                logger.error(f"Falha no upload: {object_name}")
                raise HTTPException(status_code=500, detail=f"Falha no upload do arquivo {tipo_arquivo}")
        
        return UploadResponse(
            success=True,
            message=f"Upload realizado com sucesso para {len(successful_uploads)} arquivo(s) do produto {produto}",
            file_urls=uploaded_urls
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro no upload: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro interno no servidor: {str(e)}")


@app.get("/api/status/{produto}", response_model=UploadStatus)
async def get_product_status(produto: str):
    """
    Verifica o status dos arquivos de um produto
    
    Args:
        produto: Nome do produto
    """
    
    if produto not in PRODUTOS:
        raise HTTPException(status_code=400, detail=f"Produto '{produto}' não encontrado na lista")
    
    status = UploadStatus(produto=produto)
    
    # Verificar cada tipo de arquivo
    for tipo_arquivo in TIPOS_ARQUIVO:
        object_name = minio_client.generate_object_name(produto, tipo_arquivo)
        file_info = minio_client.get_file_info(object_name)
        
        if file_info:
            file_obj = FileInfo(**file_info)
            
            if tipo_arquivo == "bula":
                status.bula = file_obj
            elif tipo_arquivo == "FISPQ":
                status.fispq = file_obj
            elif tipo_arquivo == "Ficha_de_Emergencia":
                status.ficha_emergencia = file_obj
    
    return status


@app.get("/api/wordpress/product-files/{produto}")
async def get_wordpress_files(produto: str):
    """
    Endpoint específico para integração com WordPress
    Retorna URLs dos arquivos em formato compatível
    """
    
    if produto not in PRODUTOS:
        raise HTTPException(status_code=404, detail=f"Produto '{produto}' não encontrado")
    
    files = {}
    
    for tipo_arquivo in TIPOS_ARQUIVO:
        object_name = minio_client.generate_object_name(produto, tipo_arquivo)
        
        if minio_client.check_file_exists(object_name):
            files[tipo_arquivo.lower()] = minio_client.get_file_url(object_name)
    
    return {
        "produto": produto,
        "files": files,
        "total_files": len(files)
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Testa conexão com MinIO
        bucket_exists = minio_client.client.bucket_exists(minio_client.bucket_name)
        return {
            "status": "healthy",
            "minio_connected": bucket_exists,
            "bucket": minio_client.bucket_name
        }
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "error": str(e)
            }
        )


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=API_HOST,
        port=API_PORT,
        reload=True,
        log_level="info"
    ) 