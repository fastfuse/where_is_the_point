import os

import redis as r
from flask import Flask
from flask_jwt_extended import JWTManager
from pymongo import MongoClient

# create application instance
app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])

# redis instance
redis = r.from_url(app.config['REDIS_URL'])

# mongo client
mongo_client = MongoClient(app.config['MONGODB_URL'])

# points db
points_db = mongo_client.points_db

# logger instance
logger = app.logger

# JWT stuff
jwt = JWTManager(app)

from .auth import auth_blueprint
from .index import index_blueprint
from .api import api_blueprint

app.register_blueprint(auth_blueprint)
app.register_blueprint(index_blueprint)
app.register_blueprint(api_blueprint)
