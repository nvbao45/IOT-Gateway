from flask import Blueprint
from . import events

blueprint = Blueprint(
    'ota_blueprint',
    __name__,
    url_prefix='/ota'
)
