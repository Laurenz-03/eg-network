from app.errors.handlers import errors
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
import datetime, pytz


app = Flask(__name__)

# Flask konfigurieren
app.config['SECRET_KEY'] = '71100e0e1a235b6e67a441043f514d52'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

# Instanzen erzeugen
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login_no_aff'
login_manager.login_message = 'Du musst eingeloggt sein, um Zugriff auf diese Seite zu erhalten.'
login_manager.login_message_category = 'info'
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'egnetworkcomail@gmail.com'
app.config['MAIL_PASSWORD'] = '4f98j34h8r0sg4temail'
mail = Mail(app)

admins = ['Laurenz', 'Felix']

# Variablen in der Datenbank:
# user_info
#   - last_online
#   - htg_generator_usage
#   - analyzer_usage
#
#
#
#
#
#
#

smz = 2
wtz= 1
zeitfaktor = wtz

eg_boost_runden = [
    {
        'id': 1,
        'name': 'EG-Boost Germany',
        'engage-mode': 'like_save',
        'tag-profile': 'de_eg.boost',
        'start-time': datetime.time(19 -zeitfaktor, 30),
        'upload-end-time': datetime.time(20 -zeitfaktor, 00),
        'engage-end-time': datetime.time(21 -zeitfaktor, 00),
        'upload-time-factor': 0,
        'engage-time-factor': 0,
        'next-round-duration': [0, 0]
    },

    #{
    #    'id': 2,
    #    'name': 'EG-Boost International',
    #    'engage-mode': 'like_save',
    #    'tag-profile': 'int_eg.boost',
    #    'start-time': datetime.time(20 -zeitfaktor, 30),
    #    'upload-end-time': datetime.time(21 -zeitfaktor, 10),
    #    'engage-end-time': datetime.time(22 -zeitfaktor, 00),
    #    'upload-time-factor': 0,
    #    'engage-time-factor': 0,
    #    'next-round-duration': [0, 0]
    #},
    
    {
        'id': 3,
        'name': 'EG-Comment Germany',
        'engage-mode': 'comment',
        'tag-profile': 'de_eg.comment',
        'start-time': datetime.time(19 -zeitfaktor, 30),
        'upload-end-time': datetime.time(20 -zeitfaktor, 00),
        'engage-end-time': datetime.time(21 -zeitfaktor, 00),
        'upload-time-factor': 0,
        'engage-time-factor': 0,
        'next-round-duration': [0, 0]
    },

    #{
    #    'id': 4,
    #    'name': 'EG-Comment International',
    #    'engage-mode': 'comment',
    #    'tag-profile': 'int_eg.comment',
    #    'start-time': datetime.time(20 -zeitfaktor, 30),
    #    'upload-end-time': datetime.time(21 -zeitfaktor, 10),
    #    'engage-end-time': datetime.time(22 -zeitfaktor, 00),
    #    'upload-time-factor': 0,
    #    'engage-time-factor': 0,
    #    'next-round-duration': [0, 0]
    #},
]

app.register_blueprint(errors)

from app import routes
