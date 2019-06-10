from app import create_app, cli, db, socketio
from app.models import User, Role, Permission, Post, Category, Image, Tag, PostCategory, PostImage, PostAuthor

app = create_app()
cli.register(app)


@app.shell_context_processor
def make_shell_context():
    return dict(
        db=db,
        Category=Category,
        Image=Image,
        Permission=Permission,
        Post=Post,
        PostAuthor=PostAuthor,
        PostCategory=PostCategory,
        PostImage=PostImage,
        Role=Role,
        Tag=Tag,
        User=User,
    )


if __name__ == "__main__":
    socketio.run(app)
