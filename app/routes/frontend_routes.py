# Dentro de Desenvolvimento-de-Um-Projeto-Full-Stack-main/app/routes/frontend_routes.py

from flask import (
    Blueprint, render_template, request, jsonify, redirect, url_for, 
    session, flash
)
from app import db # Importa a instância db
# Importa TODOS os modelos que o dashboard vai precisar
from app.models.item import Item
from app.models.cliente import Cliente
from app.models.categoria import Categoria
from app.models.fornecedor import Fornecedor
from app.models.atendimento import Atendimento
from decimal import Decimal
import functools # Necessário para o decorator de login

frontend_bp = Blueprint('main', __name__)

# --- DECORATOR DE LOGIN ---
# Esta função verifica se o usuário está logado antes de acessar uma rota
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if 'logged_in' not in session:
            flash('Você precisa fazer login para acessar esta página.', 'error')
            return redirect(url_for('main.login'))
        return view(**kwargs)
    return wrapped_view

# --- ROTAS DA LOJA (PÚBLICAS) ---

@frontend_bp.route('/')
def index():
    # Redireciona a rota raiz (/) para a página da loja (/loja)
    return redirect(url_for('main.loja_index'))

# Rota para a página inicial da loja
@frontend_bp.route('/loja')
def loja_index():
    try:
        # Busca 11 itens do tipo PRODUTO (Corrigido para MAIÚSCULA)
        itens_destaque = Item.query.filter_by(tipo='PRODUTO').limit(11).all()
    except Exception as e:
        print(f"Erro ao buscar itens: {e}")
        itens_destaque = []
    return render_template('index.html', itens_destaque=itens_destaque)

# Rota para o carrinho
@frontend_bp.route('/carrinho')
def carrinho():
    return render_template('carrinho.html')

# Rota para a página de produtos (com filtro opcional)
@frontend_bp.route('/produtos')
def produtos():
    categoria_slug = request.args.get('categoria')
    return render_template('produtos.html', categoria_selecionada=categoria_slug)

# Rota de API para detalhes do item (usada pelo carrinho.js)
@frontend_bp.route('/api/item/<int:id>')
def get_item_details_api(id):
    item_obj = Item.query.get_or_404(id)
    if hasattr(item_obj, 'to_dict'):
         item_dict = item_obj.to_dict()
         if 'preco' in item_dict and not isinstance(item_dict.get('preco'), float):
             try:
                 item_dict['preco'] = float(item_dict['preco'])
             except (TypeError, ValueError):
                 item_dict['preco'] = 0.0
         return jsonify(item_dict)
    else:
         return jsonify({
             'id': item_obj.id, 'nome': item_obj.nome, 'descricao': item_obj.descricao,
             'preco': float(item_obj.preco) if item_obj.preco is not None else 0.0,
             'tipo': item_obj.tipo, 'estoque': item_obj.estoque,
             'imagem_url': getattr(item_obj, 'imagem_url', None),
             'categoria_id': item_obj.categoria_id, 'fornecedor_id': item_obj.fornecedor_id
         })

# --- ROTAS DE LOGIN E DASHBOARD (PROTEGIDAS) ---

