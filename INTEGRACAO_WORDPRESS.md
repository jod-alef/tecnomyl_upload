# 🔗 Integração WordPress - Upload Tecnomyl

Este documento explica como integrar o sistema Upload Tecnomyl com seu site WordPress.

## 📡 Endpoint para WordPress

O sistema fornece um endpoint específico para integração:

```
GET /api/wordpress/product-files/{nome_produto}
```

### Exemplo de resposta:
```json
{
  "produto": "ACEFATO_750",
  "files": {
    "bula": "http://localhost:9000/tecnomyl/produtos/ACEFATO_750/ACEFATO_750_bula.pdf",
    "fispq": "http://localhost:9000/tecnomyl/produtos/ACEFATO_750/ACEFATO_750_FISPQ.pdf",
    "ficha_de_emergencia": "http://localhost:9000/tecnomyl/produtos/ACEFATO_750/ACEFATO_750_Ficha_de_Emergencia.pdf"
  },
  "total_files": 3
}
```

## 🔌 Plugin WordPress (Opção 1)

### Instalação

1. Crie um plugin personalizado no WordPress:

```php
<?php
/**
 * Plugin Name: Tecnomyl Files
 * Description: Integração com sistema Upload Tecnomyl
 * Version: 1.0
 */

// Shortcode para exibir arquivos do produto
function tecnomyl_files_shortcode($atts) {
    $atts = shortcode_atts(array(
        'produto' => '',
        'api_url' => 'http://localhost:8000'
    ), $atts);

    if (empty($atts['produto'])) {
        return '<p>Error: Nome do produto não informado</p>';
    }

    $api_endpoint = $atts['api_url'] . '/api/wordpress/product-files/' . $atts['produto'];
    
    $response = wp_remote_get($api_endpoint);
    
    if (is_wp_error($response)) {
        return '<p>Error: Não foi possível conectar com o sistema</p>';
    }
    
    $body = wp_remote_retrieve_body($response);
    $data = json_decode($body, true);
    
    if (!$data || !isset($data['files'])) {
        return '<p>Nenhum arquivo encontrado para este produto</p>';
    }
    
    $html = '<div class="tecnomyl-files">';
    $html .= '<h3>Arquivos do Produto: ' . $data['produto'] . '</h3>';
    $html .= '<ul class="product-files-list">';
    
    foreach ($data['files'] as $tipo => $url) {
        $label = ucfirst(str_replace('_', ' ', $tipo));
        $html .= '<li><a href="' . esc_url($url) . '" target="_blank">' . $label . '</a></li>';
    }
    
    $html .= '</ul>';
    $html .= '</div>';
    
    return $html;
}

add_shortcode('tecnomyl_files', 'tecnomyl_files_shortcode');

// CSS para estilização
function tecnomyl_files_styles() {
    echo '<style>
        .tecnomyl-files {
            border: 1px solid #ddd;
            border-radius: 5px;
            padding: 15px;
            margin: 15px 0;
        }
        .product-files-list {
            list-style: none;
            padding: 0;
        }
        .product-files-list li {
            margin: 10px 0;
            padding: 8px;
            background: #f9f9f9;
            border-radius: 3px;
        }
        .product-files-list a {
            text-decoration: none;
            color: #0073aa;
            font-weight: bold;
        }
        .product-files-list a:hover {
            text-decoration: underline;
        }
    </style>';
}

add_action('wp_head', 'tecnomyl_files_styles');
?>
```

### Uso do Shortcode

Adicione em suas páginas/posts:

```
[tecnomyl_files produto="ACEFATO_750"]
```

## 🔗 Integração via AJAX (Opção 2)

### JavaScript para WordPress

```javascript
// Adicione ao seu tema WordPress
function loadTecnomylFiles(produto, containerElement) {
    const apiUrl = 'http://localhost:8000/api/wordpress/product-files/' + produto;
    
    fetch(apiUrl)
        .then(response => response.json())
        .then(data => {
            if (data.files) {
                let html = '<div class="tecnomyl-files-container">';
                html += '<h4>Documentos Disponíveis</h4>';
                html += '<div class="files-grid">';
                
                Object.entries(data.files).forEach(([tipo, url]) => {
                    const label = tipo.replace('_', ' ').toUpperCase();
                    html += `
                        <div class="file-item">
                            <a href="${url}" target="_blank" class="file-link">
                                <i class="fa fa-file-pdf"></i>
                                ${label}
                            </a>
                        </div>
                    `;
                });
                
                html += '</div></div>';
                containerElement.innerHTML = html;
            } else {
                containerElement.innerHTML = '<p>Nenhum arquivo disponível</p>';
            }
        })
        .catch(error => {
            console.error('Erro ao carregar arquivos:', error);
            containerElement.innerHTML = '<p>Erro ao carregar arquivos</p>';
        });
}

// Uso
document.addEventListener('DOMContentLoaded', function() {
    const container = document.getElementById('tecnomyl-files');
    const produto = container.dataset.produto;
    
    if (produto) {
        loadTecnomylFiles(produto, container);
    }
});
```

### HTML no WordPress

```html
<div id="tecnomyl-files" data-produto="ACEFATO_750"></div>
```

## 📋 Lista de Produtos Disponíveis

Para obter a lista completa de produtos:

```
GET /api/products
```

## 🔒 Configurações de Segurança

1. **CORS**: Configure o backend para permitir seu domínio WordPress
2. **Rate Limiting**: Implemente limitação de requisições se necessário
3. **Cache**: Use cache no WordPress para melhorar performance

## 🎨 Customização CSS

```css
.tecnomyl-files-container {
    background: #f8f9fa;
    border: 1px solid #dee2e6;
    border-radius: 8px;
    padding: 20px;
    margin: 20px 0;
}

.files-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 15px;
    margin-top: 15px;
}

.file-item {
    background: white;
    border: 1px solid #e9ecef;
    border-radius: 6px;
    transition: all 0.3s ease;
}

.file-item:hover {
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    transform: translateY(-2px);
}

.file-link {
    display: block;
    padding: 15px;
    text-decoration: none;
    color: #495057;
    text-align: center;
}

.file-link i {
    font-size: 24px;
    color: #dc3545;
    margin-bottom: 8px;
    display: block;
}
```

## 🚀 Deploy em Produção

1. Altere as URLs da API para seu servidor de produção
2. Configure HTTPS se necessário
3. Ajuste as configurações de CORS
4. Teste todas as integrações

## 🆘 Suporte

Se precisar de ajuda com a integração, verifique:

1. **Logs do backend**: `/backend/logs/`
2. **Console do navegador**: Para erros JavaScript
3. **Health check**: `GET /health` para verificar status da API 