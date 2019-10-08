# -*- coding: utf-8 -*-

"""Application configuration.

Most configuration is set via environment variables.

Use a .env file to set
environment variables.
"""

from environs import Env

env = Env()
env.read_env()

# FLASK config
ENV = env.str('FLASK_ENV', default='production')
DEBUG = ENV == 'development'

SECRET_KEY = env.str('SECRET_KEY')
FLASK_HOST = env.str('FLASK_HOST', default='127.0.0.1')
FLASK_PORT = env.int('FLASK_PORT', default=5000)
SEND_FILE_MAX_AGE_DEFAULT = env.int('SEND_FILE_MAX_AGE_DEFAULT')

SQLALCHEMY_DATABASE_URI = "mysql://{user}:{password}@{host}:{port}/{db}".format(
    user=env.str('DB_USER'),
    password=env.str("DB_PASSWORD"),
    host=env.str("DB_HOST"),
    port=env.str("DB_PORT", default="5432"),
    db=env.str("DB_NAME"))
