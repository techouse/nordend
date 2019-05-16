from flask_socketio import emit, join_room, leave_room

from ... import Config
from ... import socketio
from ...models import User


@socketio.on("authenticate", namespace="/{}".format(Config.BROADCAST_ROOM))
def authenticate(data):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room.
    """
    if "token" in data:
        current_user = User.verify_auth_token(data["token"])
        if current_user is not None:
            room = "authenticated.{}".format(Config.BROADCAST_ROOM)
            join_room(room)
            emit("authenticated", {"data": "{} has entered the room.".format(current_user.id)}, room=room)
        else:
            return False
    else:
        return False


@socketio.on("authenticate", namespace="/private.{}".format(Config.BROADCAST_ROOM))
def authenticate(data):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room.
    """
    if "token" in data:
        current_user = User.verify_auth_token(data["token"])
        if current_user is not None:
            room = "user.{}".format(current_user.id)
            join_room(room)
            emit(
                "authenticated",
                {"data": "{} has authenticated in a private channel".format(current_user.id)},
                room=room,
            )
        else:
            return False
    else:
        return False


@socketio.on("leave", namespace="/{}".format(Config.BROADCAST_ROOM))
def left(data):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room.
    """
    if "token" in data:
        current_user = User.verify_auth_token(data["token"])
        if current_user is not None:
            room = "authenticated.{}".format(Config.BROADCAST_ROOM)
            leave_room(room)
            emit("left", {"data": "{} has left.".format(current_user.id)}, room=room)
        else:
            return False
    else:
        return False


@socketio.on("leave", namespace="/private.{}".format(Config.BROADCAST_ROOM))
def left(data):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room.
    """
    if "token" in data:
        current_user = User.verify_auth_token(data["token"])
        if current_user is not None:
            room = "user.{}".format(current_user.id)
            leave_room(room)
            emit("left", {"data": "{} has left private channel".format(current_user.id)}, room=room)
        else:
            return False
    else:
        return False
