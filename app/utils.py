from math import sin, cos, sqrt, atan2, radians

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

if __name__ == '__main__':
    p1 = (49.843644, 24.026498)
    p2 = (49.843443, 24.026578)
    p3 = (49.839109, 24.030677)
    p4 = (49.838678, 24.030268)

    print(calculate_points_distance(*p3, *p4))
