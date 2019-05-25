from datetime import datetime

import pytz
import simplejson as json
from simplejson import JSONDecodeError

from ...redis_keys import locked_posts_redis_key
from ...models import User, Permission
from .channels import PublicChannel as Channel
from ..schemas import PostSchema
from ... import socketio, redis


class PostBroadcast:
    post_schema = PostSchema()

    @classmethod
    def _data(cls, post):
        return {"data": cls.post_schema.dump(post).data, "timestamp": datetime.now(pytz.utc).isoformat()}

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
            "post.deleted",
            {"data": {"id": id_}, "timestamp": datetime.now(pytz.utc).isoformat()},
            broadcast=True,
            room=Channel.get_room(),
            namespace=Channel.NAMESPACE,
        )

    @classmethod
    def locked(cls, id_):
        socketio.emit(
            "post.locked",
            {"data": {"id": id_}, "timestamp": datetime.now(pytz.utc).isoformat()},
            broadcast=True,
            room=Channel.get_room(),
            namespace=Channel.NAMESPACE,
        )

    @classmethod
    def unlocked(cls, id_):
        socketio.emit(
            "post.unlocked",
            {"data": {"id": id_}, "timestamp": datetime.now(pytz.utc).isoformat()},
            broadcast=True,
            room=Channel.get_room(),
            namespace=Channel.NAMESPACE,
        )

    @classmethod
    def list_locked(cls):
        socketio.emit(
            "post.list.locked",
            {
                "data": list(map(int, redis.hkeys(locked_posts_redis_key))),
                "timestamp": datetime.now(pytz.utc).isoformat(),
            },
            broadcast=True,
            room=Channel.get_room(),
            namespace=Channel.NAMESPACE,
        )


@socketio.on("post.list.locked", namespace=Channel.NAMESPACE)
def list_locked(data):
    if "token" in data:
        current_user = User.verify_auth_token(data["token"])
        if current_user is not None:
            return PostBroadcast.list_locked()
    return False


@socketio.on("post.lock", namespace=Channel.NAMESPACE)
def lock(data):
    if {"post_id", "token"} == data.keys():
        current_user = User.verify_auth_token(data["token"])
        if current_user is not None:
            redis.hset(
                locked_posts_redis_key,
                data["post_id"],
                json.dumps(
                    {
                        "post_id": int(data["post_id"]),
                        "user_id": int(current_user.id),
                        "timestamp": datetime.now(pytz.utc).isoformat(),
                    }
                ),
            )
            return PostBroadcast.locked(data["post_id"])
    return False


@socketio.on("post.unlock", namespace=Channel.NAMESPACE)
def unlock(data):
    if {"post_id", "token"} == data.keys():
        current_user = User.verify_auth_token(data["token"])
        if data["post_id"] is not None and current_user is not None:
            lock_data = redis.hget(locked_posts_redis_key, data["post_id"])
            if lock_data:
                try:
                    lock_data = json.loads(lock_data)
                    if {"post_id", "user_id", "timestamp"} == lock_data.keys() and (
                        lock_data["user_id"] == current_user.id or current_user.can(Permission.ADMIN)
                    ):
                        redis.hdel(locked_posts_redis_key, data["post_id"])
                        return PostBroadcast.unlocked(data["post_id"])
                except JSONDecodeError:
                    pass
    return False
