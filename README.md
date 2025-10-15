Sistema de Gestão para Lanchonete

Este projeto é uma aplicação web completa desenvolvida em Flask para o gerenciamento de uma lanchonete. O sistema permite o controle de produtos (cardápio), ingredientes (estoque), e o registro de pedidos. A aplicação também expõe uma API RESTful para manipulação de dados dos produtos.

Este projeto foi desenvolvido como parte da disciplina de Desenvolvimento Web 3 por Gustavo Carvalho.

Funcionalidades

- Autenticação de Usuários: Sistema completo de registro e login com senhas seguras (hashing).
- Proteção de Rotas: Apenas usuários autenticados podem acessar as áreas de gerenciamento.
- CRUD de Produtos:
    - Criação, Leitura, Atualização e Exclusão de produtos do cardápio.
    - Suporte a upload de imagens para cada produto.
- CRUD de Ingredientes:
    - Sistema para gerenciar os ingredientes, incluindo nome, quantidade em estoque e unidade de medida.
- Sistema de Receitas (Muitos-para-Muitos):
    - Associação de múltiplos ingredientes a um único produto, formando uma "receita".
- Gerenciamento de Pedidos:
    - Interface para criar novos pedidos, selecionando produtos e quantidades.
    - Histórico de todos os pedidos realizados, mostrando data, status, itens e usuário responsável.
- API RESTful:
    - Endpoints para `GET`, `POST`, `PUT`, e `DELETE` para a entidade de Produtos, permitindo integração com outros sistemas.

Tecnologias Utilizadas

- Backend: Python 3, Flask
- Banco de Dados: MySQL
- ORM: Flask-SQLAlchemy
- Autenticação: Flask-Login
- Formulários e Segurança: Flask-WTF
- Ambiente: python-dotenv

Como Executar o Projeto

Siga os passos abaixo para configurar e rodar o projeto em um ambiente de desenvolvimento.

1. Pré-requisitos

- Python 3.10+
- Git
- Servidor MySQL instalado e rodando

2. Clonar o Repositório

```bash
git clone [URL_DO_SEU_REPOSITORIO_GIT]
cd [NOME_DA_PASTA_DO_PROJETO]
````

3. Configuração do Ambiente

```bash
# Criar o ambiente virtual
python -m venv .venv

# Ativar o ambiente virtual (Windows PowerShell)
.\.venv\Scripts\Activate.ps1
```

4. Instalar Dependências

Com o ambiente ativado, instale todos os pacotes necessários:

```bash
pip install -r requirements.txt
```

5. Configuração do Banco de Dados

  - Acesse seu cliente MySQL (como o phpMyAdmin).
  - Crie um novo banco de dados chamado `lanchonete_db` com o agrupamento `utf8mb4_unicode_ci`.
  - Crie um novo usuário (ex: `gerente_app`) e conceda a ele todos os privilégios no banco `lanchonete_db`.

6. Variáveis de Ambiente

  - Na raiz do projeto, crie um arquivo chamado `.env`.
  - Copie o conteúdo do arquivo `env.example` (se você criar um) ou adicione as seguintes variáveis, substituindo pelos seus dados:

<!-- end list -->

```
SECRET_KEY="uma_chave_secreta_muito_longa_e_aleatoria_aqui"
DATABASE_URL="mysql+pymysql://gerente_app:sua_senha_do_banco@localhost:3306/lanchonete_db"
```

7. Criar as Tabelas no Banco

  - No terminal do PyCharm, abra o Python Console.
  - Execute os seguintes comandos para criar todas as tabelas:

<!-- end list -->

```python
from dotenv import load_dotenv
load_dotenv()
from app import create_app, db
app = create_app()
with app.app_context():
    db.create_all()
```

8. Iniciar a Aplicação

Finalmente, inicie o servidor Flask:

```bash
flask run
```

A aplicação estará disponível em `http://127.0.0.1:5000`.
