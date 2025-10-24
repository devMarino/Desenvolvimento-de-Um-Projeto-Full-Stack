class Config:
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root@localhost/app_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    
    # --- DESCOMENTE ESTA LINHA ---
    SECRET_KEY = "sua-chave-secreta-pode-ser-qualquer-coisa" 
    
    JSONIFY_PRETTYPRINT_REGULAR = True