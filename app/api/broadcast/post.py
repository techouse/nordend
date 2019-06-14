from datetime import datetime, timedelta

import pytz
import simplejson as json

from .channels import PublicChannel as Channel
from ... import Config
from ... import socketio, redis
from ...models import User, Permission
from ...redis_keys import locked_posts_redis_key


class PostBroadcast:
    @staticmethod
    def created(post, by_user_id=None):
        socketio.emit(
            "post.created",
            {"data": post, "by_user_id": by_user_id, "timestamp": datetime.now(pytz.utc).isoformat()},
            broadcast=True,
            room=Channel.get_room(),
            namespace=Channel.NAMESPACE,
        )

    @staticmethod
    def updated(post, by_user_id=None):
        socketio.emit(
            "post.updated",
            {"data": post, "by_user_id": by_user_id, "timestamp": datetime.now(pytz.utc).isoformat()},
            broadcast=True,
            room=Channel.get_room(),
            namespace=Channel.NAMESPACE,
        )

    @staticmethod
    def deleted(id_, by_user_id=None):
        socketio.emit(
            "post.deleted",
            {"data": {"id": id_}, "by_user_id": by_user_id, "timestamp": datetime.now(pytz.utc).isoformat()},
            broadcast=True,
            room=Channel.get_room(),
            namespace=Channel.NAMESPACE,
        )

    @staticmethod
    def locked(id_, by_user_id=None, timestamp=None, expires=None):
        if timestamp is None:
            timestamp = datetime.now(pytz.utc)
        if expires is None and timestamp is not None:
            expires = timestamp + timedelta(seconds=Config.POST_EDIT_LOCK_TIMEOUT)
        socketio.emit(
            "post.locked",
            {
                "data": {"id": id_},
                "by_user_id": by_user_id,
                "timestamp": timestamp.isoformat(),
                "expires": expires.isoformat() if expires else None,
            },
            broadcast=True,
            room=Channel.get_room(),
            namespace=Channel.NAMESPACE,
        )

    @staticmethod
    def unlocked(id_, forced=False, notify_user_id=None, by_user_id=None):
        socketio.emit(
            "post.unlocked",
            {
                "data": {"id": id_},
                "forced": forced,
                "notify_user_id": notify_user_id,
                "by_user_id": by_user_id,
                "timestamp": datetime.now(pytz.utc).isoformat(),
            },
            broadcast=True,
            room=Channel.get_room(),
            namespace=Channel.NAMESPACE,
        )

    @staticmethod
    def list_locked():
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
            timestamp = datetime.now(pytz.utc)
            expires = timestamp + timedelta(seconds=Config.POST_EDIT_LOCK_TIMEOUT)
            redis.hset(
                locked_posts_redis_key,
                data["post_id"],
                json.dumps(
                    {
                        "post_id": int(data["post_id"]),
                        "by_user_id": current_user.id,
                        "timestamp": timestamp.isoformat(),
                        "expires": expires.isoformat(),
                    }
                ),
            )
            return PostBroadcast.locked(
                int(data["post_id"]), by_user_id=current_user.id, timestamp=timestamp, expires=expires
            )
    return False


@socketio.on("post.unlock", namespace=Channel.NAMESPACE)
def unlock(data):
    if {"post_id", "forced", "token"} == data.keys():
        current_user = User.verify_auth_token(data["token"])
        if data["post_id"] is not None and current_user is not None:
            lock_data = redis.hget(locked_posts_redis_key, data["post_id"])
            if lock_data:
                try:
                    lock_data = json.loads(lock_data)
                    if {"post_id", "by_user_id", "timestamp", "expires"} == lock_data.keys() and (
                        lock_data["by_user_id"] == current_user.id or current_user.can(Permission.MODERATE)
                    ):
                        redis.hdel(locked_posts_redis_key, data["post_id"])
                        return PostBroadcast.unlocked(
                            data["post_id"],
                            by_user_id=current_user.id,
                            forced=bool(data["forced"]),
                            notify_user_id=lock_data["by_user_id"],
                        )
                except:
                    pass
    return False
