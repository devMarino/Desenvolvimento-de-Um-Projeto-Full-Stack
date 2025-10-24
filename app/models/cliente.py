from app import db
from sqlalchemy.inspection import inspect
# Importar os outros modelos não é necessário se usarmos strings

class Cliente(db.Model):
    __tablename__ = 'cliente'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(16), nullable=True)  # Ajustado para nulo (para permitir CNPJ)
    cnpj = db.Column(db.String(18), nullable=True) # Ajustado para nulo (para permitir CPF)
    email = db.Column(db.String(100), nullable=False)
    endereco = db.Column(db.String(200), nullable=False)

    
    pedidos = db.relationship('Pedido', back_populates='cliente', cascade="all, delete-orphan")


    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}