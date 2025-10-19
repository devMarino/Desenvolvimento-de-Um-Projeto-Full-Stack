from app import db
from sqlalchemy import Enum

class Pedido(db.Model):
    __tablename__ = 'pedido'

    id = db.Column(db.Integer, primary_key=True)
    preco_total = db.Column(db.Numeric(10, 2))
    status = db.Column(Enum('pendente', 'confirmado', 'cancelado', name='status_enum'))
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)

    itens_pedido = db.relationship('ItemPedido', backref='pedido', lazy=True)
