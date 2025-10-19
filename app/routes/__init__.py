from app.routes.categoria_routes import categoria_bp
from app.routes.cliente_routes import cliente_bp
from app.routes.fornecedor_routes import fornecedor_bp
from app.routes.item_routes import item_bp
from app.routes.pedido_routes import pedido_bp
from app.routes.atendimento_routes import atendimento_bp
from app.routes.item_pedido_routes import item_pedido_bp

def register_blueprints(app):
    app.register_blueprint(categoria_bp, url_prefix='/categorias')
    app.register_blueprint(cliente_bp, url_prefix='/clientes')
    app.register_blueprint(fornecedor_bp, url_prefix='/fornecedores')
    app.register_blueprint(item_bp, url_prefix='/itens')
    app.register_blueprint(pedido_bp, url_prefix='/pedidos')
    app.register_blueprint(atendimento_bp, url_prefix='/atendimentos')
    app.register_blueprint(item_pedido_bp, url_prefix='/itens_pedido')
