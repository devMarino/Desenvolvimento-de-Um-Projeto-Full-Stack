from . import db

class categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)

class produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    categoria = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    fornecedor = db.Column(db.integer, db.foreignkey('fornecedor.id'), nullable=False)

class fornecedor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.string(100), nullable=False)
    telefone = db.Column(db.string(18), nullable=False)
    email = db.Column(db.string(100), nullable=False)
    endereco = db.Column(db.string(200), nullable=False)

class cliente(db.Model):
    id = db.Column(db.integer, primary_key=True)
    nome = db.Column(db.string(100), nullable=False)
    cpf = db.Column(db.string(16), nullable=False)
    cnpj = db.Column(db.string(16), nullable=False)
    email = db.Column(db.string(100), nullable=False)
    endereco = db.Column(db.string(200), nullable=False)

class servico(db.Model):
    id = db.Column(db.integer, primary_key=True)
    nome = db.Column(db.string(100), nullable=False)
    descricao = db.Column(db.string(200), nullable=False)
    valor = db.Column(db.float, nullable=False)

class item_servico(db.Model):
    id = db.Column(db.integer, primary_key=True)
    venda = db.Column(db.integer, db.foreignkey('venda.id'), nullable=False)
    servico = db.Column(db.integer, db.foreignkey('servico.id'), nullable=False)
    valor = db.Column(db.float, nullable=False)
    quantidade = db.Column(db.integer, nullable=False)

class venda(db.Model):
    id = db.Column(db.integer, primary_key=True)
    cliente = db.Column(db.integer, db.foreignkey('cliente.id'), nullable=False)
    data_venda = db.Column(db.datetime, nullable=False)
    total = db.Column(db.float, nullable=False)
    pagamento = db.Column(db.String(50), nullable=False)

class item_venda(db.Model):
    id = db.Column(db.integer, primary_key=True)
    produto = db.Column(db.integer, db.foreignkey('produto.id'), nullable=False)
    venda = db.Column(db.integer, db.foreignkey('venda.id'), nullable=False)
    data_entrega = db.Column(db.datetime, nullable=False)
    endereco_entrega = db.Column(db.string(200), nullable=False)
    status_entrega = db.Column(db.Enum('pendente','entregue', 'cancelado'), nullable=False)

class atendimento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    servico = db.Column(db.Integer, db.ForeignKey('servico.id'), nullable=False)
    data_atendimento = db.Column(db.DateTime, nullable=False)


    def __repr__(self):
        return f'<Task {self.title}>'