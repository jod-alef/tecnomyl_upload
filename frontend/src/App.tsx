import React, { useState, useEffect } from 'react';
import ProductSelector from './components/ProductSelector';
import FileUploadBox from './components/FileUploadBox';
import { FileUploads, FileType, UploadedFile } from './types';
import { apiService } from './services/api';
import './App.css';

function App() {
  // Estados
  const [products, setProducts] = useState<string[]>([]);
  const [selectedProduct, setSelectedProduct] = useState<string>('');
  const [uploadedFiles, setUploadedFiles] = useState<FileUploads>({});
  const [loading, setLoading] = useState<boolean>(false);
  const [uploading, setUploading] = useState<boolean>(false);
  const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);

  // Carregar produtos na inicialização
  useEffect(() => {
    loadProducts();
  }, []);

  const loadProducts = async () => {
    try {
      setLoading(true);
      const productList = await apiService.getProducts();
      setProducts(productList);
    } catch (error) {
      console.error('Erro ao carregar produtos:', error);
      setMessage({ type: 'error', text: 'Erro ao carregar lista de produtos' });
    } finally {
      setLoading(false);
    }
  };

  const handleProductChange = (product: string) => {
    setSelectedProduct(product);
    // Limpar arquivos quando mudar de produto
    setUploadedFiles({});
    setMessage(null);
  };

  const handleFileSelect = (file: File, fileType: FileType) => {
    const uploadedFile: UploadedFile = {
      file,
      preview: URL.createObjectURL(file),
    };

    setUploadedFiles(prev => ({
      ...prev,
      [fileType]: uploadedFile,
    }));

    setMessage(null);
  };

  const handleFileRemove = (fileType: FileType) => {
    setUploadedFiles(prev => {
      const newFiles = { ...prev };
      if (newFiles[fileType]?.preview) {
        URL.revokeObjectURL(newFiles[fileType]!.preview!);
      }
      delete newFiles[fileType];
      return newFiles;
    });
  };

  const handleUpload = async () => {
    if (!selectedProduct) {
      setMessage({ type: 'error', text: 'Selecione um produto antes de fazer upload' });
      return;
    }

    const fileCount = Object.keys(uploadedFiles).length;
    if (fileCount === 0) {
      setMessage({ type: 'error', text: 'Selecione pelo menos um arquivo para upload' });
      return;
    }

    try {
      setUploading(true);
      setMessage(null);

      const response = await apiService.uploadFiles(selectedProduct, uploadedFiles);

      if (response.success) {
        setMessage({ type: 'success', text: response.message });
        // Limpar arquivos após upload bem-sucedido
        setUploadedFiles({});
      } else {
        setMessage({ type: 'error', text: response.message || 'Erro no upload' });
      }
    } catch (error: any) {
      console.error('Erro no upload:', error);
      const errorMessage = error.response?.data?.detail || 'Erro ao fazer upload dos arquivos';
      setMessage({ type: 'error', text: errorMessage });
    } finally {
      setUploading(false);
    }
  };

  const dismissMessage = () => {
    setMessage(null);
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      {/* Header */}
      <header className="bg-tecnomyl-green shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-4">
              <img 
                src="/logo_horizontal_tecnomyl.png" 
                alt="Tecnomyl Logo" 
                className="h-10 w-auto object-contain"
              />
              <div className="h-6 w-px bg-white bg-opacity-30"></div>
              <h1 className="text-xl font-bold text-white">Upload de Arquivos</h1>
            </div>
            <div className="text-sm text-white text-opacity-90">
              Sistema de gestão de documentos
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 max-w-4xl mx-auto py-8 px-4 sm:px-6 lg:px-8 w-full">
        <div className="bg-white rounded-lg shadow-sm border p-6 space-y-8">
          
          {/* Título e Descrição */}
          <div className="text-center">
            <h2 className="text-2xl font-bold text-gray-900 mb-2">
              Upload de Arquivos
            </h2>
            <p className="text-gray-600">
              Selecione um produto e faça upload dos arquivos PDF (Bula, FISPQ e Ficha de Emergência)
            </p>
          </div>

          {/* Mensagem de Status */}
          {message && (
            <div className={`
              relative p-4 rounded-lg border
              ${message.type === 'success' 
                ? 'bg-green-50 border-green-200 text-green-800' 
                : 'bg-red-50 border-red-200 text-red-800'
              }
            `}>
              <div className="flex items-center justify-between">
                <div className="flex items-center">
                  {message.type === 'success' ? (
                    <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                    </svg>
                  ) : (
                    <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  )}
                  <span>{message.text}</span>
                </div>
                <button
                  onClick={dismissMessage}
                  className="text-gray-400 hover:text-gray-600"
                >
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
            </div>
          )}

          {/* Seletor de Produto */}
          <ProductSelector
            products={products}
            selectedProduct={selectedProduct}
            onProductChange={handleProductChange}
            loading={loading}
          />

          {/* Upload de Arquivos */}
          {selectedProduct && (
            <div className="space-y-6">
              <div className="border-t pt-6">
                <h3 className="text-lg font-medium text-gray-900 mb-4">
                  Arquivos do Produto
                </h3>
                
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                  <FileUploadBox
                    fileType="bula"
                    uploadedFile={uploadedFiles.bula}
                    onFileSelect={handleFileSelect}
                    onFileRemove={handleFileRemove}
                  />
                  
                  <FileUploadBox
                    fileType="fispq"
                    uploadedFile={uploadedFiles.fispq}
                    onFileSelect={handleFileSelect}
                    onFileRemove={handleFileRemove}
                  />
                  
                  <FileUploadBox
                    fileType="ficha_emergencia"
                    uploadedFile={uploadedFiles.ficha_emergencia}
                    onFileSelect={handleFileSelect}
                    onFileRemove={handleFileRemove}
                  />
                </div>
              </div>

              {/* Botão de Upload */}
              <div className="border-t pt-6">
                <div className="flex justify-center">
                  <button
                    onClick={handleUpload}
                    disabled={uploading || Object.keys(uploadedFiles).length === 0}
                    className={`
                      px-8 py-3 rounded-lg font-medium text-white text-base
                      transition-colors duration-200 min-w-200
                      ${uploading || Object.keys(uploadedFiles).length === 0
                        ? 'bg-gray-400 cursor-not-allowed'
                        : 'bg-tecnomyl-primary hover:bg-tecnomyl-dark focus:ring-2 focus:ring-tecnomyl-primary focus:ring-offset-2'
                      }
                    `}
                  >
                    {uploading ? (
                      <div className="flex items-center justify-center">
                        <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                        Enviando...
                      </div>
                    ) : (
                      `Fazer Upload (${Object.keys(uploadedFiles).length} arquivo${Object.keys(uploadedFiles).length !== 1 ? 's' : ''})`
                    )}
                  </button>
                </div>
                
                {Object.keys(uploadedFiles).length > 0 && (
                  <p className="text-center text-sm text-gray-500 mt-3">
                    Os arquivos serão automaticamente renomeados para seguir o padrão da Tecnomyl
                  </p>
                )}
              </div>
            </div>
          )}
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t bg-gray-600">
        <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col md:flex-row items-center justify-between">
            <div className="flex items-center space-x-2 mb-4 md:mb-0">
              <img 
                src="/logo_horizontal_tecnomyl.png" 
                alt="Tecnomyl" 
                className="h-6 w-auto object-contain opacity-80"
              />
              <span className="text-sm text-gray-200">Sistema de Upload de Arquivos</span>
            </div>
            <div className="text-center md:text-right">
              <p className="text-sm text-gray-200">
                &copy; 2024 Tecnomyl. Todos os direitos reservados.
              </p>
              <p className="text-xs text-gray-300 mt-1">
                Versão 1.0 - Gestão de Documentos
              </p>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;
