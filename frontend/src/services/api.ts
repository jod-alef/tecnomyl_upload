import axios from 'axios';
import { UploadResponse, UploadStatus, FileUploads } from '../types';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // 30 segundos para uploads
});

// Interceptor para adicionar token automaticamente
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('auth_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Interceptor para tratar erros de autenticação
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('auth_token');
      window.location.href = '/';
    }
    return Promise.reject(error);
  }
);

export const apiService = {
  // Fazer login
  async login(username: string, password: string): Promise<any> {
    const response = await api.post('/api/login', { username, password });
    return response.data;
  },

  // Buscar lista de produtos
  async getProducts(): Promise<string[]> {
    const response = await api.get('/api/products');
    return response.data;
  },

  // Fazer upload de arquivos
  async uploadFiles(produto: string, files: FileUploads): Promise<UploadResponse> {
    const formData = new FormData();
    
    if (files.bula) {
      formData.append('bula', files.bula.file);
    }
    if (files.fispq) {
      formData.append('fispq', files.fispq.file);
    }
    if (files.ficha_emergencia) {
      formData.append('ficha_emergencia', files.ficha_emergencia.file);
    }

    const response = await api.post(`/api/upload/${produto}`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      onUploadProgress: (progressEvent) => {
        if (progressEvent.total) {
          const percentCompleted = Math.round(
            (progressEvent.loaded * 100) / progressEvent.total
          );
          console.log(`Upload progress: ${percentCompleted}%`);
        }
      },
    });

    return response.data;
  },

  // Buscar status dos arquivos de um produto
  async getProductStatus(produto: string): Promise<UploadStatus> {
    const response = await api.get(`/api/status/${produto}`);
    return response.data;
  },

  // Health check da API
  async healthCheck(): Promise<any> {
    const response = await api.get('/health');
    return response.data;
  },
};

export default apiService; 