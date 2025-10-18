from flask import Flask
from flask_migrate import Migrate
from .models import db
from config import Config
from .seed import init_cli

migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    from app import models

    init_cli(app) # Inicializa os comandos CLI personalizados

    with app.app_context():
        try:
            db.create_all() #cria a tabela do banco
        except:
            print("Erro, o banco já existe") #caso ja tenha sido criaddo

    return app
