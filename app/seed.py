import click
from flask.cli import with_appcontext
from sqlalchemy.exc import IntegrityError
from decimal import Decimal
import random
from datetime import datetime, timedelta

# Importa os modelos do __init__.py da pasta models
from .models import *

@click.command('seed', help='Popula o banco de dados com dados iniciais para testes.')
@with_appcontext
def seed_command():
    """Comando CLI para popular o banco de dados."""
    
    # --- ETAPA ADICIONADA: Limpa dados antigos ---
    try:
        print("➡️ Limpando dados antigos (Atendimento, ItemPedido, Pedido, Item, Cliente, Categoria, Fornecedor)...")
        # Limpa em ordem de dependência (do "filho" para o "pai")
        db.session.query(Atendimento).delete()
        db.session.query(ItemPedido).delete()
        db.session.query(Pedido).delete()
        db.session.query(Item).delete()
        db.session.query(Cliente).delete()
        db.session.query(Categoria).delete()
        db.session.query(Fornecedor).delete()
        db.session.commit()
        print(" ... Dados antigos limpos com sucesso.")
    except Exception as e:
        db.session.rollback()
        print(f"  - ERRO ao limpar dados: {e}")
        print("  - Tentando continuar mesmo assim...")
    # --- FIM DA ETAPA ADICIONADA ---

    # 1. População de Dados de Referência
    seed_categorias()
    seed_fornecedores()
    seed_clientes()
    
    # 2. População de Itens (Unifica Produtos e Serviços)
    seed_items()
    
    # 3. População de Transações 
    seed_transacoes()
    
    print("\n✅ BANCO DE DADOS TOTALMENTE POPULADO (10+ exemplos de cada)!")


# --- FUNÇÕES DE SEEDING BÁSICAS ---

def seed_categorias():
    print("\n➡️ Iniciando seed: CATEGORIAS...")
    # Verifica se já foi populado (agora é seguro, pois limpamos antes)
    if Categoria.query.count() > 0:
        print("  - Categorias já existem. Pulando.")
        return

    categorias_nomes = [
        'Ferramentas Manuais', 'Hidráulica', 'Elétrica', 'Pisos e Revestimentos', 
        'Tintas e Acessórios', 'Cimento e Argamassa', 'Madeiras e Telhados', 
        'Ferragens', 'Jardinagem', 'Iluminação', 'Portas e Janelas'
    ]
    categorias_obj = [Categoria(nome=n) for n in categorias_nomes]
    
    try:
        db.session.add_all(categorias_obj)
        db.session.commit()
        print(f"  - {len(categorias_obj)} Categorias adicionadas.")
    except Exception as e:
        db.session.rollback()
        print(f"  - ERRO ao adicionar categorias: {e}")

def seed_fornecedores():
    print("➡️ Iniciando seed: FORNECEDORES...")
    if Fornecedor.query.count() > 0:
        print("  - Fornecedores já existem. Pulando.")
        return

    fornecedores_data = [
        {'nome': 'Mega Distribuidora BR', 'tel': '(11) 98765-4321', 'email': 'vendas@mega.com', 'end': 'Rua Alfa, 100'},
        {'nome': 'Indústria de Cimentos Forte', 'tel': '(21) 91234-5678', 'email': 'contato@forte.com', 'end': 'Av. Cimento, 50'},
        {'nome': 'Hydra Tech Soluções', 'tel': '(31) 90000-1111', 'email': 'suporte@hydra.com', 'end': 'Rua das Águas, 200'},
        {'nome': 'Eletro Master', 'tel': '(41) 92222-3333', 'email': 'comercial@eletro.com', 'end': 'Av. Fiação, 30'},
        {'nome': 'Tintas do Brasil', 'tel': '(51) 94444-5555', 'email': 'loja@tintasbr.com', 'end': 'Rua do Pigmento, 10'},
        {'nome': 'Madeireira Premium', 'tel': '(61) 96666-7777', 'email': 'madeiras@premium.com', 'end': 'Rod. das Árvores, 5'},
        {'nome': 'Ferragens União', 'tel': '(71) 98888-9999', 'email': 'ferragens@uniao.com', 'end': 'Rua do Aço, 40'},
    ]
    for obj in fornecedores_data:
        db.session.add(Fornecedor(nome=obj['nome'], telefone=obj['tel'], email=obj['email'], endereco=obj['end']))
    try:
        db.session.commit()
        print(f"  - {len(fornecedores_data)} Fornecedores adicionados.")
    except Exception as e:
        db.session.rollback()
        print(f"  - ERRO ao adicionar fornecedores: {e}")

