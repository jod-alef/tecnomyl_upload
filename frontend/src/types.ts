export interface UploadResponse {
  success: boolean;
  message: string;
  file_urls?: string[];
}

export interface FileInfo {
  filename: string;
  url: string;
  size: number;
  last_modified?: string;
}

export interface UploadStatus {
  produto: string;
  bula?: FileInfo;
  fispq?: FileInfo;
  ficha_emergencia?: FileInfo;
}

export interface UploadedFile {
  file: File;
  preview?: string;
}

export interface FileUploads {
  bula?: UploadedFile;
  fispq?: UploadedFile;
  ficha_emergencia?: UploadedFile;
}

export type FileType = 'bula' | 'fispq' | 'ficha_emergencia';

export const FILE_TYPE_LABELS: Record<FileType, string> = {
  bula: 'Bula',
  fispq: 'FISPQ',
  ficha_emergencia: 'Ficha de Emergência'
}; 