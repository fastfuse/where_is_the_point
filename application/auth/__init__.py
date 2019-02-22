from flask import Blueprint

auth_blueprint = Blueprint('auth_blueprint', __name__, url_prefix='/auth')

from . import views
