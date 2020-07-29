import os
from dotenv import load_dotenv
load_dotenv()

# OR, the same with increased verbosity
load_dotenv(verbose=True)

# OR, explicitly providing path to '.env'
from pathlib import Path  # python3 only
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

DEBUG=bool(os.getenv('DEBUG'))
APP= os.getenv('APP')
SERVER_PORT= int(os.getenv('SERVER_PORT'))
ENV= os.getenv('ENV')
SECRET_KEY= os.getenv('SECRET_KEY')
TESTING= bool(os.getenv('TESTING'))
SESSION_COOKIE_NAME= os.getenv('SESSION_COOKIE_NAME')
MONGO_URI= os.getenv('MONGO_URI')
GOOGLE_API_KEY= os.getenv('GOOGLE_API_KEY')

MONGODB_HOST = os.getenv('MONGODB_HOST')
MONGODB_PORT = int(os.getenv('MONGODB_PORT'))
MONGODB_DB = os.getenv('MONGODB_DB')
MONGODB_USERNAME = os.getenv('MONGODB_USERNAME')
MONGODB_PASSWORD = os.getenv('MONGODB_PASSWORD')
MONGODB_AUTH_SOURCE = os.getenv('MONGODB_AUTH_SOURCE')
DEBUG_TB_ENABLED = os.getenv('DEBUG_TB_ENABLED')

JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
FLUTTERWAVE_SECRET=os.getenv('FLUTTERWAVE_SECRET')
FLUTTERWAVE_PUBLIC=os.getenv('FLUTTERWAVE_PUBLIC')

FLASK_ADMIN_SWATCH=os.getenv('FLASK_ADMIN_SWATCH')

MAIL_DEFAULT_SENDER=os.getenv('MAIL_DEFAULT_SENDER')
MAIL_SERVER=os.getenv('MAIL_SERVER')
MAIL_PORT=int(os.getenv('MAIL_PORT'))
MAIL_DEBUG= True
MAIL_USERNAME=os.getenv('MAIL_USERNAME')
MAIL_PASSWORD=os.getenv('MAIL_PASSWORD')
MAIL_SUPPRESS_SEND= False
MAIL_USE_TLS=False
MAIL_USE_SSL=True