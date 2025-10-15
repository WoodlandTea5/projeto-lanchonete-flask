import os
from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, login_required, current_user
from . import web_bp
from .forms import LoginForm, RegistroForm, ProdutoForm, IngredienteForm
from extensions import db
from models import Usuario, Produto, Ingrediente, Pedido, PedidoItem
from werkzeug.utils import secure_filename

@web_bp.route("/")
def index():
    return render_template("layout.html")

@web_bp.route("/registro", methods=["GET", "POST"])
def registro():
    form = RegistroForm()
    if form.validate_on_submit():
        if Usuario.query.filter_by(email=form.email.data).first():
            flash("E-mail já cadastrado.", "warning")
            return redirect(url_for("web.registro"))
        u = Usuario(nome=form.nome.data, email=form.email.data)
        u.set_senha(form.senha.data)

        db.session.add(u)
        db.session.commit()

        flash("Conta criada. Faça login.", "success")
        return redirect(url_for("web.login"))

    return render_template("registro.html", form=form)

@web_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        u = Usuario.query.filter_by(email=form.email.data).first()
        if u and u.check_senha(form.senha.data):
            login_user(u)
            return redirect(url_for("web.lista_produtos"))
        flash("Credenciais inválidas.", "danger")
    return render_template("login.html", form=form)

@web_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("web.login"))


@web_bp.route("/produtos")
@login_required
def lista_produtos():
    q = request.args.get("q", "").strip()
    query = Produto.query

    if q:
        query = query.filter(
            (Produto.nome.ilike(f"%{q}%")) | (Produto.categoria.ilike(f"%{q}%"))
        )

    produtos = query.order_by(Produto.nome).all()

    return render_template("lista.html", itens=produtos, busca=q)


@web_bp.route("/produtos/novo", methods=["GET", "POST"])
@login_required
def novo_produto():
    form = ProdutoForm()
    form.ingredientes.choices = [(i.id, i.nome) for i in Ingrediente.query.order_by('nome').all()]

    if form.validate_on_submit():
        nome_imagem = 'default.png'
        if form.imagem.data:
            nome_imagem = secure_filename(form.imagem.data.filename)
            caminho_salvamento = os.path.join(
                current_app.root_path, 'static/img', nome_imagem
            )
            form.imagem.data.save(caminho_salvamento)

        novo_produto = Produto(
            nome=form.nome.data,
            descricao=form.descricao.data,
            preco=form.preco.data,
            categoria=form.categoria.data,
            imagem=nome_imagem
        )
        ingredientes_selecionados = Ingrediente.query.filter(Ingrediente.id.in_(form.ingredientes.data)).all()
        novo_produto.ingredientes.extend(ingredientes_selecionados)

        db.session.add(novo_produto)
        db.session.commit()

        flash("Produto cadastrado com sucesso.", "success")
        return redirect(url_for("web.lista_produtos"))

    return render_template("editar.html", form=form, item=None)


@web_bp.route("/produtos/<int:pk>/editar", methods=["GET", "POST"])
@login_required
def editar_produto(pk):
    produto = Produto.query.get_or_404(pk)
    form = ProdutoForm(obj=produto)
    form.ingredientes.choices = [(i.id, i.nome) for i in Ingrediente.query.order_by('nome').all()]

    if form.validate_on_submit():
        produto.nome = form.nome.data
        produto.descricao = form.descricao.data
        produto.preco = form.preco.data
        produto.categoria = form.categoria.data

        if form.imagem.data:
            nome_imagem = secure_filename(form.imagem.data.filename)
            caminho_salvamento = os.path.join(
                current_app.root_path, 'static/img', nome_imagem
            )
            form.imagem.data.save(caminho_salvamento)
            produto.imagem = nome_imagem

        produto.ingredientes.clear()
        ingredientes_selecionados = Ingrediente.query.filter(Ingrediente.id.in_(form.ingredientes.data)).all()
        produto.ingredientes.extend(ingredientes_selecionados)

        db.session.commit()
        flash("Produto atualizado com sucesso.", "success")
        return redirect(url_for("web.lista_produtos"))

    if request.method == 'GET':
        form.ingredientes.data = [ingrediente.id for ingrediente in produto.ingredientes]
        form.preco.data = float(produto.preco)

    return render_template("editar.html", form=form, item=produto)


@web_bp.route("/produtos/<int:pk>/excluir", methods=["POST"])
@login_required
def excluir_produto(pk):
    produto = Produto.query.get_or_404(pk)
    db.session.delete(produto)
    db.session.commit()
    flash("Produto excluído.", "info")
    return redirect(url_for("web.lista_produtos"))


@web_bp.route("/ingredientes")
@login_required
def lista_ingredientes():
    ingredientes = Ingrediente.query.order_by(Ingrediente.nome).all()
    return render_template("lista_ingredientes.html", itens=ingredientes)


@web_bp.route("/ingredientes/novo", methods=["GET", "POST"])
@login_required
def novo_ingrediente():
    form = IngredienteForm()
    if form.validate_on_submit():
        ingrediente = Ingrediente(
            nome=form.nome.data,
            estoque_atual=form.estoque_atual.data,
            unidade_medida=form.unidade_medida.data
        )
        db.session.add(ingrediente)
        db.session.commit()
        flash("Ingrediente cadastrado com sucesso.", "success")
        return redirect(url_for("web.lista_ingredientes"))
    return render_template("editar_ingrediente.html", form=form, item=None)


@web_bp.route("/ingredientes/<int:pk>/editar", methods=["GET", "POST"])
@login_required
def editar_ingrediente(pk):
    ingrediente = Ingrediente.query.get_or_404(pk)
    form = IngredienteForm(obj=ingrediente)
    if form.validate_on_submit():
        ingrediente.nome = form.nome.data
        ingrediente.estoque_atual = form.estoque_atual.data
        ingrediente.unidade_medida = form.unidade_medida.data
        db.session.commit()
        flash("Ingrediente atualizado com sucesso.", "success")
        return redirect(url_for("web.lista_ingredientes"))
    return render_template("editar_ingrediente.html", form=form, item=ingrediente)


@web_bp.route("/pedidos/novo", methods=['GET', 'POST'])
@login_required
def novo_pedido():
    if request.method == 'POST':
        novo_pedido = Pedido(usuario_id=current_user.id)
        db.session.add(novo_pedido)

        for key, value in request.form.items():
            if key.startswith('quantidade-'):
                produto_id = int(key.split('-')[1])
                quantidade = int(value)

                if quantidade > 0:
                    produto = Produto.query.get(produto_id)
                    item_pedido = PedidoItem(
                        pedido=novo_pedido,
                        produto=produto,
                        quantidade=quantidade
                    )
                    db.session.add(item_pedido)

                    for ingrediente in item_pedido.produto.ingredientes:
                        ingrediente.estoque_atual -= item_pedido.quantidade

        db.session.commit()
        flash('Pedido criado com sucesso!', 'success')
        return redirect(url_for('web.lista_pedidos'))

    produtos = Produto.query.order_by(Produto.categoria, Produto.nome).all()
    return render_template('novo_pedido.html', produtos=produtos)


@web_bp.route("/pedidos")
@login_required
def lista_pedidos():
    pedidos = Pedido.query.order_by(Pedido.data_hora.desc()).all()
    return render_template('lista_pedidos.html', pedidos=pedidos)
