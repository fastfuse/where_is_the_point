import json
import uuid
from collections import namedtuple

from flask import render_template, request, jsonify

from app import app, redis

POINTS_KEY = "POINTS"

LonLat = namedtuple("LonLat", ['longitude', 'latitude'])
Point = namedtuple("Point", ['uid', 'longitude', 'latitude', 'data'])


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/api/create_point', methods=['POST'])
def create_point():
    uid = str(uuid.uuid4())
    point = Point(uid=uid, **request.json)
    redis.set(uid, json.dumps(point._asdict()))
    redis.geoadd(POINTS_KEY, point.longitude, point.latitude, point.uid)

    return jsonify(status='OK', uid=uid), 201


@app.route('/api/scan', methods=["POST"])
def scan():
    position = LonLat(**request.json)

    # TODO: create partial for georadius
    pong = redis.georadius(POINTS_KEY, position.longitude, position.latitude,
                           radius=100, unit="m", withdist=True)
    data = list()

    if pong:
        for item in pong:
            uid = item[0].decode()
            point = json.loads(redis.get(uid))
            point.update(dist=item[1])
            data.append(point)

    return jsonify(result=data)
