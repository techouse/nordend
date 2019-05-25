from config import Config

locked_posts_redis_key = "{}:posts:locked".format(Config.REDIS_PREFIX)