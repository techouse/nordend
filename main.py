from kilc import app, db
from kilc.models import User, Contact, Category, Product, Bottle


@app.shell_context_processor
def make_shell_context():
    return {'db': db,
            'User': User,
            'Contact': Contact,
            'Category': Category,
            'Product': Product,
            'Bottle': Bottle}
