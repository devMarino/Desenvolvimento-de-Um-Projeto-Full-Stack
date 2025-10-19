from app import db
from sqlalchemy import Enum

class Item(db.Model):
    __tablename__ = 'item'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(300))
    preco = db.Column(db.Numeric(10, 2))
    tipo = db.Column(Enum('produto', 'servico', name='tipo_enum'))
    estoque = db.Column(db.Integer)

    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=False)
    fornecedor_id = db.Column(db.Integer, db.ForeignKey('fornecedor.id'), nullable=False)

    itens_pedido = db.relationship('ItemPedido', backref='item', lazy=True)
