from app import db

class Fornecedor(db.Model):
    __tablename__ = 'fornecedor'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(18), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    endereco = db.Column(db.String(120), nullable=False)

    itens = db.relationship('Item', back_populates='fornecedor')
