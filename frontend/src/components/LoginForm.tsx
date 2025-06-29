import React, { useState } from 'react';

interface LoginFormProps {
  onLogin: (username: string, password: string) => Promise<void>;
  error?: string;
  loading?: boolean;
}

const LoginForm: React.FC<LoginFormProps> = ({ onLogin, error, loading }) => {
  const [credentials, setCredentials] = useState({
    username: '',
    password: ''
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await onLogin(credentials.username, credentials.password);
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setCredentials(prev => ({
      ...prev,
      [e.target.name]: e.target.value
    }));
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-sm w-full space-y-8">
        {/* Header com Logo */}
        <div className="text-center">
          <div className="flex justify-center mb-6">
            <img 
              src="/logo_horizontal_tecnomyl.png" 
              alt="Tecnomyl Logo" 
              className="h-10 w-auto object-contain"
            />
          </div>
          <h2 className="text-2xl font-bold text-gray-900 mb-2">
            Sistema de Upload
          </h2>
          <p className="text-sm text-gray-600">
            Faça login para acessar o sistema
          </p>
        </div>

        {/* Caixa de Login */}
        <div className="bg-white rounded-xl shadow-lg border border-gray-100 p-8">
          <form className="space-y-5" onSubmit={handleSubmit}>
            <div>
              <label htmlFor="username" className="block text-sm font-medium text-gray-700 mb-2">
                Usuário
              </label>
              <input
                id="username"
                name="username"
                type="text"
                autoComplete="username"
                required
                value={credentials.username}
                onChange={handleChange}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-tecnomyl-green focus:border-tecnomyl-green text-sm transition-colors"
                placeholder="Digite seu usuário"
              />
            </div>

            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-2">
                Senha
              </label>
              <input
                id="password"
                name="password"
                type="password"
                autoComplete="current-password"
                required
                value={credentials.password}
                onChange={handleChange}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-tecnomyl-green focus:border-tecnomyl-green text-sm transition-colors"
                placeholder="Digite sua senha"
              />
            </div>

            {error && (
              <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
                <div className="flex items-center">
                  <svg className="w-5 h-5 mr-2 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <span className="text-sm">{error}</span>
                </div>
              </div>
            )}

            <button
              type="submit"
              disabled={loading}
              className="w-full flex justify-center items-center py-3 px-4 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-tecnomyl-green hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-tecnomyl-green disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
              {loading ? (
                <>
                  <svg className="animate-spin -ml-1 mr-3 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Entrando...
                </>
              ) : (
                'Entrar'
              )}
            </button>
          </form>

          <div className="mt-6 pt-4 border-t border-gray-100">
            <p className="text-center text-xs text-gray-500">
              Sistema Tecnomyl - Upload de Arquivos
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoginForm; 