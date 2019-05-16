from flask import g

from ..schemas import PostSchema
from ... import socketio

post_schema = PostSchema()


class PostBroadcast:
    @staticmethod
    def updated(post):
        socketio.emit(
            "post_updated",
            {"data": post_schema.dump(post).data},
            broadcast=True,
            namespace="/user.{}.ws".format(g.current_user.id),
        )
