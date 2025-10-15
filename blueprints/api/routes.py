from flask import jsonify, request, abort
from extensions import db
from models import Produto
from . import api_bp

def produto_to_dict(p: Produto):
    return {
        "id": p.id,
        "nome": p.nome,
        "descricao": p.descricao,
        "preco": str(p.preco),
        "categoria": p.categoria
    }

@api_bp.route("/produtos", methods=["GET"])
def api_listar_produtos():
    produtos = Produto.query.order_by(Produto.nome).all()
    return jsonify([produto_to_dict(p) for p in produtos]), 200

@api_bp.route("/produtos/<int:pk>", methods=["GET"])
def api_obter_produto(pk):
    produto = Produto.query.get_or_404(pk)
    return jsonify(produto_to_dict(produto)), 200

@api_bp.route("/produtos", methods=["POST"])
def api_criar_produto():
    dados = request.get_json(silent=True) or {}

    campos_obrigatorios = ["nome", "preco", "categoria"]
    if not all(campo in dados for campo in campos_obrigatorios):
        mensagem = f"Campos obrigatórios não informados: {', '.join(campos_obrigatorios)}"
        abort(400, description=mensagem)

    p = Produto(
        nome=dados["nome"],
        preco=dados["preco"],
        categoria=dados["categoria"],
        descricao=dados.get("descricao")
    )

    db.session.add(p)
    db.session.commit()

    return jsonify(produto_to_dict(p)), 201


@api_bp.route("/produtos/<int:pk>", methods=["PUT", "PATCH"])
def api_atualizar_produto(pk):
    p = Produto.query.get_or_404(pk)
    dados = request.get_json(silent=True) or {}

    p.nome = dados.get("nome", p.nome)
    p.descricao = dados.get("descricao", p.descricao)
    p.preco = dados.get("preco", p.preco)
    p.categoria = dados.get("categoria", p.categoria)

    db.session.commit()
    return jsonify(produto_to_dict(p)), 200


@api_bp.route("/produtos/<int:pk>", methods=["DELETE"])
def api_excluir_produto(pk):
    p = Produto.query.get_or_404(pk)

    db.session.delete(p)
    db.session.commit()

    return jsonify({"mensagem": "Produto excluído com sucesso"}), 200