from app import db
from sqlalchemy.inspection import inspect

class Cliente(db.Model):
    __tablename__ = 'cliente'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(16), nullable=False)
    cnpj = db.Column(db.String(16), nullable=True)
    email = db.Column(db.String(100), nullable=False)
    endereco = db.Column(db.String(200), nullable=False)

    pedidos = db.relationship('Pedido', back_populates='cliente')

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
