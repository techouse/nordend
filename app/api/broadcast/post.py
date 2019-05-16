from flask import g, current_app

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
            room="authenticated.{}".format(current_app.config["BROADCAST_ROOM"]),
            namespace="/{}".format(current_app.config["BROADCAST_ROOM"]),
        )
