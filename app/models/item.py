from app import db

class Item(db.Model):
    __tablename__ = 'item'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(300), nullable=False)
    preco = db.Column(db.Numeric(10, 2), nullable=False)
    tipo = db.Column(db.Enum('PRODUTO', 'SERVICO', name='item_tipo'), nullable=False)
    estoque = db.Column(db.Integer, nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=False)
    fornecedor_id = db.Column(db.Integer, db.ForeignKey('fornecedor.id'), nullable=False)

    categoria = db.relationship('Categoria', back_populates='itens')
    fornecedor = db.relationship('Fornecedor', back_populates='itens')
    itens_pedido = db.relationship('ItemPedido', back_populates='item')
