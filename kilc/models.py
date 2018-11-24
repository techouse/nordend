from kilc import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.name)


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

