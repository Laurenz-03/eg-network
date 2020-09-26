from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = '71100e0e1a235b6e67a441043f514d52'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

#Instanz der Datenbank erzeugen
db = SQLAlchemy(app)

from app import routes