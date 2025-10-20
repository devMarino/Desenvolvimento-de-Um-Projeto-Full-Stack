from app import db

class ItemPedido(db.Model):
    __tablename__ = 'item_pedido'

    id = db.Column(db.Integer, primary_key=True)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedido.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)

    pedido = db.relationship('Pedido', back_populates='itens_pedido')
    item = db.relationship('Item', back_populates='itens_pedido')
    atendimentos = db.relationship('Atendimento', back_populates='item_pedido')
