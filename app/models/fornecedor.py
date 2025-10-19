from app import db

class Fornecedor(db.Model):
    __tablename__ = 'fornecedor'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(18))
    email = db.Column(db.String(100))
    endereco = db.Column(db.String(120))

    itens = db.relationship('Item', backref='fornecedor', lazy=True)
