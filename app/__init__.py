from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import datetime


app = Flask(__name__)

#Flask konfigurieren
app.config['SECRET_KEY'] = '71100e0e1a235b6e67a441043f514d52'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

#Instanzen erzeugen
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Du musst eingeloggt sein, um Zugriff auf diese Seite zu erhalten.'
login_manager.login_message_category = 'info'

admins = ['Laurenz', 'Felix', 'Stan']

eg_boost_runden = [
    {
    'id': 1,
    'name': 'EG-Boost Germany',
    'engage-mode': 'like_save',
    'tag-profile': 'eg-boost-germany',
    'upload-time': 40,
    'upload-start-time': datetime.time(20, 30),
    'upload-end-time': datetime.time(21, 10),
    'engage-time': 90,
    'engage-start-time': datetime.time(20, 30),
    'engage-end-time': datetime.time(22, 00),
    'upload-time-factor': 0,
    'engage-time-factor': 0
    },

    {
    'id': 2,
    'name': 'EG-Boost International',
    'engage-mode': 'like_save',
    'tag-profile': 'eg-boost-international',
    'upload-time': 40,
   'upload-start-time': datetime.time(20, 30),
    'upload-end-time': datetime.time(21, 10),
    'engage-time': 90,
    'engage-start-time': datetime.time(20, 30),
    'engage-end-time': datetime.time(22, 00),
    'upload-time-factor': 0,
    'engage-time-factor': 0
    },

    {
    'id': 3,
    'name': 'EG-Comment Germany',
    'engage-mode': 'comment',
    'tag-profile': 'eg-boost-germany',
    'upload-time': 40,
    'upload-start-time': datetime.time(20, 30),
    'upload-end-time': datetime.time(21, 10),
    'engage-time': 90,
    'engage-start-time': datetime.time(20, 30),
    'engage-end-time': datetime.time(22, 00),
    'upload-time-factor': 0,
    'engage-time-factor': 0
    },

    {
    'id': 4,
    'name': 'EG-Comment International',
    'engage-mode': 'comment',
    'tag-profile': 'eg-boost-international',
    'upload-time': 40,
    'upload-start-time': datetime.time(20, 30),
    'upload-end-time': datetime.time(21, 10),
    'engage-time': 90,
    'engage-start-time': datetime.time(20, 30),
    'engage-end-time': datetime.time(22, 00),
    'upload-time-factor': 0,
    'engage-time-factor': 0
    },
    ]

from app import routes
from app.errors.handlers import errors
app.register_blueprint(errors)