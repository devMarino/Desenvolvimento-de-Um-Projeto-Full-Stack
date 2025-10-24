
from flask import Flask
from config import Config # Assume que seu config.py está na raiz do projeto
from app.extensions import db, migrate # Importa db e migrate de app.extensions
from app.routes import register_blueprints # Importa a função de registro de blueprints
from app.seed import init_cli 

def create_app(config_class=Config):
    """Fábrica de aplicativos Flask."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    register_blueprints(app)

    init_cli(app)

    return app
