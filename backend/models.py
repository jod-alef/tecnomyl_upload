from pydantic import BaseModel
from typing import Optional, List


class LoginRequest(BaseModel):
    username: str
    password: str


class LoginResponse(BaseModel):
    success: bool
    message: str
    token: Optional[str] = None
    expires_in_hours: Optional[int] = None


class UploadResponse(BaseModel):
    success: bool
    message: str
    file_urls: Optional[List[str]] = None


class ProductInfo(BaseModel):
    name: str
    files: Optional[dict] = None


class FileInfo(BaseModel):
    filename: str
    url: str
    size: int
    last_modified: Optional[str] = None


class UploadStatus(BaseModel):
    produto: str
    bula: Optional[FileInfo] = None
    fispq: Optional[FileInfo] = None
    ficha_emergencia: Optional[FileInfo] = None 