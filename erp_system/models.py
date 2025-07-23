from erp_system import db, app, login_manager
from sqlalchemy import Enum
from flask_login import UserMixin #methods for is_authenticated, etc.
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
            return f"User('{self.username}', '{self.email}')"

class Service(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    type = db.Column(db.String(20), nullable=False)
    client_name = db.Column(db.String(20), nullable=False)
    client_address = db.Column(db.String(30), nullable=False)
    client_phone = db.Column(db.String(20), nullable=False)
    status =  db.Column(Enum('En proceso', 'Completado', 'Cancelado', name='status_enum'), nullable=False, default='En proceso')
    comment = db.Column(db.String(100), nullable=True)

    def __repr__(self):
            return f"Service('{self.client_name}', '{self.type}')"
