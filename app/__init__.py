from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from app.api import DoorAPI, ProductAPI, CustomerAPI, OrderAPI
import os
import rsa
from dotenv import load_dotenv
from flask_qrcode import QRcode

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

app = Flask(__name__)
app.config.from_object(Config)
datab = SQLAlchemy(app)
QRcode(app)
csrf = CSRFProtect()
csrf.init_app(app)
bcrypt = Bcrypt(app)

if os.environ.get("RSA_PUBLIC_KEY") == None or os.environ.get("RSA_PRIVATE_KEY") == None:
    publicKey, privateKey = rsa.newkeys(2048)
else:
    with open(os.environ.get("RSA_PUBLIC_KEY"), "rb") as file:
        public_key = file.read()
    with open(os.environ.get("RSA_PRIVATE_KEY"), "rb") as file:
        private_key = file.read()
    publicKey = rsa.PublicKey.load_pkcs1(public_key)
    privateKey = rsa.PrivateKey.load_pkcs1(private_key)

login_manager = LoginManager()
login_manager.init_app(app)

door_api = DoorAPI()
product_api = ProductAPI(token=os.environ.get('STEPPAY_SECRET_KEY'))
customer_api = CustomerAPI(token=os.environ.get('STEPPAY_SECRET_KEY'))
order_api = OrderAPI(token=os.environ.get('STEPPAY_SECRET_KEY'))

print(app.root_path)

from app import routes