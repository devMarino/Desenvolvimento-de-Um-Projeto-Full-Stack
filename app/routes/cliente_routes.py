from flask import Blueprint, request, jsonify
from app import db
from app.models.cliente import Cliente

cliente_bp = Blueprint('cliente', __name__)

@cliente_bp.route('/', methods=['GET'])
def get_all_clientes():
    clientes = Cliente.query.all()
    return jsonify([c.to_dict() for c in clientes])

@cliente_bp.route('/<int:id>', methods=['GET'])
def get_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    return jsonify(cliente.to_dict())

@cliente_bp.route('/', methods=['POST'])
def create_cliente():
    data = request.get_json()
    novo = Cliente(**data)
    db.session.add(novo)
    db.session.commit()
    return jsonify({'message': 'Cliente criado'}), 201

@cliente_bp.route('/<int:id>', methods=['PUT'])
def update_cliente(id):
    data = request.get_json()
    cliente = Cliente.query.get_or_404(id)
    for k, v in data.items():
        setattr(cliente, k, v)
    db.session.commit()
    return jsonify({'message': 'Cliente atualizado'})

@cliente_bp.route('/<int:id>', methods=['DELETE'])
def delete_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    db.session.delete(cliente)
    db.session.commit()
    return jsonify({'message': 'Cliente excluído'})
