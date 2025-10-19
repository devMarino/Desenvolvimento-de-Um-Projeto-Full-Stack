from flask import Flask
from config import Config
from app.extensions import db, migrate
from app.routes import register_blueprints
from app.seed import init_cli

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    register_blueprints(app)

    init_cli(app) # Inicializa os comandos personalizados
    with app.app_context():
        try:
            db.create_all() # Cria a tabela do banco
        except:
            print("Erro, o banco já existe") # Caso ja tenha sido criado

    return app
