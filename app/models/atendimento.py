from app import db

class Atendimento(db.Model):
    __tablename__ = 'atendimento'

    id = db.Column(db.Integer, primary_key=True)
    data_atendimento = db.Column(db.Date, nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)

    itens_pedido = db.relationship('ItemPedido', backref='atendimento', lazy=True)
