from dotenv import load_dotenv
load_dotenv()
from app import create_app, db
from models import Ingrediente, Produto

# Cria uma instância da aplicação para ter acesso ao contexto
app = create_app()

# O "with app.app_context()" garante que a aplicação sabe qual banco de dados usar
with app.app_context():
    print("Iniciando o povoamento do banco de dados...")

    # Limpa as tabelas para evitar duplicatas ao rodar o script várias vezes
    # CUIDADO: Isso apaga todos os produtos e ingredientes existentes!
    db.session.query(Produto).delete()
    db.session.query(Ingrediente).delete()

    # Adiciona os ingredientes
    lista_ingredientes = [
        {'nome': 'Pão de Hambúrguer', 'estoque_atual': 100, 'unidade_medida': 'unidade'},
        {'nome': 'Hambúrguer Artesanal 150g', 'estoque_atual': 80, 'unidade_medida': 'unidade'},
        {'nome': 'Queijo Mussarela Fatiado', 'estoque_atual': 3000, 'unidade_medida': 'g'},
        {'nome': 'Bacon em Tiras', 'estoque_atual': 2000, 'unidade_medida': 'g'},
        {'nome': 'Alface Crespa', 'estoque_atual': 10, 'unidade_medida': 'unidade'},
        {'nome': 'Tomate', 'estoque_atual': 5000, 'unidade_medida': 'g'},
        {'nome': 'Batata Palito Congelada', 'estoque_atual': 10000, 'unidade_medida': 'g'},
        {'nome': 'Creme de Cheddar', 'estoque_atual': 1500, 'unidade_medida': 'g'},
        {'nome': 'Refrigerante Lata', 'estoque_atual': 200, 'unidade_medida': 'unidade'},
        {'nome': 'Polpa de Açaí Congelada', 'estoque_atual': 5000, 'unidade_medida': 'g'}
    ]

    for item in lista_ingredientes:
        ingrediente = Ingrediente(**item)  # O ** desempacota o dicionário
        db.session.add(ingrediente)

    print(f"{len(lista_ingredientes)} ingredientes adicionados.")

    # Adiciona os produtos
    lista_produtos = [
        {
            'nome': 'X-Bacon Clássico',
            'descricao': 'Pão, hambúrguer de 150g, queijo mussarela, bacon em tiras e alface.',
            'preco': 28.00,
            'categoria': 'Lanche',
            'imagem': 'default.png'
        },
        {
            'nome': 'Batata com Cheddar e Bacon',
            'descricao': 'Porção generosa de 400g de batata frita, coberta com creme de cheddar e bacon.',
            'preco': 25.00,
            'categoria': 'Porção',
            'imagem': 'default.png'
        },
        {
            'nome': 'Refrigerante',
            'descricao': 'Lata 350ml (diversos sabores).',
            'preco': 7.00,
            'categoria': 'Bebida',
            'imagem': 'default.png'
        }
    ]

    for item in lista_produtos:
        produto = Produto(**item)
        db.session.add(produto)

    print(f"{len(lista_produtos)} produtos adicionados.")

    # Efetiva as mudanças no banco de dados
    db.session.commit()

    print("Banco de dados populado com sucesso!")