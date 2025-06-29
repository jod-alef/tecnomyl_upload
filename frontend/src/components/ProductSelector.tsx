import React from 'react';

interface ProductSelectorProps {
  products: string[];
  selectedProduct: string;
  onProductChange: (product: string) => void;
  loading?: boolean;
}

const ProductSelector: React.FC<ProductSelectorProps> = ({
  products,
  selectedProduct,
  onProductChange,
  loading = false,
}) => {
  return (
    <div className="w-full">
      <label className="block text-sm font-medium text-gray-700 mb-2">
        Selecione o Produto
      </label>
      
      <div className="relative">
        <select
          value={selectedProduct}
          onChange={(e) => onProductChange(e.target.value)}
          disabled={loading}
          className={`
            w-full px-4 py-3 border border-gray-300 rounded-lg shadow-sm
            focus:ring-2 focus:ring-tecnomyl-primary focus:border-tecnomyl-primary
            text-gray-900 text-base
            ${loading ? 'bg-gray-100 cursor-not-allowed' : 'bg-white'}
            transition-colors duration-200
          `}
        >
          <option value="">Escolha um produto...</option>
          {products.map((product) => (
            <option key={product} value={product}>
              {product.replace(/_/g, ' ')}
            </option>
          ))}
        </select>
        
        {loading && (
          <div className="absolute right-3 top-1/2 transform -translate-y-1/2">
            <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-tecnomyl-primary"></div>
          </div>
        )}
        
        <div className="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none">
          {!loading && (
            <svg className="h-5 w-5 text-gray-400" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clipRule="evenodd" />
            </svg>
          )}
        </div>
      </div>
      
      {selectedProduct && (
        <p className="mt-2 text-sm text-gray-600">
          Produto selecionado: <span className="font-medium text-tecnomyl-dark">{selectedProduct.replace(/_/g, ' ')}</span>
        </p>
      )}
    </div>
  );
};

export default ProductSelector; 