def seed_clientes():
    print("➡️ Iniciando seed: CLIENTES...")
    if Cliente.query.count() > 0:
        print("  - Clientes já existem. Pulando.")
        return
        
    clientes_data = [
        {'nome': 'Marcelo Silva', 'cpf': '123.456.789-00', 'cnpj': None, 'email': 'marcelo@pf.com', 'end': 'Rua das Pessoas, 1'},
        {'nome': 'Construtora Gama', 'cpf': None, 'cnpj': '00.111.222/0001-33', 'email': 'compras@construtora.com', 'end': 'Av. dos Projetos, 20'},
        {'nome': 'Ana Souza', 'cpf': '987.654.321-11', 'cnpj': None, 'email': 'ana@pf.com', 'end': 'Travessa B, 5'},
        {'nome': 'Reforma Rápida ME', 'cpf': None, 'cnpj': '33.444.555/0001-44', 'email': 'contato@reforma.com', 'end': 'Rua dos Empreiteiros, 15'},
        {'nome': 'João Oliveira', 'cpf': '101.202.303-22', 'cnpj': None, 'email': 'joao@pf.com', 'end': 'Rua 7 de Setembro, 88'},
    ]
    for obj in clientes_data:
        db.session.add(Cliente(nome=obj['nome'], cpf=obj['cpf'], cnpj=obj['cnpj'], email=obj['email'], endereco=obj['end']))
    try:
        db.session.commit()
        print(f"  - {len(clientes_data)} Clientes adicionados.")
    except Exception as e:
        db.session.rollback()
        print(f"  - ERRO ao adicionar clientes: {e}")

# --- FUNÇÃO DE SEEDING UNIFICADA (ITEM) ---

def seed_items():
    print("➡️ Iniciando seed: ITENS (Produtos e Serviços)...")
    if Item.query.count() > 0:
        print("  - Itens já existem. Pulando.")
        return
        
    fornecedores_ids = [f.id for f in Fornecedor.query.all()]
    categorias_map = {c.nome: c.id for c in Categoria.query.all()}
    
    itens_data = []

    # 1. DADOS DE PRODUTOS (tipo='PRODUTO', tem estoque)
    # *** CORRIGIDO: Adicionando 'img_url' e + 2 produtos ***
    produtos_data = [
        {'nome': 'Martelo Unha 500g', 'cat': 'Ferramentas Manuais', 'preco': 25.50, 'qtd': 50, 'desc': 'Martelo de alta resistência.', 'img': 'martelo_unha.jpg'},
        {'nome': 'Tubo PVC 100mm', 'cat': 'Hidráulica', 'preco': 45.90, 'qtd': 80, 'desc': 'Tubo para esgoto.', 'img': 'tubo_pvc.jpg'},
        {'nome': 'Fio Flexível 2.5mm', 'cat': 'Elétrica', 'preco': 89.90, 'qtd': 100, 'desc': 'Rolo de 100m.', 'img': 'fio_flexivel.jpg'},
        {'nome': 'Porcelanato Polido 60x60', 'cat': 'Pisos e Revestimentos', 'preco': 59.99, 'qtd': 300, 'desc': 'Caixa com 2m².', 'img': 'porcelanato.jpg'},
        {'nome': 'Tinta Acrílica Branca 18L', 'cat': 'Tintas e Acessórios', 'preco': 250.00, 'qtd': 50, 'desc': 'Galão de tinta profissional.', 'img': 'tinta_acrilica.jpg'},
        {'nome': 'Saco de Cimento CP V 50kg', 'cat': 'Cimento e Argamassa', 'preco': 32.00, 'qtd': 200, 'desc': 'Cimento de alta qualidade.', 'img': 'saco_cimento.jpg'},
        {'nome': 'Telha Cerâmica Romana', 'cat': 'Madeiras e Telhados', 'preco': 3.50, 'qtd': 1000, 'desc': 'Telha tradicional.', 'img': 'telha_ceramica.jpg'},
        {'nome': 'Parafuso Philips 4x40mm (Caixa)', 'cat': 'Ferragens', 'preco': 50.00, 'qtd': 50, 'desc': 'Caixa com 1000 parafusos.', 'img': 'parafuso_philips.jpg'},
        {'nome': 'Lâmpada LED 9W', 'cat': 'Iluminação', 'preco': 10.00, 'qtd': 300, 'desc': 'Lâmpada econômica.', 'img': None},
        # +2 PRODUTOS (como pedido)
        {'nome': 'Chave de Fenda Philips', 'cat': 'Ferramentas Manuais', 'preco': 15.00, 'qtd': 70, 'desc': 'Chave com ponta magnética.', 'img': None},
        {'nome': 'Torneira de Cozinha Bica Alta', 'cat': 'Hidráulica', 'preco': 120.00, 'qtd': 30, 'desc': 'Torneira cromada.', 'img': None},
    ]
    for data in produtos_data:
        cat_id = categorias_map.get(data['cat'])
        if cat_id:
            # Garante que haja fornecedores antes de tentar escolher um
            if not fornecedores_ids:
                print("  - ERRO: Não há fornecedores para associar aos itens.")
                continue
            forn_id = random.choice(fornecedores_ids)
            
            itens_data.append(
                Item(
                    nome=data['nome'], descricao=data['desc'], tipo='PRODUTO', # 'PRODUTO' em ENUM (MAIÚSCULA)
                    categoria_id=cat_id, preco=Decimal(data['preco']), 
                    estoque=data['qtd'], fornecedor_id=forn_id,
                    imagem_url=data['img'] # *** CAMPO ADICIONADO ***
                )
            )

    # 2. DADOS DE SERVIÇOS (tipo='SERVICO', estoque=0)
    servicos_data = [
        {'nome': 'Instalação Elétrica Completa', 'cat': 'Elétrica', 'preco': 350.00, 'desc': 'Mão de obra por ponto de luz/tomada.'},
        {'nome': 'Consultoria de Cores', 'cat': 'Tintas e Acessórios', 'preco': 80.00, 'desc': 'Ajuda especializada na escolha de tintas.'},
        {'nome': 'Conserto Hidráulico', 'cat': 'Hidráulica', 'preco': 150.00, 'desc': 'Reparo de vazamentos.'},
        {'nome': 'Assentamento de Piso (m²)', 'cat': 'Pisos e Revestimentos', 'preco': 45.00, 'desc': 'Valor por m² instalado.'},
    ]
    for data in servicos_data:
        cat_id = categorias_map.get(data['cat'])
        if cat_id:
            if not fornecedores_ids:
                print("  - ERRO: Não há fornecedores para associar aos itens.")
                continue
            forn_id = random.choice(fornecedores_ids)
            
            itens_data.append(
                Item(
                    nome=data['nome'], descricao=data['desc'], tipo='SERVICO', # 'SERVICO' em ENUM (MAIÚSCULA)
                    categoria_id=cat_id, preco=Decimal(data['preco']), 
                    estoque=0, fornecedor_id=forn_id, # Estoque 0 ou nulo para serviço
                    imagem_url=None # Serviços não têm imagem
                )
            )

    try:
        db.session.add_all(itens_data)
        db.session.commit()
        print(f"  - {len(itens_data)} Itens (Produtos e Serviços) adicionados.")
    except Exception as e:
        db.session.rollback()
        print(f"  - ERRO ao adicionar itens: {e}")

