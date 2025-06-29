from minio import Minio
from minio.error import S3Error
import io
from typing import Optional, Tuple
import logging
from config import (
    MINIO_ENDPOINT, MINIO_ACCESS_KEY, MINIO_SECRET_KEY, 
    MINIO_SECURE, MINIO_BUCKET
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MinIOClient:
    def __init__(self):
        self.client = Minio(
            MINIO_ENDPOINT,
            access_key=MINIO_ACCESS_KEY,
            secret_key=MINIO_SECRET_KEY,
            secure=MINIO_SECURE
        )
        self.bucket_name = MINIO_BUCKET
        self._ensure_bucket_exists()

    def _ensure_bucket_exists(self):
        """Garante que o bucket existe"""
        try:
            if not self.client.bucket_exists(self.bucket_name):
                self.client.make_bucket(self.bucket_name)
                logger.info(f"Bucket '{self.bucket_name}' criado com sucesso")
            else:
                logger.info(f"Bucket '{self.bucket_name}' já existe")
        except S3Error as e:
            logger.error(f"Erro ao verificar/criar bucket: {e}")
            raise

    def upload_file(self, file_content: bytes, object_name: str, content_type: str = "application/pdf") -> bool:
        """
        Faz upload de um arquivo para o MinIO
        
        Args:
            file_content: Conteúdo do arquivo em bytes
            object_name: Nome do objeto no bucket (caminho/nome_arquivo.pdf)
            content_type: Tipo MIME do arquivo
            
        Returns:
            bool: True se sucesso, False caso contrário
        """
        try:
            file_stream = io.BytesIO(file_content)
            
            self.client.put_object(
                bucket_name=self.bucket_name,
                object_name=object_name,
                data=file_stream,
                length=len(file_content),
                content_type=content_type
            )
            
            logger.info(f"Arquivo '{object_name}' enviado com sucesso")
            return True
            
        except S3Error as e:
            logger.error(f"Erro ao fazer upload do arquivo '{object_name}': {e}")
            return False

    def get_file_url(self, object_name: str) -> str:
        """
        Gera URL pública para o arquivo
        
        Args:
            object_name: Nome do objeto no bucket
            
        Returns:
            str: URL pública do arquivo
        """
        if MINIO_SECURE:
            protocol = "https"
        else:
            protocol = "http"
            
        return f"{protocol}://{MINIO_ENDPOINT}/{self.bucket_name}/{object_name}"

    def check_file_exists(self, object_name: str) -> bool:
        """
        Verifica se um arquivo existe no bucket
        
        Args:
            object_name: Nome do objeto no bucket
            
        Returns:
            bool: True se existe, False caso contrário
        """
        try:
            self.client.stat_object(self.bucket_name, object_name)
            return True
        except S3Error:
            return False

    def get_file_info(self, object_name: str) -> Optional[dict]:
        """
        Obtém informações de um arquivo no bucket
        
        Args:
            object_name: Nome do objeto no bucket
            
        Returns:
            dict: Informações do arquivo ou None se não existe
        """
        try:
            stat = self.client.stat_object(self.bucket_name, object_name)
            return {
                "filename": object_name.split("/")[-1],
                "size": stat.size,
                "last_modified": stat.last_modified.isoformat() if stat.last_modified else None,
                "url": self.get_file_url(object_name)
            }
        except S3Error:
            return None

    def generate_object_name(self, produto: str, tipo_arquivo: str) -> str:
        """
        Gera o nome padronizado do objeto no bucket
        
        Args:
            produto: Nome do produto
            tipo_arquivo: Tipo do arquivo (bula, FISPQ, Ficha_de_Emergencia)
            
        Returns:
            str: Nome do objeto no formato produtos/{produto}/{produto}_{tipo}.pdf
        """
        return f"produtos/{produto}/{produto}_{tipo_arquivo}.pdf"


# Instância global do cliente MinIO
minio_client = MinIOClient() 