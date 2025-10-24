// Este script só roda na página do carrinho.html

document.addEventListener('DOMContentLoaded', () => {
    const cartList = document.getElementById('cart-list');
    const loadingMessage = document.getElementById('loading-message');
    
    // Funções para pegar/salvar o carrinho (copiadas de main.js para garantir)
    function getCart() {
        return JSON.parse(localStorage.getItem('carrinho')) || {};
    }
    function saveCart(cart) {
        localStorage.setItem('carrinho', JSON.stringify(cart));
    }

    // Função para buscar os detalhes de um item na nossa nova API
    async function fetchItemDetails(id) {
        try {
            const response = await fetch(`/api/item/${id}`);
            if (!response.ok) {
                throw new Error('Produto não encontrado');
            }
            return await response.json();
        } catch (error) {
            console.error('Erro ao buscar item:', error);
            return null; // Retorna nulo se der erro
        }
    }

    // Função principal para mostrar os itens do carrinho
    async function displayCartItems() {
        const cart = getCart();
        const items = Object.values(cart); // Pega os itens do objeto

        if (items.length === 0) {
            loadingMessage.textContent = 'Seu carrinho está vazio.';
            return;
        }
        
        // Limpa a mensagem "Carregando..."
        cartList.innerHTML = '';
        
        let subtotal = 0;

        // Para cada item no localStorage, busca os detalhes e cria o HTML
        for (const cartItem of items) {
            const itemDetails = await fetchItemDetails(cartItem.id);
            
            if (itemDetails) {
                const totalItemPrice = itemDetails.preco * cartItem.quantidade;
                subtotal += totalItemPrice;

                const li = document.createElement('li');
                li.className = 'cart-item-line';
                li.innerHTML = `
                    <div class="item-details">
                        <span class="item-name">${itemDetails.nome}</span>
                        <span class="item-price-unit">R$ ${itemDetails.preco.toFixed(2)} / un.</span>
                    </div>
                    <div class="item-controls">
                        <input type="number" class="quantity-input" value="${cartItem.quantidade}" data-item-id="${cartItem.id}" min="1">
                        <span class="item-price-total">R$ ${totalItemPrice.toFixed(2)}</span>
                        <button class="btn-remove" data-item-id="${cartItem.id}">Remover</button>
                    </div>
                `;
                cartList.appendChild(li);
            }
        }
        
        // Atualiza os totais no Resumo
        document.getElementById('subtotal').textContent = `R$ ${subtotal.toFixed(2)}`;
        document.getElementById('total-final').textContent = `R$ ${subtotal.toFixed(2)}`;
        
        // Adiciona funcionalidade aos botões de remover e mudar quantidade
        addCartEventListeners();
    }
    
    // Função para atualizar o carrinho se o usuário mudar a quantidade ou remover
    function addCartEventListeners() {
        // Botões de Remover
        document.querySelectorAll('.btn-remove').forEach(button => {
            button.addEventListener('click', (e) => {
                const itemId = e.target.getAttribute('data-item-id');
                removeItem(itemId);
            });
        });

        // Campo de Quantidade
        document.querySelectorAll('.quantity-input').forEach(input => {
            input.addEventListener('change', (e) => {
                const itemId = e.target.getAttribute('data-item-id');
                const novaQuantidade = parseInt(e.target.value, 10);
                updateQuantity(itemId, novaQuantidade);
            });
        });
    }

    function removeItem(itemId) {
        const cart = getCart();
        delete cart[itemId];
        saveCart(cart);
        displayCartItems(); // Recarrega a lista
    }

    function updateQuantity(itemId, quantidade) {
        if (quantidade <= 0) {
            removeItem(itemId);
            return;
        }
        const cart = getCart();
        if (cart[itemId]) {
            cart[itemId].quantidade = quantidade;
            saveCart(cart);
            displayCartItems(); // Recarrega a lista
        }
    }

    // Ponto de partida: Chama a função para mostrar os itens
    displayCartItems();
});