# Rota para a página de login (GET e POST)
@frontend_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # --- LÓGICA DE LOGIN SIMPLES (sem banco de dados de usuário) ---
        # Verifique se o login e senha estão corretos (hardcoded)
        if email == 'admin@admin.com' and password == 'admin':
            session['logged_in'] = True # "Loga" o usuário na sessão
            session['user_email'] = email
            flash('Login bem-sucedido!', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            flash('E-mail ou senha inválidos.', 'error')
            
    # Se for GET, apenas mostra a página de login
    return render_template('login.html')

@frontend_bp.route('/logout')
@login_required # Precisa estar logado para deslogar
def logout():
    session.clear() # Limpa a sessão
    flash('Você foi desconectado.', 'success')
    return redirect(url_for('main.loja_index'))

# Rota principal do Dashboard (PROTEGIDA)
@frontend_bp.route('/dashboard')
@login_required # <- ISSO PROTEGE A ROTA
def dashboard():
    try:
        # Busca todos os dados necessários para o dashboard.html
        clientes = Cliente.query.all()
        itens = Item.query.all()
        atendimentos = Atendimento.query.all()
        categorias = Categoria.query.all()
        fornecedores = Fornecedor.query.all()
        
        # Para os cards de estatística
        total_clientes = len(clientes)
        total_itens = len(itens)
        total_atendimentos = len(atendimentos)

        return render_template('dashboard.html', 
                               clientes=clientes, 
                               itens=itens,
                               atendimentos=atendimentos,
                               categorias=categorias,
                               fornecedores=fornecedores,
                               total_clientes=total_clientes,
                               total_itens=total_itens,
                               total_atendimentos=total_atendimentos)
    except Exception as e:
        flash(f'Erro ao carregar o dashboard: {e}', 'error')
        return redirect(url_for('main.loja_index'))

# --- ROTAS CRUD (Cliente) ---

@frontend_bp.route('/cliente/add', methods=['POST'])
@login_required
def add_cliente():
    try:
        novo = Cliente(
            nome=request.form.get('nome_cliente'),
            email=request.form.get('email_cliente'),
            telefone=request.form.get('telefone_cliente'),
            cpf=request.form.get('cpf_cliente'),
            endereco=request.form.get('endereco_cliente')
        )
        db.session.add(novo)
        db.session.commit()
        flash('Cliente cadastrado com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao cadastrar cliente: {e}', 'error')
    return redirect(url_for('main.dashboard'))

@frontend_bp.route('/cliente/edit/<int:id>')
@login_required
def edit_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    return render_template('edit_cliente.html', cliente=cliente)

@frontend_bp.route('/cliente/update/<int:id>', methods=['POST'])
@login_required
def update_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    try:
        cliente.nome = request.form.get('nome_cliente')
        cliente.email = request.form.get('email_cliente')
        cliente.telefone = request.form.get('telefone_cliente')
        cliente.cpf = request.form.get('cpf_cliente')
        cliente.endereco = request.form.get('endereco_cliente')
        db.session.commit()
        flash('Cliente atualizado com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao atualizar cliente: {e}', 'error')
    return redirect(url_for('main.dashboard'))

@frontend_bp.route('/cliente/delete/<int:id>')
@login_required
def delete_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    try:
        db.session.delete(cliente)
        db.session.commit()
        flash('Cliente excluído com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao excluir cliente: {e}', 'error')
    return redirect(url_for('main.dashboard'))


# --- ROTAS CRUD (Item / Produto/Serviço) ---

@frontend_bp.route('/item/add', methods=['POST'])
@login_required
def add_item():
    try:
        novo = Item(
            nome=request.form.get('nome_item'),
            categoria_id=int(request.form.get('categoria_id')),
            fornecedor_id=int(request.form.get('fornecedor_id')),
            preco=Decimal(request.form.get('valor_item')),
            tipo=request.form.get('tipo_item'), # Já vem 'PRODUTO' ou 'SERVICO'
            estoque=int(request.form.get('estoque_item')),
            descricao=request.form.get('descricao_item')
        )
        db.session.add(novo)
        db.session.commit()
        flash('Item cadastrado com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao cadastrar item: {e}', 'error')
    return redirect(url_for('main.dashboard'))

@frontend_bp.route('/item/edit/<int:id>')
@login_required
def edit_item(id):
    item = Item.query.get_or_404(id)
    categorias = Categoria.query.all()
    fornecedores = Fornecedor.query.all()
    return render_template('edit_item.html', 
                           item=item, 
                           categorias=categorias, 
                           fornecedores=fornecedores)

@frontend_bp.route('/item/update/<int:id>', methods=['POST'])
@login_required
def update_item(id):
    item = Item.query.get_or_404(id)
    try:
        item.nome = request.form.get('nome_item')
        item.categoria_id = int(request.form.get('categoria_id'))
        item.fornecedor_id = int(request.form.get('fornecedor_id'))
        item.preco = Decimal(request.form.get('valor_item'))
        item.tipo = request.form.get('tipo_item')
        item.estoque = int(request.form.get('estoque_item'))
        item.descricao = request.form.get('descricao_item')
        db.session.commit()
        flash('Item atualizado com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao atualizar item: {e}', 'error')
    return redirect(url_for('main.dashboard'))

@frontend_bp.route('/item/delete/<int:id>')
@login_required
def delete_item(id):
    item = Item.query.get_or_404(id)
    try:
        db.session.delete(item)
        db.session.commit()
        flash('Item excluído com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao excluir item: {e}', 'error')
    return redirect(url_for('main.dashboard'))


# --- ROTAS CRUD (Atendimento) ---

@frontend_bp.route('/atendimento/add', methods=['POST'])
@login_required
def add_atendimento():
    # ATENÇÃO: O modelo de Atendimento está estranho (liga-se a item_pedido_id)
    # Vou simplificar e ligar a cliente_id e item_id, como o formulário sugere
    try:
        novo = Atendimento(
            cliente_id=int(request.form.get('cliente_id')),
            item_id=int(request.form.get('item_id')),
            observacoes=request.form.get('observacoes')
            # data_atendimento é default=today()
        )
        db.session.add(novo)
        db.session.commit()
        flash('Atendimento registrado com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao registrar atendimento: {e}', 'error')
    return redirect(url_for('main.dashboard'))

@frontend_bp.route('/atendimento/edit/<int:id>')
@login_required
def edit_atendimento(id):
    atendimento = Atendimento.query.get_or_404(id)
    clientes = Cliente.query.all()
    itens = Item.query.all()
    return render_template('edit_atendimento.html', 
                           atendimento=atendimento, 
                           clientes=clientes, 
                           itens=itens)

@frontend_bp.route('/atendimento/update/<int:id>', methods=['POST'])
@login_required
def update_atendimento(id):
    atendimento = Atendimento.query.get_or_404(id)
    try:
        atendimento.cliente_id = int(request.form.get('cliente_id'))
        atendimento.item_id = int(request.form.get('item_id'))
        atendimento.observacoes = request.form.get('observacoes')
        db.session.commit()
        flash('Atendimento atualizado com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao atualizar atendimento: {e}', 'error')
    return redirect(url_for('main.dashboard'))

@frontend_bp.route('/atendimento/delete/<int:id>')
@login_required
def delete_atendimento(id):
    atendimento = Atendimento.query.get_or_404(id)
    try:
        db.session.delete(atendimento)
        db.session.commit()
        flash('Atendimento excluído com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao excluir atendimento: {e}', 'error')
    return redirect(url_for('main.dashboard'))