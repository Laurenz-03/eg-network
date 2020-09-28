from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    eg_level = db.Column(db.Integer(), default=100)
    rang = db.Column(db.String(30), default='kein Rang')
    date_created = db.Column(db.DateTime, default=datetime.now)
    instaname1 = db.Column(db.String(60))
    instaname2 = db.Column(db.String(60))
    instaname3 = db.Column(db.String(60))

    # Wie der User später ausgegeben wird
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.instaname1}', '{self.instaname2}', '{self.instaname3}')"