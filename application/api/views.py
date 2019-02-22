import json
import uuid

from flask import request, jsonify
from flask.views import View
from flask_jwt_extended import jwt_required

from application import redis, points_db, utils
from . import api_blueprint

POINTS_KEY = "POINTS"

users_collection = points_db['users']


class CreatePoint(View):
    """
    Create point resource
    """
    methods = ['POST']
    decorators = [jwt_required]

    def dispatch_request(self):
        uid = str(uuid.uuid4())
        point = utils.Point(uid=uid, **request.json)
        redis.set(uid, json.dumps(point._asdict()))
        redis.geoadd(POINTS_KEY, point.longitude, point.latitude, point.uid)

        return jsonify(status='OK', uid=uid), 201


class Scan(View):
    """
    Check if there are some Points near provided coordinates
    """
    methods = ['POST']
    decorators = [jwt_required]

    def dispatch_request(self):
        position = utils.LonLat(**request.json)

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


# =====================   Register endpoints   ==============================

api_blueprint.add_url_rule('/create_point',
                           view_func=CreatePoint.as_view("create_point_api"),
                           methods=['POST'])

api_blueprint.add_url_rule('/scan',
                           view_func=Scan.as_view("scan_api"),
                           methods=['POST'])
