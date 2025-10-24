class Config:
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root@localhost/flask_app"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    # SECRET_KEY = "123"    # nao tem senha no meu banco
    JSONIFY_PRETTYPRINT_REGULAR = True