import os
from flask import Flask
import redis as r
from pymongo import MongoClient

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


from app import views
from app import models
