from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    instaname1 = db.Column(db.String(60))
    instaname2 = db.Column(db.String(60))
    instaname3 = db.Column(db.String(60))

    # Wie der User später ausgegeben wird
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.instaname1}', '{self.instaname2}', '{self.instaname3}')"