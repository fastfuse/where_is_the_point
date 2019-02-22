"""
Authentication views.
"""
from bson import ObjectId
from flask import request, make_response, jsonify
from flask.views import MethodView
from flask_jwt_extended import (create_access_token,
                                create_refresh_token,
                                get_jwt_identity,
                                jwt_required,
                                get_raw_jwt,
                                jwt_refresh_token_required)
from werkzeug.security import check_password_hash, generate_password_hash

from application import logger as log, points_db
from application import utils
from application.exceptions import TokenNotFound
from . import auth_blueprint

users_collection = points_db['users']


class RegistrationView(MethodView):
    """
    User Registration Resource
    """

    def post(self):
        # get the post data
        data = request.get_json()

        # get user from db
        user = users_collection.find_one({"username": data.get("username")})

        if not user:
            try:
                new_user = dict(username=data.get('username'),
                                password_hash=generate_password_hash(data.get('password')))

                new_user_id = users_collection.insert_one(new_user).inserted_id

                response = dict(status='Success', message='Successfully registered',
                                user_id=str(new_user_id))

                return make_response(jsonify(response)), 201

            except Exception as e:
                log.error(e)
                response = utils.json_resp('Fail', 'Some error occurred. Please try again later')
                return make_response(jsonify(response)), 500

        else:
            response = utils.json_resp('Fail', 'User already exists. Please Log in')
            return make_response(jsonify(response)), 202


class LoginView(MethodView):
    """
    User Login Resource
    """

    def post(self):
        # get the post data
        data = request.get_json()

        try:
            # fetch user data
            user = users_collection.find_one({"username": data.get("username")})

            if not user:
                response = utils.json_resp('Fail', 'User does not exist')
                return make_response(jsonify(response)), 404

            if not check_password_hash(user['password_hash'], data.get('password')):
                response = utils.json_resp('Fail', 'Password did not match')
                return make_response(jsonify(response)), 400

            access_token = create_access_token(identity=user)
            refresh_token = create_refresh_token(identity=user)

            # store tokens
            utils.store_token(access_token)
            utils.store_token(refresh_token)

            response = {'status': 'Success',
                        'message': 'Successfully logged in',
                        'access_token': access_token,
                        'refresh_token': refresh_token
                        }

            return make_response(jsonify(response)), 200

        except Exception as e:
            log.error(e)
            response = utils.json_resp('Fail', 'Try again')
            return make_response(jsonify(response)), 500


class LogoutView(MethodView):
    """
    User logout Resource.
    Invalidate (blacklist) user's access and refresh tokens
    """

    decorators = [jwt_required]

    def post(self):

        user_identity = str(get_jwt_identity())
        access_token_id = get_raw_jwt().get("jti")
        # refresh_token_id = get_jti(data.get("refresh_token"))

        try:
            utils.revoke_token(access_token_id, user_identity)
            # utils.revoke_token(refresh_token_id, user_identity)

            response = utils.json_resp('Success', 'Successfully Logged out')

            return make_response(jsonify(response)), 200

        except TokenNotFound as e:
            log.error(e)

            response = utils.json_resp('Failure', 'The specified token was not found')

            return make_response(jsonify(response)), 404


class RefreshTokenView(MethodView):
    """
    Token refresh Resource
    """

    decorators = [jwt_refresh_token_required]

    def get(self):
        user_identity = get_jwt_identity()
        user = users_collection.find_one({"_id": ObjectId(user_identity)})

        access_token = create_access_token(identity=user)
        utils.store_token(access_token)

        response = {'status': 'Success',
                    'access_token': access_token
                    }

        return make_response(jsonify(response)), 200


# =====================   Register endpoints   ==============================

auth_blueprint.add_url_rule('/register',
                            view_func=RegistrationView.as_view('registration'),
                            methods=['POST'])

auth_blueprint.add_url_rule('/login',
                            view_func=LoginView.as_view('login'),
                            methods=['POST'])

auth_blueprint.add_url_rule('/logout',
                            view_func=LogoutView.as_view('logout'),
                            methods=['POST'])

auth_blueprint.add_url_rule('/refresh',
                            view_func=RefreshTokenView.as_view('refresh'),
                            methods=['GET'])
