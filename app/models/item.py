# Dentro de Desenvolvimento-de-Um-Projeto-Full-Stack-main/app/models/item.py

from app import db
from sqlalchemy.inspection import inspect
from sqlalchemy.types import Enum # Import Enum

# Import Decimal para conversão no to_dict
from decimal import Decimal

class Item(db.Model):
    __tablename__ = 'item'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(300), nullable=True) # Alterado para nullable=True (como no original)
    preco = db.Column(db.Numeric(10, 2), nullable=False)

    # Verifica se o Enum está definido como 'PRODUTO'/'SERVICO' ou 'produto'/'servico'
    # Use o que for compatível com o resto do seu projeto. O frontend original usava minúsculas.
    # Vamos usar minúsculas aqui para compatibilidade com o frontend copiado.
    tipo = db.Column(Enum('produto', 'servico', name='item_tipo'), nullable=False)

    estoque = db.Column(db.Integer, nullable=True) # Alterado para nullable=True (serviços não têm estoque)

    # --- CAMPO ADICIONADO ---
    # Necessário para o template index.html e carrinho.js
    imagem_url = db.Column(db.String(100), nullable=True)
    # --- FIM DA ADIÇÃO ---

    # Chaves estrangeiras e relacionamentos (verifique se os nomes das tabelas/classes estão corretos)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=False)
    fornecedor_id = db.Column(db.Integer, db.ForeignKey('fornecedor.id'), nullable=False)

    # Relacionamentos (verifique os nomes em back_populates nos outros modelos)
    categoria = db.relationship('Categoria', back_populates='itens')
    fornecedor = db.relationship('Fornecedor', back_populates='itens')
    itens_pedido = db.relationship('ItemPedido', back_populates='item')
    # Adicione o relacionamento para Atendimento se o seu modelo Atendimento tiver um ForeignKey para item
    # atendimentos = db.relationship('Atendimento', back_populates='item_obj') # Exemplo

    # --- MÉTODO ADICIONADO ---
    # Necessário para a rota /api/item/<int:id> em frontend_routes.py
    def to_dict(self):
        """Converte o objeto item para um dicionário compatível com JSON."""
        return {
            'id': self.id,
            'nome': self.nome,
            'descricao': self.descricao,
            # Converte Decimal para float, essencial para JSON e JavaScript
            'preco': float(self.preco) if isinstance(self.preco, Decimal) else self.preco,
            'tipo': self.tipo,
            'estoque': self.estoque,
            'imagem_url': self.imagem_url, # Inclui o novo campo
            'categoria_id': self.categoria_id,
            'fornecedor_id': self.fornecedor_id
            # Adicione outros campos se necessário
        }
    # --- FIM DO MÉTODO ---