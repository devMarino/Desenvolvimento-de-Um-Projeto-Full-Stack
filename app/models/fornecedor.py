from app import db
from sqlalchemy.inspection import inspect

class Fornecedor(db.Model):
    __tablename__ = 'fornecedor'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(18), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    endereco = db.Column(db.String(120), nullable=False)

    itens = db.relationship('Item', back_populates='fornecedor')

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}