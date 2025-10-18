import click
from flask.cli import with_appcontext
from sqlalchemy.exc import IntegrityError
from decimal import Decimal
import random
from datetime import datetime, timedelta

from .models import * # Importa todos os modelos definidos


@click.command('seed', help='Popula o banco de dados com dados iniciais para testes.')
@with_appcontext
def seed_command():
    """Comando CLI para popular o banco de dados."""
    
    # 1. População de Dados de Referência
    seed_categorias()
    seed_fornecedores()
    seed_clientes()
    
    # 2. População de Itens (Unifica Produtos e Serviços)
    seed_items()
    
    # 3. População de Transações (Fluxo: Atendimento -> Pedido -> Item_Pedido)
    seed_transacoes()
    
    print("\n✅ BANCO DE DADOS TOTALMENTE POPULADO (10+ exemplos de cada)!")


# --- FUNÇÕES DE SEEDING BÁSICAS (Sem alterações) ---

def seed_categorias():
    print("\n➡️ Iniciando seed: CATEGORIAS...")
    if categoria.query.count() > 0:
        print("  - Categorias já existem. Pulando.")
        return

    categorias_nomes = [
        'Ferramentas Manuais', 'Hidráulica', 'Elétrica', 'Pisos e Revestimentos', 
        'Tintas e Acessórios', 'Cimento e Argamassa', 'Madeiras e Telhados', 
        'Ferragens', 'Jardinagem', 'Iluminação', 'Portas e Janelas'
    ]
    categorias_obj = [categoria(nome=n) for n in categorias_nomes]
    
    try:
        db.session.add_all(categorias_obj)
        db.session.commit()
        print(f"  - {len(categorias_obj)} Categorias adicionadas.")
    except Exception as e:
        db.session.rollback()
        print(f"  - ERRO ao adicionar categorias: {e}")

def seed_fornecedores():
    print("➡️ Iniciando seed: FORNECEDORES...")
    if fornecedor.query.count() > 0:
        print("  - Fornecedores já existem. Pulando.")
        return

    # Dados de Fornecedores
    fornecedores_data = [
        {'nome': 'Mega Distribuidora BR', 'tel': '(11) 98765-4321', 'email': 'vendas@mega.com', 'end': 'Rua Alfa, 100'},
        {'nome': 'Indústria de Cimentos Forte', 'tel': '(21) 91234-5678', 'email': 'contato@forte.com', 'end': 'Av. Cimento, 50'},
        {'nome': 'Hydra Tech Soluções', 'tel': '(31) 90000-1111', 'email': 'suporte@hydra.com', 'end': 'Rua das Águas, 200'},
        {'nome': 'Eletro Master', 'tel': '(41) 92222-3333', 'email': 'comercial@eletro.com', 'end': 'Av. Fiação, 30'},
        {'nome': 'Tintas do Brasil', 'tel': '(51) 94444-5555', 'email': 'loja@tintasbr.com', 'end': 'Rua do Pigmento, 10'},
        {'nome': 'Madeireira Premium', 'tel': '(61) 96666-7777', 'email': 'madeiras@premium.com', 'end': 'Rod. das Árvores, 5'},
        {'nome': 'Ferragens União', 'tel': '(71) 98888-9999', 'email': 'ferragens@uniao.com', 'end': 'Rua do Aço, 40'},
        {'nome': 'Jardim Verde', 'tel': '(81) 91010-1010', 'email': 'jardim@verde.com', 'end': 'Rua das Flores, 15'},
        {'nome': 'Lux Iluminação', 'tel': '(91) 91212-1212', 'email': 'lux@ilumina.com', 'end': 'Av. da Luz, 80'},
        {'nome': 'Portas & Cia', 'tel': '(11) 93434-3434', 'email': 'portas@cia.com', 'end': 'Rua das Esquadrias, 12'},
    ]
    
    for obj in fornecedores_data:
        db.session.add(fornecedor(nome=obj['nome'], telefone=obj['tel'], email=obj['email'], endereco=obj['end']))

    try:
        db.session.commit()
        print(f"  - {len(fornecedores_data)} Fornecedores adicionados.")
    except Exception as e:
        db.session.rollback()
        print(f"  - ERRO ao adicionar fornecedores: {e}")

