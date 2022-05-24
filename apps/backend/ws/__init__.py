from flask import Blueprint
from . import events


blueprint = Blueprint('ws_blueprint', __name__, url_prefix='/ws')

