from app import db
from sqlalchemy.inspection import inspect
from datetime import date

class Atendimento(db.Model):
    __tablename__ = 'atendimento'

    id = db.Column(db.Integer, primary_key=True)
    data_atendimento = db.Column(db.Date, nullable=False, default=date.today)
    item_pedido_id = db.Column(db.Integer, db.ForeignKey('item_pedido.id'), nullable=False)

    item_pedido = db.relationship('ItemPedido', back_populates='atendimentos')

    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