def seed_clientes():
    print("➡️ Iniciando seed: CLIENTES...")
    if cliente.query.count() > 0:
        print("  - Clientes já existem. Pulando.")
        return
        
    # Dados de Clientes
    clientes_data = [
        {'nome': 'Marcelo Silva', 'cpf': '123.456.789-00', 'cnpj': None, 'email': 'marcelo@pf.com', 'end': 'Rua das Pessoas, 1'},
        {'nome': 'Construtora Gama', 'cpf': None, 'cnpj': '00.111.222/0001-33', 'email': 'compras@construtora.com', 'end': 'Av. dos Projetos, 20'},
        {'nome': 'Ana Souza', 'cpf': '987.654.321-11', 'cnpj': None, 'email': 'ana@pf.com', 'end': 'Travessa B, 5'},
        {'nome': 'Reforma Rápida ME', 'cpf': None, 'cnpj': '33.444.555/0001-44', 'email': 'contato@reforma.com', 'end': 'Rua dos Empreiteiros, 15'},
        {'nome': 'João Oliveira', 'cpf': '101.202.303-22', 'cnpj': None, 'email': 'joao@pf.com', 'end': 'Rua 7 de Setembro, 88'},
        {'nome': 'Elétrica Segura Ltda', 'cpf': None, 'cnpj': '66.777.888/0001-55', 'email': 'financeiro@eletrica.com', 'end': 'Av. dos Eletricistas, 10'},
        {'nome': 'Maria Santos', 'cpf': '404.505.606-33', 'cnpj': None, 'email': 'maria@pf.com', 'end': 'Rua do Porto, 30'},
        {'nome': 'Pinturas Artísticas', 'cpf': None, 'cnpj': '99.000.111/0001-66', 'email': 'pinturas@artistica.com', 'end': 'Rua do Aquarela, 5'},
        {'nome': 'Carlos Ferreira', 'cpf': '707.808.909-44', 'cnpj': None, 'email': 'carlos@pf.com', 'end': 'Rua da Praia, 12'},
        {'nome': 'Pedro Rocha', 'cpf': '111.222.333-55', 'cnpj': None, 'email': 'pedro@pf.com', 'end': 'Rua da Montanha, 25'},
        {'nome': 'Loja de Bairros', 'cpf': None, 'cnpj': '12.345.678/0001-90', 'email': 'bairros@loja.com', 'end': 'Rua do Comércio, 3'}
    ]
    
    for obj in clientes_data:
        db.session.add(cliente(nome=obj['nome'], cpf=obj['cpf'], cnpj=obj['cnpj'], email=obj['email'], endereco=obj['end']))
    
    try:
        db.session.commit()
        print(f"  - {len(clientes_data)} Clientes adicionados.")
    except Exception as e:
        db.session.rollback()
        print(f"  - ERRO ao adicionar clientes: {e}")

# --- FUNÇÃO DE SEEDING UNIFICADA (ITEM) ---

