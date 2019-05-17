from ... import Config


class PublicChannel:
    NAMESPACE = "/{}".format(Config.BROADCAST_ROOM)

    @staticmethod
    def get_room(user=None):
        return "authenticated.{}".format(Config.BROADCAST_ROOM)


class PrivateChannel:
    NAMESPACE = "/private.{}".format(Config.BROADCAST_ROOM)

    @staticmethod
    def get_room(user):
        return "user.{}".format(user.id)
