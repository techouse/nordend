from flask_socketio import emit, join_room, leave_room

from ..channels import AdminChannel as Channel
from .... import socketio
from ....models import User, Permission


@socketio.on("authenticate", namespace=Channel.NAMESPACE)
def authenticate(data):
    """Admin broadcast channel authentication"""
    if "token" in data:
        current_user = User.verify_auth_token(data["token"])
        if current_user is not None and current_user.can(Permission.ADMIN):
            room = Channel.get_room()
            join_room(room)
            emit("authenticated", {"data": "{} has entered the admin channel.".format(current_user.id)}, room=room)
        else:
            return False
    else:
        return False


@socketio.on("leave", namespace=Channel.NAMESPACE)
def left(data):
    """Admin broadcast channel departure"""
    if "token" in data:
        current_user = User.verify_auth_token(data["token"])
        if current_user is not None and current_user.can(Permission.ADMIN):
            room = Channel.get_room()
            leave_room(room)
            emit("left", {"data": "{} has left the admin channel.".format(current_user.id)}, room=room)
        else:
            return False
    else:
        return False
