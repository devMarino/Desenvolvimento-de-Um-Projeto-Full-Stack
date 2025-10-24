// Espera o HTML carregar
document.addEventListener('DOMContentLoaded', () => {

    // 1. PEGAR OS ELEMENTOS DA PÁGINA
    const tituloElemento = document.getElementById('categoria-titulo');
    const productGrid = document.getElementById('product-grid');
    const loadingMessage = document.getElementById('loading-message');

    // 2. FUNÇÃO PARA PEGAR O PARÂMETRO DA URL
    function getQueryParam(param) {
        const urlParams = new URLSearchParams(window.location.search);
        return urlParams.get(param); // Ex: 'cimento-e-argamassa'
    }

    // 3. FUNÇÃO PARA FORMATAR O NOME (de 'cimento-e-argamassa' para 'Cimento e Argamassa')
    function formatarNomeCategoria(slug) {
        if (!slug) return "Todos os Produtos"; // Fallback
        
        let palavras = slug.split('-'); // ['cimento', 'e', 'argamassa']
        
        let nomeFormatado = palavras.map(palavra => {
            // Capitaliza a primeira letra de cada palavra (exceto 'e', 'de', 'da')
            if (palavra !== 'e' && palavra !== 'de' && palavra !== 'da') {
                return palavra.charAt(0).toUpperCase() + palavra.slice(1);
            } else {
                return palavra;
            }
        }).join(' '); // 'Cimento e Argamassa'
        
        return nomeFormatado;
    }

    // 4. FUNÇÃO (PLACEHOLDER) PARA BUSCAR PRODUTOS NA API
    // (Por enquanto, ela só vai mostrar uma mensagem)
    async function fetchProductsByCategory(categoriaSlug) {
        console.log(`Iniciando busca por produtos da categoria: ${categoriaSlug}`);
        
        // --- SIMULAÇÃO DE DEMORA (loading) ---
        // (No futuro, aqui será a chamada fetch('/api/produtos?categoria=...')
        setTimeout(() => {
            
            // Limpa a mensagem "Carregando..."
            productGrid.innerHTML = ''; 
            
            // --- SIMULAÇÃO DE RESULTADO ---
            // (Substituir isso pela lógica real de criar os cards)
            
            // Exemplo de como seria se tivéssemos produtos:
            /*
            const produtos = [ {nome: 'Cimento Votoran', ...}, {nome: 'Argamassa ACIII', ...} ];
            
            if(produtos.length === 0) {
                 productGrid.innerHTML = '<p class="loading-products">Nenhum produto encontrado nesta categoria.</p>';
                 return;
            }
            
            produtos.forEach(produto => {
                const card = document.createElement('div');
                card.className = 'product-card';
                card.innerHTML = `
                    <div class="product-image-placeholder"></div>
                    <h3>${produto.nome}</h3>
                    <span class="product-price">R$ ${produto.preco}</span>
                    <button class="btn-add-cart">Adicionar ao Carrinho</button>
                `;
                productGrid.appendChild(card);
            });
            */
            
            // Mensagem temporária enquanto a API não existe:
            productGrid.innerHTML = `<p class="loading-products">API de produtos ainda não conectada. (Categoria: ${categoriaSlug})</p>`;


        }, 1500); // Simula 1.5s de loading
    }


    // --- PONTO DE PARTIDA ---
    
    // 1. Pega a categoria da URL
    const categoriaSlug = getQueryParam('categoria');
    
    // 2. Formata o nome e atualiza o H1 da página
    const nomeFormatado = formatarNomeCategoria(categoriaSlug);
    tituloElemento.textContent = nomeFormatado;

    // 3. Chama a função para buscar os produtos
    if (categoriaSlug) {
        fetchProductsByCategory(categoriaSlug);
    } else {
        // Se não veio categoria, poderia buscar todos
        console.log("Nenhuma categoria especificada, buscando todos os produtos.");
        // fetchProductsByCategory('todos'); // Ou algo assim
        loadingMessage.textContent = "Nenhuma categoria foi selecionada.";
    }

});