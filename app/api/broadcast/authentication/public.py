from flask_socketio import emit, join_room, leave_room

from ..channels import PublicChannel as Channel
from .... import socketio
from ....models import User


@socketio.on("authenticate", namespace=Channel.NAMESPACE)
def authenticate(data):
    """Public broadcast channel authentication"""
    if "token" in data:
        current_user = User.verify_auth_token(data["token"])
        if current_user is not None:
            room = Channel.get_room()
            join_room(room)
            emit("authenticated", {"data": "{} has entered the room.".format(current_user.id)}, room=room)
        else:
            return False
    else:
        return False


@socketio.on("leave", namespace=Channel.NAMESPACE)
def left(data):
    """Public broadcast channel departure"""
    if "token" in data:
        current_user = User.verify_auth_token(data["token"])
        if current_user is not None:
            room = Channel.get_room()
            leave_room(room)
            emit("left", {"data": "{} has left.".format(current_user.id)}, room=room)
        else:
            return False
    else:
        return False
