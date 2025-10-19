from flask import Blueprint, request, jsonify
from app import db
from app.models.item import Item

item_bp = Blueprint('item', __name__)

@item_bp.route('/', methods=['GET'])
def get_all_items():
    items = Item.query.all()
    return jsonify([i.__dict__ for i in items])

@item_bp.route('/<int:id>', methods=['GET'])
def get_item(id):
    item = Item.query.get_or_404(id)
    return jsonify(item.__dict__)

@item_bp.route('/', methods=['POST'])
def create_item():
    data = request.get_json()
    novo = Item(**data)
    db.session.add(novo)
    db.session.commit()
    return jsonify({'message': 'Item criado com sucesso'}), 201

@item_bp.route('/<int:id>', methods=['PUT'])
def update_item(id):
    data = request.get_json()
    item = Item.query.get_or_404(id)
    for k, v in data.items():
        setattr(item, k, v)
    db.session.commit()
    return jsonify({'message': 'Item atualizado'})

@item_bp.route('/<int:id>', methods=['DELETE'])
def delete_item(id):
    item = Item.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Item excluído'})
