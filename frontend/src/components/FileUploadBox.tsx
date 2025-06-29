import React, { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { FileType, FILE_TYPE_LABELS, UploadedFile } from '../types';

interface FileUploadBoxProps {
  fileType: FileType;
  uploadedFile?: UploadedFile;
  onFileSelect: (file: File, fileType: FileType) => void;
  onFileRemove: (fileType: FileType) => void;
}

const FileUploadBox: React.FC<FileUploadBoxProps> = ({
  fileType,
  uploadedFile,
  onFileSelect,
  onFileRemove,
}) => {
  const onDrop = useCallback(
    (acceptedFiles: File[]) => {
      if (acceptedFiles.length > 0) {
        onFileSelect(acceptedFiles[0], fileType);
      }
    },
    [fileType, onFileSelect]
  );

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
    },
    maxFiles: 1,
    maxSize: 10 * 1024 * 1024, // 10MB
  });

  const handleRemoveFile = (e: React.MouseEvent) => {
    e.stopPropagation();
    onFileRemove(fileType);
  };

  const formatFileSize = (bytes: number): string => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  return (
    <div className="w-full">
      <label className="block text-sm font-medium text-gray-700 mb-2">
        {FILE_TYPE_LABELS[fileType]}
      </label>
      
      <div
        {...getRootProps()}
        className={`
          border-2 border-dashed rounded-lg p-6 text-center cursor-pointer transition-colors
          ${isDragActive 
            ? 'border-tecnomyl-primary bg-tecnomyl-light' 
            : uploadedFile 
              ? 'border-green-400 bg-green-50' 
              : 'border-gray-300 hover:border-tecnomyl-secondary'
          }
        `}
      >
        <input {...getInputProps()} />
        
        {uploadedFile ? (
          <div className="space-y-3">
            <div className="flex items-center justify-center">
              <svg className="w-12 h-12 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            
            <div className="text-sm text-gray-600">
              <p className="font-medium text-gray-900">{uploadedFile.file.name}</p>
              <p>{formatFileSize(uploadedFile.file.size)}</p>
            </div>
            
            <button
              onClick={handleRemoveFile}
              className="inline-flex items-center px-3 py-1 text-xs bg-red-100 text-red-700 rounded-full hover:bg-red-200 transition-colors"
            >
              <svg className="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
              Remover
            </button>
          </div>
        ) : (
          <div className="space-y-3">
            <div className="flex items-center justify-center">
              <svg className="w-12 h-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
              </svg>
            </div>
            
            <div className="text-sm text-gray-600">
              {isDragActive ? (
                <p className="text-tecnomyl-primary font-medium">Solte o arquivo aqui...</p>
              ) : (
                <div>
                  <p className="font-medium text-gray-900">
                    Arraste o arquivo PDF aqui
                  </p>
                  <p>ou clique para selecionar</p>
                  <p className="text-xs text-gray-500 mt-1">
                    Máximo 10MB
                  </p>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default FileUploadBox; 