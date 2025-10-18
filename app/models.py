from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
from sqlalchemy.types import Enum


# MODELOS PRINCIPAIS
class categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)

    # Relacionamento 1:N com Item
    item_list = db.relationship('item', backref='categoria_obj', lazy=True)


class fornecedor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(18), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    endereco = db.Column(db.String(120), nullable=False)

    # Relacionamento 1:N com Item
    item_list = db.relationship('item', backref='fornecedor_obj', lazy=True)


class cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(16), nullable=True)
    cnpj = db.Column(db.String(16), nullable=True)
    email = db.Column(db.String(100), nullable=False)
    endereco = db.Column(db.String(200), nullable=False)
    
    # Relacionamento 1:N com Atendimento
    atendimentos = db.relationship('atendimento', backref='cliente_obj', lazy=True)


# MODELO PRODUTO/SERVIÇO

class item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(300), nullable=True)
    preco = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    
    # Campo para diferenciar Produto ou Serviço
    tipo = db.Column(db.Enum('produto', 'servico', name='tipo_item'), nullable=False)
    
    estoque = db.Column(db.Integer, nullable=True)
    
    # Chaves estrangeiras
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=False)
    fornecedor_id = db.Column(db.Integer, db.ForeignKey('fornecedor.id'), nullable=False)

  
    # Relacionamento N:M com item_pedido
    pedidos_item = db.relationship('item_pedido', backref='item_obj', lazy=True)

# --- MODELOS TRANSACIONAIS ---
class atendimento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    # Chave Estrangeira: 1:N com Cliente
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    
    data_atendimento = db.Column(db.DateTime, nullable=False)
    
    # Relacionamento 1:1 com Pedido (o backref já cuida da relação)


class pedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    # Chave Estrangeira: 1:1 com Atendimento
    atendimento_id = db.Column(db.Integer, db.ForeignKey('atendimento.id'), nullable=False, unique=True)
    
    preco_total = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    status = db.Column(db.Enum('pendente', 'confirmado', 'cancelado', name='status_pedido'), 
                       default='pendente', nullable=False)
    
    # Relacionamento 1:1 de volta para Atendimento (permite acessar o objeto atendimento)
    atendimento_rel = db.relationship('atendimento', backref=db.backref('pedido_obj', uselist=False), lazy=True)
    
    # Relacionamento 1:N com item_pedido
    itens_pedido = db.relationship('item_pedido', backref='pedido_obj', lazy=True)


class item_pedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    # Chaves Estrangeiras
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedido.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    
    quantidade = db.Column(db.Integer, nullable=False)
