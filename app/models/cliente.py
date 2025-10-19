from app import db

class Cliente(db.Model):
    __tablename__ = 'cliente'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(16))
    cnpj = db.Column(db.String(16))
    email = db.Column(db.String(100))
    endereco = db.Column(db.String(200))

    atendimentos = db.relationship('Atendimento', backref='cliente', lazy=True)
