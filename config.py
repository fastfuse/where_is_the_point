import os


class Config(object):
    DEBUG = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET_KEY',
                                '\x02=\xb5 !\t\x89\x1c~\xfc\xc8\xde\x92Z[zK\x7f\xe6\x14y\xb8\xbc\x94')


class DevelopmentConfig(Config):
    DEBUG = True
    REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379')


class ProductionConfig(Config):
    DEBUG = False
