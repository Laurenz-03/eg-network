from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

#Flask konfigurieren
app.config['SECRET_KEY'] = '71100e0e1a235b6e67a441043f514d52'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

#Instanzen erzeugen
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from app import routes