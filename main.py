from app import create_app, cli, db, socketio
from app.models import User, Role, Permission, Post, Category, Image

app = create_app()
cli.register(app)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role, Permission=Permission, Post=Post, Category=Category, Image=Image)


if __name__ == "__main__":
    socketio.run(app)
