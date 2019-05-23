from datetime import datetime

import pytz

from .channels import PublicChannel as Channel
from ..schemas import PostSchema
from ... import socketio, redis
import simplejson as json


class PostBroadcast:
    post_schema = PostSchema()

    @classmethod
    def _data(cls, post):
        return {"data": cls.post_schema.dump(post).data}

    @classmethod
    def created(cls, post):
        socketio.emit(
            "post.created", cls._data(post), broadcast=True, room=Channel.get_room(), namespace=Channel.NAMESPACE
        )

    @classmethod
    def updated(cls, post):
        socketio.emit(
            "post.updated", cls._data(post), broadcast=True, room=Channel.get_room(), namespace=Channel.NAMESPACE
        )

    @classmethod
    def deleted(cls, id_):
        socketio.emit(
            "post.deleted", {"data": {"id": id_}}, broadcast=True, room=Channel.get_room(), namespace=Channel.NAMESPACE
        )


@socketio.on("post.lock", namespace=Channel.NAMESPACE)
def locked(data):
    redis.set(
        "post_id_{}_locked".format(data["post_id"]),
        json.dumps(dict(**data, timestamp=int(datetime.now(pytz.utc).timestamp()))),
    )
    print(f"locked post {data['post_id']}")


@socketio.on("post.unlock", namespace=Channel.NAMESPACE)
def unlocked(data):
    redis.delete("post_id_{}_locked".format(data["post_id"]))
    print(f"unlocked post {data['post_id']}")
