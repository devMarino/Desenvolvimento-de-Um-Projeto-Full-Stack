from flask import Blueprint, request, jsonify
from app import db
from app.models.fornecedor import Fornecedor

fornecedor_bp = Blueprint('fornecedor', __name__)

@fornecedor_bp.route('/', methods=['GET'])
def get_all_fornecedores():
    fornecedores = Fornecedor.query.all()
    return jsonify([f.__dict__ for f in fornecedores])

@fornecedor_bp.route('/<int:id>', methods=['GET'])
def get_fornecedor(id):
    fornecedor = Fornecedor.query.get_or_404(id)
    return jsonify(fornecedor.__dict__)

@fornecedor_bp.route('/', methods=['POST'])
def create_fornecedor():
    data = request.get_json()
    novo = Fornecedor(**data)
    db.session.add(novo)
    db.session.commit()
    return jsonify({'message': 'Fornecedor criado'}), 201

@fornecedor_bp.route('/<int:id>', methods=['PUT'])
def update_fornecedor(id):
    data = request.get_json()
    fornecedor = Fornecedor.query.get_or_404(id)
    for k, v in data.items():
        setattr(fornecedor, k, v)
    db.session.commit()
    return jsonify({'message': 'Fornecedor atualizado'})

@fornecedor_bp.route('/<int:id>', methods=['DELETE'])
def delete_fornecedor(id):
    fornecedor = Fornecedor.query.get_or_404(id)
    db.session.delete(fornecedor)
    db.session.commit()
    return jsonify({'message': 'Fornecedor excluído'})
