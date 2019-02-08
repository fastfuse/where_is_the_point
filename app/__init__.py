import os
from flask import Flask
import redis as r

app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])

redis = r.from_url(app.config['REDIS_URL'])

from app import views
from app import models
