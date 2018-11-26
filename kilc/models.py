from datetime import datetime
from hashlib import md5
from time import time

import jwt
from flask import current_app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash

from . import db, login


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, index=True)
    email = db.Column(db.String(120), nullable=False, index=True, unique=True)
    about_me = db.Column(db.Text)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode({'reset_password': self.id, 'exp': time() + expires_in},
                          current_app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    def generate_confirmation_token(self, expires = 3600):
        s = Serializer(current_app.config['SECRET_KEY'], expires)
        return s.dumps({'confirm': self.id}).decode('utf-8')

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

    def __repr__(self):
        return '<User {}>'.format(self.name)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True, nullable=False, index=True)
    name = db.Column(db.String(120))
    address = db.Column(db.String(255))
    phone = db.Column(db.String(64))
    fax = db.Column(db.String(64))
    email = db.Column(db.String(120))

    def __repr__(self):
        return '<Contact {}>'.format(self.title)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, index=True, unique=True)
    products = db.relationship('Product', backref='category', lazy=True)

    def __repr__(self):
        return '<Category {}>'.format(self.name)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    name = db.Column(db.String(120), index=True, unique=True, nullable=False)
    description = db.Column(db.Text)
    potency = db.Column(db.Float, nullable=False, default=0)
    bottles = db.relationship('Bottle', backref='product', lazy=True)

    def __repr__(self):
        return '<Product {}>'.format(self.name)


class Bottle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    name = db.Column(db.String(120), index=True, nullable=False)
    volume = db.Column(db.Float, nullable=False, default=0)
    description = db.Column(db.Text)

    def __repr__(self):
        return '<Bottle {}>'.format(self.name)
