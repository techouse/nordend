from flask_socketio import emit, join_room, leave_room

from ..channels import PrivateChannel as Channel
from .... import socketio
from ....models import User


@socketio.on("authenticate", namespace=Channel.NAMESPACE)
def authenticate(data):
    """Private broadcast channel authentication"""
    if "token" in data:
        current_user = User.verify_auth_token(data["token"])
        if current_user is not None:
            room = Channel.get_room(current_user)
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


@socketio.on("leave", namespace=Channel.NAMESPACE)
def left(data):
    """Private broadcast channel departure"""
    if "token" in data:
        current_user = User.verify_auth_token(data["token"])
        if current_user is not None:
            room = Channel.get_room(current_user)
            leave_room(room)
            emit("left", {"data": "{} has left private channel".format(current_user.id)}, room=room)
        else:
            return False
    else:
        return False
