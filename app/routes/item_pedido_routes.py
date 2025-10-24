from flask import Blueprint, request, jsonify
from app import db
from app.models.item_pedido import ItemPedido

item_pedido_bp = Blueprint('item_pedido', __name__)

@item_pedido_bp.route('/', methods=['GET'])
def get_all_item_pedidos():
    itens = ItemPedido.query.all()
    return jsonify([i.to_dict() for i in itens])

@item_pedido_bp.route('/<int:id>', methods=['GET'])
def get_item_pedido(id):
    item_pedido = ItemPedido.query.get_or_404(id)
    return jsonify(item_pedido.to_dict())

@item_pedido_bp.route('/', methods=['POST'])
def create_item_pedido():
    data = request.get_json()
    novo = ItemPedido(**data)
    db.session.add(novo)
    db.session.commit()
    return jsonify({'message': 'ItemPedido criado com sucesso'}), 201

@item_pedido_bp.route('/<int:id>', methods=['PUT'])
def update_item_pedido(id):
    data = request.get_json()
    item_pedido = ItemPedido.query.get_or_404(id)
    for k, v in data.items():
        setattr(item_pedido, k, v)
    db.session.commit()
    return jsonify({'message': 'ItemPedido atualizado'})

@item_pedido_bp.route('/<int:id>', methods=['DELETE'])
def delete_item_pedido(id):
    item_pedido = ItemPedido.query.get_or_404(id)
    db.session.delete(item_pedido)
    db.session.commit()
    return jsonify({'message': 'ItemPedido excluído'})
