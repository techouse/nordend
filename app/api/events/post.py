from flask_socketio import emit

from ... import socketio
from ...models import Post
from ..schemas import PostSchema

post_schema = PostSchema()

namespace = "/posts_ws"


@socketio.on("init", namespace=namespace)
def handle_init(init):
    post_id = init.get("post_id")
    if post_id:
        post = Post.query.get(post_id)
        data = post_schema.dump(post).data
    else:
        data = None
    emit("init", {"data": data})
