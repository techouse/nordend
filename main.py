from kilc import create_app, cli, db
from kilc.models import User, Contact, Category, Product, Bottle

app = create_app()
cli.register(app)


@app.shell_context_processor
def make_shell_context():
    return {'db': db,
            'User': User,
            'Contact': Contact,
            'Category': Category,
            'Product': Product,
            'Bottle': Bottle}
