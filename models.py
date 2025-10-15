from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db
from datetime import datetime

receita = db.Table('receita',
    db.Column('produto_id', db.Integer, db.ForeignKey('produto.id'), primary_key=True),
    db.Column('ingrediente_id', db.Integer, db.ForeignKey('ingrediente.id'), primary_key=True)
)

class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(256), nullable=False)
    pedidos = db.relationship('Pedido', backref='usuario', lazy=True)

    def set_senha(self, senha:str) -> None:
        self.senha_hash = generate_password_hash(senha)

    def check_senha(self, senha:str) -> bool:
        return check_password_hash(self.senha_hash, senha)


class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    descricao = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.String(50), nullable=False)
    categoria = db.Column(db.String(50), nullable=False)
    imagem = db.Column(db.String(255), nullable=False, default='default.png')
    pedidos = db.relationship('PedidoItem', back_populates='produto')
    ingredientes = db.relationship('Ingrediente', secondary=receita,
                                   lazy='subquery',
                                   backref=db.backref('produtos', lazy=True))



class Ingrediente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), unique=True, nullable=False)
    estoque_atual = db.Column(db.Float, nullable=False, default=0)
    unidade_medida = db.Column(db.String(20), nullable=False)


class Pedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data_hora = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(50), nullable=False, default='Recebido')
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    itens = db.relationship('PedidoItem', back_populates='pedido', cascade="all, delete-orphan")


class PedidoItem(db.Model):
    __tablename__ = 'pedido_item'
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedido.id'), primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey('produto.id'), primary_key=True)
    quantidade = db.Column(db.Integer, nullable=False)

    pedido = db.relationship('Pedido', back_populates='itens')
    produto = db.relationship('Produto', back_populates='pedidos')

