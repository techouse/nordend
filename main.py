from app import create_app, cli, db
from app.models import User, Role, Permission, Post

app = create_app()
cli.register(app)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role, Permission=Permission, Post=Post)
