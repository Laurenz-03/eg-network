from datetime import datetime
from app import db, login_manager, app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


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
    instaid1 = db.Column(db.Integer())
    instaid2 = db.Column(db.Integer())
    instaid3 = db.Column(db.Integer())
    email_confirmed = db.Column(db.String(10), default='false')
    user_info = db.Column(db.String(), default="{}")
    marketplace_info = db.Column(db.String(), default="{}")
    rang_info = db.Column(db.String(), default="{}")

    def get_confirm_email_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_confirm_email_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)


    # Wie der User später ausgegeben wird
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.instaname1}', '{self.instaname2}', '{self.instaname3}')"