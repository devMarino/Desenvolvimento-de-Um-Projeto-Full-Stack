from flask import Blueprint, request, jsonify
from app import db
from app.models.pedido import Pedido

pedido_bp = Blueprint('pedido', __name__)

@pedido_bp.route('/', methods=['GET'])
def get_all_pedidos():
    pedidos = Pedido.query.all()
    return jsonify([p.to_dict() for p in pedidos])

@pedido_bp.route('/<int:id>', methods=['GET'])
def get_pedido(id):
    pedido = Pedido.query.get_or_404(id)
    return jsonify(pedido.to_dict())

@pedido_bp.route('/', methods=['POST'])
def create_pedido():
    data = request.get_json()
    novo = Pedido(**data)
    db.session.add(novo)
    db.session.commit()
    return jsonify({'message': 'Pedido criado com sucesso'}), 201

@pedido_bp.route('/<int:id>', methods=['PUT'])
def update_pedido(id):
    data = request.get_json()
    pedido = Pedido.query.get_or_404(id)
    for k, v in data.items():
        setattr(pedido, k, v)
    db.session.commit()
    return jsonify({'message': 'Pedido atualizado'})

@pedido_bp.route('/<int:id>', methods=['DELETE'])
def delete_pedido(id):
    pedido = Pedido.query.get_or_404(id)
    db.session.delete(pedido)
    db.session.commit()
    return jsonify({'message': 'Pedido excluído'})