def seed_items():
    print("➡️ Iniciando seed: ITENS (Produtos e Serviços)...")
    if item.query.count() > 0:
        print("  - Itens já existem. Pulando.")
        return
        
    # Obtendo IDs para relacionamento
    fornecedores_ids = [f.id for f in fornecedor.query.all()]
    categorias_map = {c.nome: c.id for c in categoria.query.all()}
    
    itens_data = []

    # 1. DADOS DE PRODUTOS (tipo='produto', tem estoque)
    produtos_data = [
        {'nome': 'Martelo Unha 500g', 'cat': 'Ferramentas Manuais', 'preco': 25.50, 'qtd': 50, 'desc': 'Martelo de alta resistência.'},
        {'nome': 'Tubo PVC 100mm', 'cat': 'Hidráulica', 'preco': 45.90, 'qtd': 80, 'desc': 'Tubo para esgoto.'},
        {'nome': 'Fio Flexível 2.5mm', 'cat': 'Elétrica', 'preco': 89.90, 'qtd': 100, 'desc': 'Rolo de 100m.'},
        {'nome': 'Porcelanato Polido 60x60', 'cat': 'Pisos e Revestimentos', 'preco': 59.99, 'qtd': 300, 'desc': 'Caixa com 2m².'},
        {'nome': 'Tinta Acrílica Branca 18L', 'cat': 'Tintas e Acessórios', 'preco': 250.00, 'qtd': 50, 'desc': 'Galão de tinta profissional.'},
        {'nome': 'Saco de Cimento CP V 50kg', 'cat': 'Cimento e Argamassa', 'preco': 32.00, 'qtd': 200, 'desc': 'Cimento de alta qualidade.'},
        {'nome': 'Telha Cerâmica Romana', 'cat': 'Madeiras e Telhados', 'preco': 3.50, 'qtd': 1000, 'desc': 'Telha tradicional.'},
        {'nome': 'Parafuso Philips 4x40mm (Caixa)', 'cat': 'Ferragens', 'preco': 50.00, 'qtd': 50, 'desc': 'Caixa com 1000 parafusos.'},
        {'nome': 'Lâmpada LED 9W', 'cat': 'Iluminação', 'preco': 10.00, 'qtd': 300, 'desc': 'Lâmpada econômica.'},
    ]
    for data in produtos_data:
        cat_id = categorias_map.get(data['cat'])
        if cat_id:
            forn_id = random.choice(fornecedores_ids)
            itens_data.append(
                item(
                    nome=data['nome'], descricao=data['desc'], tipo='produto',
                    categoria_id=cat_id, preco=Decimal(data['preco']), 
                    estoque=data['qtd'], fornecedor_id=forn_id
                )
            )

    # 2. DADOS DE SERVIÇOS (tipo='servico', estoque=None)
    servicos_data = [
        {'nome': 'Instalação Elétrica Completa', 'cat': 'Elétrica', 'preco': 350.00, 'desc': 'Mão de obra por ponto de luz/tomada.'},
        {'nome': 'Consultoria de Cores', 'cat': 'Tintas e Acessórios', 'preco': 80.00, 'desc': 'Ajuda especializada na escolha de tintas.'},
        {'nome': 'Conserto Hidráulico', 'cat': 'Hidráulica', 'preco': 150.00, 'desc': 'Reparo de vazamentos.'},
        {'nome': 'Assentamento de Piso (m²)', 'cat': 'Pisos e Revestimentos', 'preco': 45.00, 'desc': 'Valor por m² instalado.'},
        {'nome': 'Pintura Residencial (m²)', 'cat': 'Tintas e Acessórios', 'preco': 20.00, 'desc': 'Mão de obra por m² pintado.'},
        {'nome': 'Corte de Madeira (unidade)', 'cat': 'Madeiras e Telhados', 'preco': 5.00, 'desc': 'Serviço de corte sob medida.'},
    ]
    for data in servicos_data:
        cat_id = categorias_map.get(data['cat'])
        if cat_id:
            forn_id = random.choice(fornecedores_ids)
            itens_data.append(
                item(
                    nome=data['nome'], descricao=data['desc'], tipo='servico',
                    categoria_id=cat_id, preco=Decimal(data['preco']), 
                    estoque=None, fornecedor_id=forn_id # Estoque é None para serviços
                )
            )

    try:
        db.session.add_all(itens_data)
        db.session.commit()
        print(f"  - {len(itens_data)} Itens (Produtos e Serviços) adicionados.")
    except Exception as e:
        db.session.rollback()
        print(f"  - ERRO ao adicionar itens: {e}")

# --- FUNÇÃO DE SEEDING DE TRANSAÇÕES ATUALIZADA ---

