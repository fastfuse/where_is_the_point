from datetime import datetime
from collections import namedtuple

from flask_jwt_extended import decode_token

from app import points_db, jwt

jwt_tokens_collection = points_db['jwt_tokens']


class TokenNotFound(Exception):
    """
    Indicates that a token could not be found in the database
    """
    pass


# namedtuple to simplify creation of response messages
Response = namedtuple('Response', ['status', 'message'])

# Longitude and Latitude object
LonLat = namedtuple("LonLat", ['longitude', 'latitude'])

# Point object
Point = namedtuple("Point", ['uid', 'longitude', 'latitude', 'data'])


def json_resp(status, message):
    """
    JSON-formatted response
    """
    return Response(status, message)._asdict()


# ======================== JWT helpers ================
# TODO: move to auth.utils?


@jwt.token_in_blacklist_loader
def check_if_token_revoked(decoded_token):
    """
    Callback function to check if a token has been revoked
    """
    return is_revoked(decoded_token)


@jwt.user_identity_loader
def user_identity_lookup(user):
    """
    A function that will be called whenever create_access_token
    is used. It will take whatever object is passed into the
    create_access_token method, and lets us define what the identity
    of the access token should be.
    """
    return str(user['_id'])


def epoch_utc_to_datetime(epoch_utc):
    """
    Helper function for converting epoch timestamps (as stored in JWTs) into python datetime objects.
    """
    return datetime.fromtimestamp(epoch_utc)


def store_token(encoded_token, identity_claim='identity'):
    """
    Adds a new token to the database. It is not revoked when it is added.
    """
    decoded_token = decode_token(encoded_token)

    token = dict(jti=decoded_token['jti'],
                 token_type=decoded_token['type'],
                 user_identity=decoded_token[identity_claim],
                 expires=epoch_utc_to_datetime(decoded_token['exp']),
                 revoked=False,
                 )

    jwt_tokens_collection.insert_one(token)


def is_revoked(decoded_token):
    """
    Checks if the given token is revoked. Because we are adding all the
    tokens that we create into DB, if the token is not present
    in the DB we are going to consider it revoked, as we don't know where
    it was created.
    """
    jti = decoded_token['jti']

    token = jwt_tokens_collection.find_one({"jti": jti})

    if not token:
        return True

    return token.revoked


def get_user_tokens(user_identity):
    """
    Returns all tokens for the given user
    """
    return jwt_tokens_collection.find({"user_identity": user_identity})


def revoke_token(token_id, user):
    """
    Revokes token by the given ID.
    Raises a TokenNotFound error if the token does not exist in DB
    """
    token = jwt_tokens_collection.find_one(dict(jti=token_id, user_identity=user))

    if not token:
        raise TokenNotFound("Could not find the token {}".format(token_id))

    # update
    # https://api.mongodb.com/python/current/api/pymongo/collection.html#pymongo.collection.Collection.update_one
