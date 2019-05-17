from .channels import PublicChannel as Channel
from ..schemas import PostSchema
from ... import socketio


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
