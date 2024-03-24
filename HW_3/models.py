from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(90), nullable=False)
    user_surname = db.Column(db.String(90), nullable=False)
    email = db.Column(db.String(130), unique=True, nullable=False)
    hashed_psw = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f'User({self.username}, {self.email})'