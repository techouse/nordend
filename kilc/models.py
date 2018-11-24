from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from kilc import db, login


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, index=True)
    email = db.Column(db.String(120), nullable=False, index=True, unique=True)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.name)


@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


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