def seed_transacoes():
    print("➡️ Iniciando seed: TRANSAÇÕES (Atendimento -> Pedido -> Item_Pedido)...")

    # Garante que há dados mestre para relacionamento
    clientes_obj = cliente.query.all()
    itens_obj = item.query.all()
    if not (clientes_obj and itens_obj):
        print("  - Dados mestres insuficientes. Pulando transações.")
        return

    # Mapeamento para facilitar: Produtos e Serviços
    produtos = [i for i in itens_obj if i.tipo == 'produto']
    servicos = [i for i in itens_obj if i.tipo == 'servico']

    atendimentos_list = []
    pedidos_list = []
    itens_pedido_list = []

    # Criar 20 Transações
    for i in range(1, 21):
        data_transacao = datetime.now() - timedelta(days=random.randint(1, 90))
        cli = random.choice(clientes_obj)
        
        # 1. Cria o ATENDIMENTO
        novo_atendimento = atendimento(
            cliente_id=cli.id,
            data_atendimento=data_transacao
        )
        db.session.add(novo_atendimento)
        db.session.flush() # Para que 'novo_atendimento' tenha um ID

        # 2. Cria o PEDIDO (ligado ao atendimento)
        status_opcoes = ['pendente', 'confirmado', 'cancelado']
        novo_pedido = pedido(
            atendimento_id=novo_atendimento.id,
            preco_total=Decimal('0.00'), # Será atualizado
            status=random.choice(status_opcoes)
        )
        db.session.add(novo_pedido)
        db.session.flush() # Para que 'novo_pedido' tenha um ID
        
        preco_total_pedido = Decimal('0.00')

        # 3. Adiciona 1 a 4 ITENS_PEDIDO (Produtos e/ou Serviços)
        
        # 3. Adiciona ITENS_PEDIDO (Produtos e/ou Serviços)

        # --- Seleção de Produtos ---
        # Máximo de 3 produtos, mas nunca mais do que a quantidade que temos disponível
        max_produtos_a_pegar = min(3, len(produtos))
        if max_produtos_a_pegar > 0:
            num_produtos = random.randint(1, max_produtos_a_pegar)
            itens_produtos = random.sample(produtos, k=num_produtos)
        else:
            itens_produtos = []

        # --- Seleção de Serviços ---
        # Máximo de 2 serviços, mas nunca mais do que a quantidade que temos disponível
        max_servicos_a_pegar = min(2, len(servicos))
        if max_servicos_a_pegar > 0:
            num_servicos = random.randint(1, max_servicos_a_pegar)
            itens_servicos = random.sample(servicos, k=num_servicos)
        else:
            itens_servicos = []

        # Combina as listas
        itens_selecionados = itens_produtos + itens_servicos

        # Se não conseguimos selecionar nada (o que é raro, mas possível), pulamos
        if not itens_selecionados: 
            continue 

        # O número de itens a adicionar ao pedido é no máximo 4, mas nunca mais do que a lista selecionada
        max_itens_no_pedido = min(4, len(itens_selecionados))
        num_itens_para_pedido = random.randint(1, max_itens_no_pedido)

        # Seleciona a amostra final para o pedido
        itens_para_pedido = random.sample(itens_selecionados, k=num_itens_para_pedido)

        for it in itens_para_pedido:
            qtd = random.randint(1, 5) if it.tipo == 'produto' else random.randint(1, 2)
            
            item_p = item_pedido(
                pedido_id=novo_pedido.id,
                item_id=it.id,
                quantidade=qtd
            )
            itens_pedido_list.append(item_p)
            
            preco_total_pedido += it.preco * qtd
            db.session.add(item_p)

        # 4. Atualiza o Total do Pedido
        novo_pedido.preco_total = preco_total_pedido
        atendimentos_list.append(novo_atendimento)
        pedidos_list.append(novo_pedido)

    try:
        db.session.commit()
        print(f"  - {len(atendimentos_list)} Atendimentos criados.")
        print(f"  - {len(pedidos_list)} Pedidos criados.")
        print(f"  - {len(itens_pedido_list)} Itens de Pedido criados.")
    except Exception as e:
        db.session.rollback()
        print(f"  - ERRO ao adicionar transações: {e}")


# Função que será usada no __init__.py para registrar o comando
def init_cli(app):
    app.cli.add_command(seed_command)