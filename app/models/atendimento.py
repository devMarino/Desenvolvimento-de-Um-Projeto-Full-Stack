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

    @property
    def cliente_obj(self):
        """
        Retorna o cliente relacionado a este atendimento,
        navegando através do item_pedido → pedido → cliente.
        """
        try:
            return self.item_pedido.pedido.cliente
        except AttributeError:
            return None

    def to_dict(self):
        data = {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
        # Se quiser incluir o nome do cliente no dicionário JSON:
        if self.cliente_obj:
            data["cliente_nome"] = self.cliente_obj.nome
        else:
            data["cliente_nome"] = None
        return data