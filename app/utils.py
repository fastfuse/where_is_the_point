from collections import namedtuple
from math import sin, cos, sqrt, atan2, radians

from werkzeug.security import generate_password_hash, check_password_hash

# approximate radius of earth in km
R = 6373.0


def calculate_points_distance(lat1, lon1, lat2, lon2):
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    return distance


def hash_password(password):
    return generate_password_hash(password)


def check_password(password, password_hash):
    return check_password_hash(password_hash, password)



# namedtuple to simplify creation of response messages
Response = namedtuple('Response', ['status', 'message'])


def json_resp(status, message):
    """
    JSON-formatted response
    """
    return Response(status, message)._asdict()
