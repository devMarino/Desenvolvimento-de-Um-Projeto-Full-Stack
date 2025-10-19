from flask import Blueprint, request, jsonify
from app import db
from app.models.categoria import Categoria

categoria_bp = Blueprint('categoria', __name__)

@categoria_bp.route('/', methods=['GET'])
def get_all_categorias():
    categorias = Categoria.query.all()
    return jsonify([c.__dict__ for c in categorias])

@categoria_bp.route('/<int:id>', methods=['GET'])
def get_categoria(id):
    categoria = Categoria.query.get_or_404(id)
    return jsonify(categoria.__dict__)

@categoria_bp.route('/', methods=['POST'])
def create_categoria():
    data = request.get_json()
    nova_categoria = Categoria(**data)
    db.session.add(nova_categoria)
    db.session.commit()
    return jsonify({'message': 'Categoria criada com sucesso'}), 201

@categoria_bp.route('/<int:id>', methods=['PUT'])
def update_categoria(id):
    data = request.get_json()
    categoria = Categoria.query.get_or_404(id)
    for key, value in data.items():
        setattr(categoria, key, value)
    db.session.commit()
    return jsonify({'message': 'Categoria atualizada'})

@categoria_bp.route('/<int:id>', methods=['DELETE'])
def delete_categoria(id):
    categoria = Categoria.query.get_or_404(id)
    db.session.delete(categoria)
    db.session.commit()
    return jsonify({'message': 'Categoria excluída'})
