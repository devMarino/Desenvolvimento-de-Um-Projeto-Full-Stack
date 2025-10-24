from flask import Blueprint, request, jsonify
from app import db
from app.models.atendimento import Atendimento

atendimento_bp = Blueprint('atendimento', __name__)

@atendimento_bp.route('/', methods=['GET'])
def get_all_atendimentos():
    atendimentos = Atendimento.query.all()
    return jsonify([a.to_dict() for a in atendimentos])

@atendimento_bp.route('/<int:id>', methods=['GET'])
def get_atendimento(id):
    atendimento = Atendimento.query.get_or_404(id)
    return jsonify(atendimento.to_dict())

@atendimento_bp.route('/', methods=['POST'])
def create_atendimento():
    data = request.get_json()
    novo = Atendimento(**data)
    db.session.add(novo)
    db.session.commit()
    return jsonify({'message': 'Atendimento criado com sucesso'}), 201

@atendimento_bp.route('/<int:id>', methods=['PUT'])
def update_atendimento(id):
    data = request.get_json()
    atendimento = Atendimento.query.get_or_404(id)
    for k, v in data.items():
        setattr(atendimento, k, v)
    db.session.commit()
    return jsonify({'message': 'Atendimento atualizado'})

@atendimento_bp.route('/<int:id>', methods=['DELETE'])
def delete_atendimento(id):
    atendimento = Atendimento.query.get_or_404(id)
    db.session.delete(atendimento)
    db.session.commit()
    return jsonify({'message': 'Atendimento excluído'})