# --- FUNÇÃO DE SEEDING DE TRANSAÇÕES ---

def seed_transacoes():
    print("➡️ Iniciando seed: TRANSAÇÕES (Pedido -> Item_Pedido -> Atendimento)...")

    clientes_obj = Cliente.query.all()
    itens_obj = Item.query.all()
    
    if not (clientes_obj and itens_obj):
        print("  - Dados mestres (Clientes e Itens) insuficientes. Pulando transações.")
        return

    pedidos_list = []
    itens_pedido_list = []
    atendimentos_list = []
    
    NUM_TRANSACOES = 15 # Criando 15 pedidos de exemplo

    for i in range(1, NUM_TRANSACOES + 1):
        data_transacao = datetime.now() - timedelta(days=random.randint(1, 90))
        cli = random.choice(clientes_obj)
        
        # 1. Cria o PEDIDO
        status_opcoes = ['CANCELADO', 'PENDENTE', 'ENTREGUE'] 
        
        novo_pedido = Pedido(
            cliente_id=cli.id,
            preco_total=Decimal('0.00'),
            status=random.choice(status_opcoes)
        )
        db.session.add(novo_pedido)
        db.session.flush() # Pega o ID do novo_pedido antes do commit
        
        preco_total_pedido = Decimal('0.00')

        # 2. Adiciona ITENS_PEDIDO
        num_itens_para_pedido = random.randint(1, min(3, len(itens_obj)))
        itens_para_pedido = random.sample(itens_obj, k=num_itens_para_pedido)
        
        item_pedido_para_atendimento = None 

        for it in itens_para_pedido:
            # Quantidade (1-5 para produto, 1 para serviço)
            qtd = random.randint(1, 5) if it.tipo == 'PRODUTO' else 1
            
            item_p = ItemPedido(
                pedido_id=novo_pedido.id,
                item_id=it.id,
                quantidade=qtd
            )
            itens_pedido_list.append(item_p)
            db.session.add(item_p)
            
            # Calcula o preço total do pedido
            preco_total_pedido += (it.preco * qtd)
            
            # Guarda o primeiro ItemPedido para o Atendimento
            if item_pedido_para_atendimento is None:
                item_pedido_para_atendimento = item_p
                
        db.session.flush() # Pega os IDs dos item_p

        # 3. Cria o ATENDIMENTO (somente se não for cancelado e houver um item_pedido)
        if novo_pedido.status != 'CANCELADO' and item_pedido_para_atendimento:
            novo_atendimento = Atendimento(
                data_atendimento=data_transacao,
                item_pedido_id=item_pedido_para_atendimento.id
            )
            atendimentos_list.append(novo_atendimento)
            db.session.add(novo_atendimento)

        # 4. Atualiza o Total do Pedido
        novo_pedido.preco_total = preco_total_pedido
        pedidos_list.append(novo_pedido)

    try:
        db.session.commit()
        print(f"  - {len(pedidos_list)} Pedidos criados.")
        print(f"  - {len(itens_pedido_list)} Itens de Pedido criados.")
        print(f"  - {len(atendimentos_list)} Atendimentos criados.") 
    except Exception as e:
        db.session.rollback()
        print(f"  - ERRO ao adicionar transações: {e}")

# Função que será usada no __init__.py para registrar o comando
def init_cli(app):
    app.cli.add_command(seed_command)