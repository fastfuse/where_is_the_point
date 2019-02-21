import json
import uuid
from collections import namedtuple

from flask import render_template, request, jsonify, make_response

from app import app, redis, points_db, utils
from app.utils import hash_password

POINTS_KEY = "POINTS"

LonLat = namedtuple("LonLat", ['longitude', 'latitude'])
Point = namedtuple("Point", ['uid', 'longitude', 'latitude', 'data'])

users_collection = points_db['users']


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


@app.route('/api/register', methods=['POST'])
def register():
    """
    User registration
    """
    # get the post data
    data = request.get_json()

    # fetch user data
    user = users_collection.find_one({"username": data.get("username")})

    if not user:
        try:
            new_user = dict(username=data.get('username'),
                            password_hash=hash_password(data.get('password')))

            new_user_id = users_collection.insert_one(new_user).inserted_id

            response = utils.json_resp('Success', 'Successfully registered')

            return make_response(jsonify(response)), 201

        except Exception as e:
            # log.error(e)
            response = utils.json_resp('Fail', 'Some error occurred. Please try again later')
            return make_response(jsonify(response)), 500

    else:
        response = utils.json_resp('Fail', 'User already exists. Please Log in')
        return make_response(jsonify(response)), 202


@app.route('/api/login', methods=["POST"])
def login():
    """
    User login
    """
    # get the post data
    data = request.get_json()

    try:
        # fetch user data
        user = users_collection.find_one({"username": data.get("username")})

        if user:
            if not user.check_password(data.get('password')):
                response = utils.json_resp('Fail', 'Invalid password')
                return make_response(jsonify(response)), 400

            access_token = create_access_token(identity=user)
            refresh_token = create_refresh_token(identity=user)

            # store tokens to db
            utils.store_token(access_token)
            utils.store_token(refresh_token)

            response = {'status': 'Success',
                        'message': 'Successfully logged in',
                        'access_token': access_token,
                        'refresh_token': refresh_token
                        }

            return make_response(jsonify(response)), 200

        else:
            response = utils.json_resp('Fail', 'User does not exist')
            return make_response(jsonify(response)), 404

    except Exception as e:
        log.error(e)
        response = utils.json_resp('Fail', 'Try again')
        return make_response(jsonify(response)), 500