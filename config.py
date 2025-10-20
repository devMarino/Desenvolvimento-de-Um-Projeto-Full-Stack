class Config:
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:devpassword@localhost/app_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
    SECRET_KEY = "123"  
    JSONIFY_PRETTYPRINT_REGULAR = True 

