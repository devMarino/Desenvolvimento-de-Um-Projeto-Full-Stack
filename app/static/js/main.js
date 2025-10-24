// --- Lógica do Carrinho (Adicionar) ---

// Função para pegar o carrinho atual do localStorage
function getCart() {
    // Se não houver carrinho, retorna um objeto vazio
    return JSON.parse(localStorage.getItem('carrinho')) || {};
}

// Função para salvar o carrinho no localStorage
function saveCart(cart) {
    localStorage.setItem('carrinho', JSON.stringify(cart));
}

// Função principal para adicionar um item
function addItemToCart(itemId) {
    const cart = getCart();
    
    // Se o item já está no carrinho, só aumenta a quantidade (ex: 1 -> 2)
    if (cart[itemId]) {
        cart[itemId].quantidade += 1;
    } else {
        // Se for um item novo, adiciona com quantidade 1
        cart[itemId] = { id: itemId, quantidade: 1 };
    }
    
    saveCart(cart);
    console.log('Carrinho atualizado:', getCart());
    alert('Produto adicionado ao carrinho!');
}

// Adiciona o "ouvidor" de clique a TODOS os botões .btn-add-cart da página
document.addEventListener('DOMContentLoaded', () => {
    // ... (o código do menu hamburger já existe aqui) ...

    const addButtons = document.querySelectorAll('.btn-add-cart');
    addButtons.forEach(button => {
        button.addEventListener('click', () => {
            const itemId = button.getAttribute('data-item-id');
            addItemToCart(itemId);
        });
    });
});