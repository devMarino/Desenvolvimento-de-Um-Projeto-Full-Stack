# Dentro de Desenvolvimento-de-Um-Projeto-Full-Stack-main/app/routes/frontend_routes.py

from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from app import db # Importa a instância db do __init__.py principal
from app.models.item import Item # Importa o modelo Item do seu projeto

frontend_bp = Blueprint('main', __name__)

@frontend_bp.route('/')
def index():
    # Redireciona a rota raiz (/) para a página da loja (/loja)
    return redirect(url_for('main.loja_index'))

# Rota para a página inicial da loja
@frontend_bp.route('/loja')
def loja_index():
    try:
        # Busca 8 itens do tipo PRODUTO (verifique se 'PRODUTO' é o valor correto no seu modelo Item)
        # Adapte 'imagem_url' se o nome do campo for diferente no seu modelo Item
        itens_destaque = Item.query.filter_by(tipo='produto').limit(8).all()
    except Exception as e:
        print(f"Erro ao buscar itens: {e}")
        itens_destaque = []
    return render_template('index.html', itens_destaque=itens_destaque)

# Rota para a página de login
@frontend_bp.route('/login')
def login():
    return render_template('login.html')

# Rota para o carrinho
@frontend_bp.route('/carrinho')
def carrinho():
    return render_template('carrinho.html')

# Rota para a página de produtos (com filtro opcional)
@frontend_bp.route('/produtos')
def produtos():
    categoria_slug = request.args.get('categoria')
    # Lógica de filtro viria aqui
    return render_template('produtos.html', categoria_selecionada=categoria_slug)

# Rota de API para detalhes do item (usada pelo carrinho.js)
@frontend_bp.route('/api/item/<int:id>')
def get_item_details_api(id):
    item_obj = Item.query.get_or_404(id)
    # Tenta usar o método to_dict se existir, senão cria o dicionário
    if hasattr(item_obj, 'to_dict'):
         item_dict = item_obj.to_dict()
         # Garante que o preço seja float para o JSON
         if 'preco' in item_dict and not isinstance(item_dict.get('preco'), float):
             try:
                 item_dict['preco'] = float(item_dict['preco'])
             except (TypeError, ValueError):
                 item_dict['preco'] = 0.0
         return jsonify(item_dict)
    else:
         # Cria dicionário manualmente, garantindo a conversão do preço
         # Verifique se o seu modelo Item tem 'imagem_url'
         return jsonify({
             'id': item_obj.id,
             'nome': item_obj.nome,
             'descricao': item_obj.descricao,
             'preco': float(item_obj.preco) if item_obj.preco is not None else 0.0,
             'tipo': item_obj.tipo,
             'estoque': item_obj.estoque,
             'imagem_url': getattr(item_obj, 'imagem_url', None), # Adiciona imagem_url se existir no modelo
             'categoria_id': item_obj.categoria_id,
             'fornecedor_id': item_obj.fornecedor_id
         })
