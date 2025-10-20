from app import db

class Pedido(db.Model):
    __tablename__ = 'pedido'

    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    preco_total = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.Enum('ABERTO', 'FECHADO', 'CANCELADO', name='pedido_status'), nullable=False)

    cliente = db.relationship('Cliente', back_populates='pedidos')
    itens_pedido = db.relationship('ItemPedido', back_populates='pedido')
