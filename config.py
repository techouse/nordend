import os


class Config(object):
    APP_NAME = 'KILC d.o.o. Bovec'
    APP_LANG = 'en'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'im-not-lazy-im-just-very-relaxed'
