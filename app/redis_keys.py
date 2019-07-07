from config import Config

locked_posts_redis_key = Config.REDIS_PREFIX + ":posts:locked"
user_otp_secret_key = Config.REDIS_PREFIX + "_user_id_{id}_otp_secret"
