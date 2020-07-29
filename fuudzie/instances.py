#from flask_mongoengine import MongoEngine
from flask_jwt_extended import JWTManager, create_access_token
from mongoengine import connect
from flask_mail import Mail


jwt = JWTManager()
mail = Mail()

def initializeDB(app):
    #mongo.init_app(app)
    connect(app.config['MONGODB_DB'], host=app.config['MONGODB_HOST'], 
            port=app.config['MONGODB_PORT'], username=app.config['MONGODB_USERNAME'],
            password=app.config['MONGODB_PASSWORD'], authentication_source=app.config['MONGODB_AUTH_SOURCE'])

def initializeJWT(app):
    jwt.init_app(app)


def initializeMail(app):
    mail.init_app(app)    
